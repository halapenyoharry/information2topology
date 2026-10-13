"""Shared assembly helpers for the dead-detained-deported hypergraph.

Every builder in this example (the initial research-doc extraction and the
per-source fetchers in update_pipeline.py) goes through this module so that
IDs are deterministic: the same person, death, facility, or source always
produces the same node id, which is what makes merge-by-ID federation work
(hypergraph.topothink.spec.md rule S2).

Vocabulary prefixes used in this example:
  schema:   schema.org-style basics (name, url)
  dcterms:  provenance (dcterms:source lists source-node ids)
  i2t:      format-level keys (predicate, category, evidence, reified)
  ddd:      domain keys for this corpus (date_of_death, ledger_status, ...)
"""
from __future__ import annotations

import datetime
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
EXAMPLE_DIR = Path(__file__).resolve().parent
LAYERS_DIR = EXAMPLE_DIR / "layers"
SNAPSHOTS_DIR = EXAMPLE_DIR / "snapshots"
CANONICAL_PATH = EXAMPLE_DIR / "dead-detained-deported.hypergraph.topothink.json"
REGISTRY_PATH = EXAMPLE_DIR / "sources.registry.json"

TOPOTHINK_VERSION = "0.1"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text


def person_id(name: str) -> str:
    return f"person:{slugify(name)}"


def death_event_id(name: str, date_iso: str | None) -> str:
    # Date disambiguates persons who share a slugged name; "undated" keeps
    # determinism for deaths the sources report without a date.
    return f"event:death/{slugify(name)}-{date_iso or 'undated'}"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utcnow_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class GraphBuilder:
    """Accumulates nodes/edges/incidences and writes a canonical file."""

    def __init__(self, title: str, extra_metadata: dict | None = None):
        self.metadata = {"topothink-version": TOPOTHINK_VERSION, "title": title}
        if extra_metadata:
            self.metadata.update(extra_metadata)
        self.nodes: dict[str, dict] = {}
        self.edges: dict[str, dict] = {}
        self.incidences: list[dict] = []

    def node(self, node_id: str, **attrs) -> str:
        """Add or enrich a node. Later attrs never overwrite earlier ones."""
        existing = self.nodes.setdefault(node_id, {"id": node_id, "attrs": {}})
        for k, v in attrs.items():
            if v is not None:
                existing["attrs"].setdefault(k, v)
        return node_id

    def edge(
        self,
        edge_id: str,
        predicate: str,
        category: str,
        members: list[tuple[str, str | None]],
        evidence: str | None = None,
        sources: list[str] | None = None,
        directed: bool = False,
        reify: bool = False,
        **attrs,
    ) -> str:
        """Add an edge plus its incidences.

        members: list of (node_id, role) pairs; role may be None on
        undirected edges. All member node ids must already exist or are
        created bare. category must be one of the four in
        docs/edge-categories.md.
        """
        assert category in {"containment", "state_change", "interactivity", "reference"}
        edge_attrs = {"i2t:predicate": predicate, "i2t:category": category}
        if evidence:
            edge_attrs["i2t:evidence"] = evidence
        if sources:
            edge_attrs["dcterms:source"] = sources
        edge_attrs.update({k: v for k, v in attrs.items() if v is not None})
        edge_obj: dict = {"id": edge_id, "attrs": edge_attrs}
        if directed:
            edge_obj["directed"] = True
        self.edges[edge_id] = edge_obj
        if reify:
            self.node(edge_id, **{"i2t:reified": True})
        for node_id, role in members:
            if node_id not in self.nodes:
                self.node(node_id)
            inc = {"edge": edge_id, "node": node_id}
            if role:
                inc["role"] = role
            self.incidences.append(inc)
        return edge_id

    def to_doc(self) -> dict:
        return {
            "metadata": self.metadata,
            "nodes": list(self.nodes.values()),
            "edges": list(self.edges.values()),
            "incidences": self.incidences,
        }

    def write(self, path: Path) -> dict:
        doc = self.to_doc()
        sys.path.insert(0, str(REPO_ROOT))
        from engine.validator import validate_topothink_hypergraph

        ok, errors = validate_topothink_hypergraph(doc)
        if not ok:
            raise SystemExit("validation failed:\n" + "\n".join(errors))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(
            f"wrote {path.relative_to(REPO_ROOT)}: "
            f"{len(doc['nodes'])} nodes / {len(doc['edges'])} edges / "
            f"{len(doc['incidences'])} incidences (valid)"
        )
        return doc


def add_death(
    g: GraphBuilder,
    name: str,
    date_iso: str | None,
    ledger_status: str,
    sources: list[str],
    evidence: str,
    fiscal_year: str | None = None,
    facility: str | None = None,
    facility_role: str = "custodial_site",
    country_of_death: str | None = None,
    nationality: str | None = None,
    age: str | None = None,
    circumstances: str | None = None,
) -> str:
    """One death = one reified state-change hyperedge.

    The death is the central fact of this corpus, so it is an entity other
    edges can point at (registry membership, exclusion assertions, audits).
    ledger_status values used here:
      official                 on ICE's Detainee Death Reporting ledger
      excluded-post-release    released/paroled shortly before death, uncounted
      excluded-enforcement-op  lethal force during arrest operations, uncounted
      post-removal             died after deportation; outside US monitoring
      audit-documented         documented via PHR/ACLU clinical audits
    """
    pid = g.node(person_id(name), **{"schema:name": name, "ddd:nationality": nationality, "ddd:age_at_death": age})
    eid = death_event_id(name, date_iso)
    members: list[tuple[str, str | None]] = [(pid, "deceased")]
    if facility:
        members.append((facility, facility_role))
    if country_of_death:
        members.append((country_of_death, "country_of_death"))
    g.edge(
        eid,
        predicate="died",
        category="state_change",
        members=members,
        evidence=evidence,
        sources=sources,
        reify=True,
        **{
            "ddd:date_of_death": date_iso,
            "ddd:fiscal_year": fiscal_year,
            "ddd:ledger_status": ledger_status,
            "ddd:circumstances": circumstances,
        },
    )
    return eid
