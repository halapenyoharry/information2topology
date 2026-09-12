#!/usr/bin/env python3
"""Adapter: TopoThink hypergraph (or any HIF-like file) → normalized dyadic JSON.

Produces a JSON file matching the NormalizedGraph interface negotiated with the
json-visual-viewer (JVV) in correspondence/json-visual-viewer.md:

    {
      "metadata": { "format": "normalized-dyadic", "flavor": "...",
                    "i2t:relation_to_canonical": "dyadic-projection",
                    "originalCounts": {...} },
      "nodes": [{"id", "label?", "kind": "node|hyperedge|edge-as-node", "attrs?": {...}}, ...],
      "links": [{"source", "target", "label?", "directed?", "role?", "layer?", "attrs?": {...}}, ...]
    }

Projection rules (from J2/J3/J4/J5 in the correspondence thread):

    - Arity-2 hyperedges that are NOT reified  →  one plain dyadic link, attrs on the link.
    - Arity-≥-3 OR reified                     →  synthetic node (kind="hyperedge"
                                                  if not in source nodes,
                                                  "edge-as-node" if reified) plus
                                                  one dyadic link per incidence.
    - Predicate (edge.attrs["i2t:predicate"] or fallbacks) becomes link.label AND
      link.layer (so JVV can use either independently).
    - Incidence role passes through verbatim ("source", "target", "member", or any
      open-vocabulary value).

Input is either a TopoThink hypergraph file (*.hypergraph.topothink.json) or any
HIF-shaped JSON with top-level nodes / edges / incidences arrays. The adapter
reads node/edge IDs from `id` (i2t) or `node`/`edge` (HIF) field names.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict


PREDICATE_FALLBACK_KEYS = (
    "i2t:predicate", "predicate", "relation", "type", "label",
)


def _node_id(n: dict) -> str:
    return n.get("id") or n["node"]


def _edge_id(e: dict) -> str:
    return e.get("id") or e["edge"]


def _predicate(edge: dict) -> str | None:
    attrs = edge.get("attrs") or {}
    for k in PREDICATE_FALLBACK_KEYS:
        v = attrs.get(k)
        if v:
            return v
    return edge.get("label") or None


def normalize(doc: dict) -> dict:
    src_nodes = doc.get("nodes", [])
    src_edges = doc.get("edges", [])
    src_incidences = doc.get("incidences", [])

    src_node_ids: set[str] = {_node_id(n) for n in src_nodes}

    # Group incidences by edge
    inc_by_edge: dict[str, list[dict]] = defaultdict(list)
    for inc in src_incidences:
        inc_by_edge[inc["edge"]].append(inc)

    out_nodes: list[dict] = []
    out_links: list[dict] = []
    seen_node_ids: set[str] = set()

    # Pass 1: emit every source node as kind="node" (kind upgraded later if reified)
    for n in src_nodes:
        nid = _node_id(n)
        if nid in seen_node_ids:
            continue
        seen_node_ids.add(nid)
        entry = {"id": nid, "kind": "node"}
        attrs = n.get("attrs")
        if attrs:
            entry["attrs"] = attrs
            # Pull a label out of common attr keys for display ergonomics
            for k in ("schema:name", "name", "label", "title"):
                if attrs.get(k):
                    entry["label"] = attrs[k]
                    break
        out_nodes.append(entry)

    # Index for kind-upgrades
    out_node_by_id = {n["id"]: n for n in out_nodes}

    # Pass 2: project edges
    for e in src_edges:
        eid = _edge_id(e)
        incidences = inc_by_edge.get(eid, [])
        arity = len(incidences)
        reified = eid in src_node_ids
        predicate = _predicate(e)
        edge_attrs = e.get("attrs") or {}
        directed = e.get("directed", True)

        if arity == 0:
            # Spec forbids zero-incidence edges, but be defensive.
            continue

        if arity == 2 and not reified:
            # Plain dyadic projection. Try canonical source/target roles first
            # (legacy from/to edges). If absent, take incidences in order and
            # carry whatever per-end roles are set (editorial-discipline shape:
            # role pairs like predecessor/successor, voice_carrier/speaker).
            src_inc = next((i for i in incidences if i.get("role") == "source"), None)
            tgt_inc = next((i for i in incidences if i.get("role") == "target"), None)
            if not (src_inc and tgt_inc):
                src_inc, tgt_inc = incidences[0], incidences[1]
            src_node, tgt_node = src_inc["node"], tgt_inc["node"]
            link: dict = {
                "source": src_node,
                "target": tgt_node,
                "directed": directed,
            }
            # Editorial-discipline convention: prefer text-evidence label
            # (attrs.label) over the categorical predicate. Predicate still
            # rides as link.layer for grouping/filtering.
            text_label = edge_attrs.get("label")
            if text_label:
                link["label"] = text_label
            elif predicate:
                link["label"] = predicate
            if predicate:
                link["layer"] = predicate
            # Per-end role pair (e.g., predecessor/successor or voice_carrier/speaker)
            if src_inc.get("role"):
                link["source_role"] = src_inc["role"]
            if tgt_inc.get("role"):
                link["target_role"] = tgt_inc["role"]
            if edge_attrs:
                link["attrs"] = edge_attrs
            out_links.append(link)
        else:
            # Dyadic projection of an arity-≥-3 or reified edge.
            # The hyperedge needs to exist as a node so dyadic links can address it.
            if reified:
                # Already in nodes; upgrade its kind.
                if eid in out_node_by_id:
                    out_node_by_id[eid]["kind"] = "edge-as-node"
                    if predicate and "label" not in out_node_by_id[eid]:
                        out_node_by_id[eid]["label"] = predicate
                else:
                    entry = {"id": eid, "kind": "edge-as-node"}
                    if predicate:
                        entry["label"] = predicate
                    if edge_attrs:
                        entry["attrs"] = edge_attrs
                    out_nodes.append(entry)
                    out_node_by_id[eid] = entry
            else:
                entry = {"id": eid, "kind": "hyperedge"}
                if predicate:
                    entry["label"] = predicate
                if edge_attrs:
                    entry["attrs"] = edge_attrs
                out_nodes.append(entry)
                out_node_by_id[eid] = entry

            # Emit one dyadic link per incidence. Link direction follows incidence role:
            #   role=source: incidence node → hyperedge (the node is the origin)
            #   role=target: hyperedge → incidence node
            #   anything else: hyperedge → incidence node (undirected-ish)
            for inc in incidences:
                role = inc.get("role")
                inc_node = inc["node"]
                if role == "source":
                    link_src, link_tgt = inc_node, eid
                else:
                    link_src, link_tgt = eid, inc_node
                inc_link: dict = {
                    "source": link_src,
                    "target": link_tgt,
                    "directed": directed,
                }
                if role:
                    inc_link["role"] = role
                if predicate:
                    inc_link["layer"] = predicate
                inc_attrs = inc.get("attrs")
                if inc_attrs:
                    inc_link["attrs"] = inc_attrs
                out_links.append(inc_link)

    src_meta = doc.get("metadata", {}) or {}
    out_meta = {
        "format": "normalized-dyadic",
        "flavor": "dyadic-projection-from-hypergraph",
        "i2t:relation_to_canonical": "dyadic-projection",
        "originalCounts": {
            "nodes": len(src_nodes),
            "edges": len(src_edges),
            "incidences": len(src_incidences),
        },
        "source-metadata": src_meta,
    }

    return {
        "metadata": out_meta,
        "nodes": out_nodes,
        "links": out_links,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("input", help="Input hypergraph JSON file (TopoThink or HIF-shaped)")
    ap.add_argument(
        "-o", "--output",
        help="Output normalized-dyadic JSON file (default: derived from input filename)",
    )
    args = ap.parse_args()

    inpath = Path(args.input)
    with open(inpath) as f:
        doc = json.load(f)

    normalized = normalize(doc)

    if args.output:
        outpath = Path(args.output)
    else:
        stem = inpath.name
        for trim in (".hypergraph.topothink.json", ".json"):
            if stem.endswith(trim):
                stem = stem[: -len(trim)]
                break
        outpath = inpath.with_name(f"{stem}.normalized-dyadic.json")

    outpath.parent.mkdir(parents=True, exist_ok=True)
    with open(outpath, "w") as f:
        json.dump(normalized, f, indent=2)

    n_nodes = len(normalized["nodes"])
    n_links = len(normalized["links"])
    kinds = defaultdict(int)
    for n in normalized["nodes"]:
        kinds[n["kind"]] += 1

    print(f"wrote {outpath}", file=sys.stderr)
    print(f"  nodes: {n_nodes:>6}  links: {n_links:>6}", file=sys.stderr)
    print(f"  node kinds: {dict(kinds)}", file=sys.stderr)
    orig = normalized["metadata"]["originalCounts"]
    print(f"  source: {orig['nodes']} nodes, {orig['edges']} edges, {orig['incidences']} incidences",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
