#!/usr/bin/env python3
"""Adapter: InstaGraph-format JSON → TopoThink hypergraph.

Reads JSON in the schema used by yoheinakajima/instagraph (and any extractor
following that convention):

    { "metadata": {...},
      "nodes": [{"id", "label", "type", "color", "properties": {...}}, ...],
      "edges": [{"from", "to", "relationship", "direction", "color", "properties": {...}}, ...] }

Plus two backward-compatible EXTENSIONS for richer extractions that need to
exercise the hypergraph format more fully:

  1. *Hyperedges (n-ary)* — an edge MAY use `members` instead of `from`/`to`:

        {"members": [
            {"node": "alice",  "role": "subject"},
            {"node": "bob",    "role": "object"},
            {"node": "tuesday","role": "time"}
         ],
         "relationship": "Mary_kissed_John_on_Tuesday"}

     `members` is a list of either bare node-id strings (role defaults to
     "member") or {node, role, attrs} objects. Each member produces one
     incidence on the resulting edge.

  2. *Reified edges* — an edge MAY include an explicit `id` field. When the
     same id ALSO appears as a node id in the same file, the edge is reified
     (statements ABOUT it become possible). The same id appears in BOTH the
     output hypergraph's `nodes` list and `edges` list, per spec rule S4.

Vanilla InstaGraph files (no `members`, no edge `id`) still convert as before.

Writes a TopoThink hypergraph (see hypergraph.topothink.spec.md):

    { "metadata": {...},
      "nodes":      [{"id", "attrs": {...}}, ...],
      "edges":      [{"id", "directed", "attrs": {...}}, ...],
      "incidences": [{"edge", "node", "role", "attrs"?}, ...] }

Mapping:
    - Node `label`, `type`, `color`, and entries of `properties` flow into `attrs`
      (prefixed `instagraph:` for `type` and `color` to mark provenance; `label`
      and individual property keys passed through).
    - Edge `relationship` becomes `attrs["i2t:predicate"]` so the predicate is
      addressable everywhere downstream tooling expects it (split_by_predicate.py,
      hypergraph_to_dyadic.py both look there first).
    - Edge `direction == "directed"` (default) sets `directed: true` on the edge.
    - For a from/to edge: two incidences, source/target. For a `members` edge:
      one incidence per member with the supplied (or default) role.

Edge IDs without an explicit `id` are auto-namespaced `edge:instagraph/<index>`.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path


def adapt(g: dict) -> tuple[dict, set[str]]:
    """Translate one InstaGraph document to a TopoThink hypergraph.

    Returns (hypergraph_doc, set_of_dangling_endpoint_ids).
    """
    src_meta = g.get("metadata", {}) or {}

    out = {
        "metadata": {
            "topothink-version": "0.1",
            "adapter": "instagraph_to_hypergraph.py",
            "source-format": "instagraph",
            "source-meta": src_meta,
        },
        "nodes": [],
        "edges": [],
        "incidences": [],
    }

    seen_ids: set[str] = set()
    for n in g.get("nodes", []):
        nid = n["id"]
        seen_ids.add(nid)
        attrs: dict = {}
        if n.get("label"):
            attrs["label"] = n["label"]
        if n.get("type"):
            attrs["instagraph:type"] = n["type"]
        if n.get("color"):
            attrs["instagraph:color"] = n["color"]
        for k, v in (n.get("properties") or {}).items():
            attrs[k] = v
        out["nodes"].append({"id": nid, "attrs": attrs})

    dangling: set[str] = set()
    for idx, e in enumerate(g.get("edges", [])):
        # Extension 2: explicit edge id enables reification (id may also appear
        # in nodes list). Default to positional index when absent.
        eid = e.get("id") or f"edge:instagraph/{idx}"
        rel = e.get("relationship", "")
        attrs: dict = {"i2t:predicate": rel}
        # Editorial-discipline convention: optional `label` on the input edge
        # carries text-evidence for the connection. Propagated to attrs.label.
        if e.get("label"):
            attrs["label"] = e["label"]
        if e.get("color"):
            attrs["instagraph:color"] = e["color"]
        for k, v in (e.get("properties") or {}).items():
            attrs[k] = v
        directed = e.get("direction", "directed") == "directed"
        out["edges"].append({"id": eid, "directed": directed, "attrs": attrs})

        # Extension 1: `members` list takes precedence over from/to. Each entry
        # is either a bare node-id (role defaults to "member") or a dict with
        # node + role + optional attrs.
        members = e.get("members")
        if members is not None:
            for m in members:
                if isinstance(m, str):
                    node_id, role, m_attrs = m, "member", {}
                else:
                    node_id = m["node"]
                    role    = m.get("role", "member")
                    m_attrs = m.get("attrs", {}) or {}
                if node_id not in seen_ids:
                    dangling.add(node_id)
                inc: dict = {"edge": eid, "node": node_id, "role": role}
                if m_attrs:
                    inc["attrs"] = m_attrs
                out["incidences"].append(inc)
        else:
            src, tgt = e["from"], e["to"]
            if src not in seen_ids:
                dangling.add(src)
            if tgt not in seen_ids:
                dangling.add(tgt)
            out["incidences"].append({"edge": eid, "node": src, "role": "source"})
            out["incidences"].append({"edge": eid, "node": tgt, "role": "target"})

    return out, dangling


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("input", help="Input InstaGraph JSON file")
    ap.add_argument(
        "-o", "--output",
        help="Output hypergraph JSON file (default: derived from input filename)",
    )
    args = ap.parse_args()

    inpath = Path(args.input)
    with open(inpath) as f:
        g = json.load(f)

    hypergraph, dangling = adapt(g)

    if args.output:
        outpath = Path(args.output)
    else:
        stem = inpath.name
        for trim in (".instagraph.json", ".json"):
            if stem.endswith(trim):
                stem = stem[: -len(trim)]
                break
        outpath = inpath.with_name(f"{stem}.hypergraph.topothink.json")

    outpath.parent.mkdir(parents=True, exist_ok=True)
    with open(outpath, "w") as f:
        json.dump(hypergraph, f, indent=2)

    n_nodes = len(hypergraph["nodes"])
    n_edges = len(hypergraph["edges"])
    n_inc = len(hypergraph["incidences"])
    print(f"wrote {outpath}", file=sys.stderr)
    print(f"  nodes: {n_nodes:>6}  edges: {n_edges:>6}  incidences: {n_inc:>6}", file=sys.stderr)
    if dangling:
        print(
            f"  WARNING: {len(dangling)} edge endpoint(s) reference IDs missing from the input nodes list",
            file=sys.stderr,
        )
        for d in list(dangling)[:5]:
            print(f"    {d}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
