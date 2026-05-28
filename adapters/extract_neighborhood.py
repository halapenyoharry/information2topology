#!/usr/bin/env python3
"""Adapter: extract the K-hop neighborhood around anchor nodes from a TopoThink hypergraph.

Anchor selection options (mutually exclusive):
  --anchor-predicate <pred>   Seed = all nodes incident on edges with this predicate.
  --anchor-id-prefix <pfx>    Seed = all nodes whose id starts with this prefix.
  --anchor-ids <ids>          Seed = explicit comma-separated node IDs.

Expansion treats the hypergraph as undirected for traversal purposes (you want to
follow relationships in either direction when extracting context). The resulting
sub-hypergraph keeps:
  - all nodes within K hops of any anchor
  - all edges whose every incident node is in the kept node set
  - all incidences for kept edges

Output is itself a valid TopoThink hypergraph (closed structure, open vocabulary preserved).
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict


def adjacency(hypergraph: dict) -> dict[str, set[str]]:
    """Undirected adjacency derived from incidences."""
    edge_endpoints: dict[str, dict[str, list[str]]] = defaultdict(lambda: {"src": [], "tgt": [], "any": []})
    for inc in hypergraph.get("incidences", []):
        role = inc.get("role")
        bucket = "src" if role == "source" else "tgt" if role == "target" else "any"
        edge_endpoints[inc["edge"]][bucket].append(inc["node"])

    adj: dict[str, set[str]] = defaultdict(set)
    for eps in edge_endpoints.values():
        all_nodes = eps["src"] + eps["tgt"] + eps["any"]
        for a in all_nodes:
            for b in all_nodes:
                if a != b:
                    adj[a].add(b)
    return adj


def seed_anchors(hypergraph: dict, predicate: str | None,
                 id_prefix: str | None, explicit_ids: list[str] | None) -> set[str]:
    if explicit_ids:
        return set(explicit_ids)
    if id_prefix:
        return {n["id"] for n in hypergraph.get("nodes", []) if n["id"].startswith(id_prefix)}
    if predicate:
        edge_ids = {e["id"] for e in hypergraph.get("edges", [])
                    if (e.get("attrs") or {}).get("i2t:predicate") == predicate}
        return {inc["node"] for inc in hypergraph.get("incidences", []) if inc["edge"] in edge_ids}
    raise ValueError("Must supply one of --anchor-predicate, --anchor-id-prefix, --anchor-ids")


def expand(adj: dict[str, set[str]], seeds: set[str], hops: int) -> set[str]:
    visited = set(seeds)
    frontier = set(seeds)
    for _ in range(hops):
        new = set()
        for n in frontier:
            new |= adj.get(n, set())
        new -= visited
        if not new:
            break
        visited |= new
        frontier = new
    return visited


def extract(hypergraph: dict, kept_ids: set[str]) -> dict:
    nodes = [n for n in hypergraph.get("nodes", []) if n["id"] in kept_ids]
    incidences = [inc for inc in hypergraph.get("incidences", []) if inc["node"] in kept_ids]
    # An edge is kept if all its incidences land on kept nodes
    edge_kept_count: dict[str, int] = defaultdict(int)
    edge_total: dict[str, int] = defaultdict(int)
    for inc in hypergraph.get("incidences", []):
        edge_total[inc["edge"]] += 1
        if inc["node"] in kept_ids:
            edge_kept_count[inc["edge"]] += 1
    kept_edge_ids = {eid for eid in edge_total if edge_kept_count[eid] == edge_total[eid]}
    edges = [e for e in hypergraph.get("edges", []) if e["id"] in kept_edge_ids]
    incidences = [inc for inc in incidences if inc["edge"] in kept_edge_ids]
    return {
        "metadata": {
            **hypergraph.get("metadata", {}),
            "i2t:relation_to_canonical": "k-hop-neighborhood",
            "extraction-stats": {
                "nodes": len(nodes),
                "edges": len(edges),
                "incidences": len(incidences),
            },
        },
        "nodes": nodes,
        "edges": edges,
        "incidences": incidences,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--hops", type=int, default=1)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--anchor-predicate")
    g.add_argument("--anchor-id-prefix")
    g.add_argument("--anchor-ids", help="comma-separated")
    args = ap.parse_args()

    with open(args.input) as f:
        hypergraph = json.load(f)

    anchors = seed_anchors(
        hypergraph,
        args.anchor_predicate,
        args.anchor_id_prefix,
        args.anchor_ids.split(",") if args.anchor_ids else None,
    )
    adj = adjacency(hypergraph)
    kept = expand(adj, anchors, args.hops)
    extracted = extract(hypergraph, kept)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(extracted, f, indent=2)

    s = extracted["metadata"]["extraction-stats"]
    print(f"anchor seed: {len(anchors)} nodes  hops: {args.hops}", file=sys.stderr)
    print(f"extracted: {s['nodes']} nodes, {s['edges']} edges, {s['incidences']} incidences", file=sys.stderr)
    print(f"wrote: {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
