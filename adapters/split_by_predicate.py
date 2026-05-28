#!/usr/bin/env python3
"""Adapter: split a TopoThink hypergraph into one hypergraph file per edge predicate.

Each output file contains:
  - all edges whose 'i2t:predicate' attribute matches the given predicate
  - all incidences belonging to those edges
  - all nodes touched by those incidences (no orphan nodes)

This implements the multilayer-network insight: a single TopoThink hypergraph is the
canonical superposition of multiple distinct topological layers, one per relation type.
Layer-split files render and reason about each layer independently, while staying
format-conforming so they can be merged back losslessly by ID-matching.

Usage:
    python3 adapters/split_by_predicate.py <input.hypergraph.topothink.json> -o <output-dir>
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict


def split(hypergraph: dict) -> dict[str, dict]:
    """Return {predicate: hypergraph-document} for each predicate in the input."""
    edges_by_pred: dict[str, list[dict]] = defaultdict(list)
    for e in hypergraph.get("edges", []):
        pred = (e.get("attrs") or {}).get("i2t:predicate") or "untagged"
        edges_by_pred[pred].append(e)

    nodes_by_id = {n["id"]: n for n in hypergraph.get("nodes", [])}
    incidences_by_edge: dict[str, list[dict]] = defaultdict(list)
    for inc in hypergraph.get("incidences", []):
        incidences_by_edge[inc["edge"]].append(inc)

    out: dict[str, dict] = {}
    base_meta = hypergraph.get("metadata", {})

    for pred, edges in edges_by_pred.items():
        edge_ids = {e["id"] for e in edges}
        layer_incidences = [inc for inc in hypergraph.get("incidences", []) if inc["edge"] in edge_ids]
        layer_node_ids = {inc["node"] for inc in layer_incidences}
        layer_nodes = [nodes_by_id[nid] for nid in layer_node_ids if nid in nodes_by_id]

        out[pred] = {
            "metadata": {
                **base_meta,
                "i2t:relation_to_canonical": "predicate-layer",
                "layer-predicate": pred,
                "layer-stats": {
                    "nodes": len(layer_nodes),
                    "edges": len(edges),
                    "incidences": len(layer_incidences),
                },
            },
            "nodes": layer_nodes,
            "edges": edges,
            "incidences": layer_incidences,
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Input TopoThink hypergraph JSON file")
    ap.add_argument("-o", "--output-dir", required=True,
                    help="Output directory; one <stem>.<predicate>.hypergraph.topothink.json file per predicate")
    args = ap.parse_args()

    inpath = Path(args.input)
    with open(inpath) as f:
        hypergraph = json.load(f)

    layers = split(hypergraph)

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    stem = inpath.name.replace(".hypergraph.topothink.json", "").replace(".json", "")

    print(f"input: {inpath.name}", file=sys.stderr)
    print(f"  total nodes: {len(hypergraph.get('nodes', []))}", file=sys.stderr)
    print(f"  total edges: {len(hypergraph.get('edges', []))}", file=sys.stderr)
    print(f"  layers found: {len(layers)}", file=sys.stderr)

    for pred, doc in sorted(layers.items(), key=lambda x: -len(x[1]["edges"])):
        # Sanitize predicate for filename
        safe = pred.replace(":", "_").replace("/", "_")
        outpath = outdir / f"{stem}.layer-{safe}.hypergraph.topothink.json"
        with open(outpath, "w") as f:
            json.dump(doc, f, indent=2)
        s = doc["metadata"]["layer-stats"]
        print(f"  layer '{pred}': {s['nodes']:>5} nodes, {s['edges']:>5} edges → {outpath.name}",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
