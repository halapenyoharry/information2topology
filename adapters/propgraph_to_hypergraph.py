#!/usr/bin/env python3
"""Adapter: property-graph JSON → TopoThink hypergraph.

Reads input files in the dirgraph / ghgraph / merged format:
    { "meta": {...},
      "nodes": [{"id": str, "properties": {...}}],
      "edges": [{"id": str, "source": str, "target": str, "label": str, "properties": {...}}] }

Writes a TopoThink hypergraph (see hypergraph.topothink.spec.md):
    { "metadata": {...},
      "nodes": [{"id": str, "attrs": {...}}],
      "edges": [{"id": str, "directed": bool, "attrs": {...}}],
      "incidences": [{"edge": str, "node": str, "role": str}] }

Vocabulary handling:
    - Node property keys are prefixed with the node ID's URI scheme (the part before the
      first ':'), so 'path' on an 'fs:...' node becomes 'fs:path'. Cross-scheme merges stay
      unambiguous and round-trip cleanly.
    - The edge label is preserved under 'i2t:predicate' on each output edge.
    - Edge custom properties (currently rare in this data) get prefixed with the source
      tool name to disambiguate.

Output edge IDs use a positional index ('edge:<source-tool>/<index>') to guarantee
uniqueness — input edge IDs may collide across sources in pre-merged files.
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path


def adapt(g: dict) -> tuple[dict, set[str]]:
    """Translate one property-graph document to a TopoThink hypergraph.

    Returns (hypergraph_doc, set_of_dangling_endpoint_ids).
    """
    meta = g.get("meta", {}) or {}
    tool = meta.get("tool") or "pg"

    out = {
        "metadata": {
            "topothink-version": "0.1",
            "adapter": "propgraph_to_hypergraph.py",
            "source-meta": meta,
        },
        "nodes": [],
        "edges": [],
        "incidences": [],
    }

    seen_ids: set[str] = set()
    for n in g.get("nodes", []):
        nid = n["id"]
        seen_ids.add(nid)
        scheme = nid.split(":", 1)[0] if ":" in nid else "attr"
        attrs = {f"{scheme}:{k}": v for k, v in (n.get("properties") or {}).items()}
        out["nodes"].append({"id": nid, "attrs": attrs})

    dangling: set[str] = set()
    for idx, e in enumerate(g.get("edges", [])):
        # Positional index guarantees uniqueness — input edge IDs may collide across
        # sources in pre-merged files (observed in projects-merged.graph.json: bare
        # 'e1' from dirgraph and 'e1' from ghgraph coexist).
        eid = f"edge:{tool}/{idx}"
        attrs = {"i2t:predicate": e.get("label", "")}
        if e.get("id"):
            attrs["i2t:original-id"] = e["id"]
        for k, v in (e.get("properties") or {}).items():
            attrs[f"{tool}:{k}"] = v
        out["edges"].append({"id": eid, "directed": True, "attrs": attrs})

        src, tgt = e["source"], e["target"]
        if src not in seen_ids:
            dangling.add(src)
        if tgt not in seen_ids:
            dangling.add(tgt)
        out["incidences"].append({"edge": eid, "node": src, "role": "source"})
        out["incidences"].append({"edge": eid, "node": tgt, "role": "target"})

    return out, dangling


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("input", help="Input property-graph JSON file")
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
        stem = inpath.stem
        for trim in (".graph", ".dirgraph", ".ghgraph"):
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
        if len(dangling) > 5:
            print(f"    ...and {len(dangling) - 5} more", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
