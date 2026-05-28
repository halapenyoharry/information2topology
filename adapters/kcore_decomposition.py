"""
kcore_decomposition.py — Transform adapter for the TopoThink hypergraph format.

Reads a *.hypergraph.topothink.json file, computes the k-core decomposition,
and writes the result back with core numbers annotated on each node.

The core number of a node is the highest k for which that node belongs to the
k-core (the maximal subgraph where every vertex has at least k connections).
Nodes in higher cores are more deeply embedded in the dense center of the graph.
Nodes in low cores are peripheral.

Usage:
    python3 adapters/kcore_decomposition.py data/wizard-of-oz.hypergraph.topothink.json

Output:
    - Annotates each node with attrs["i2t:core-number"]
    - Writes a summary to stdout
    - Optionally splits into per-shell layer files with --split

Dependencies:
    pip install networkx (only external dep)
"""

import json
import sys
import os
import argparse
from collections import Counter

try:
    import networkx as nx
except ImportError:
    print("networkx required: pip install networkx", file=sys.stderr)
    sys.exit(1)


def load_hypergraph(path):
    with open(path) as f:
        return json.load(f)


def build_nx_graph(hg):
    """Build a NetworkX graph from a TopoThink hypergraph.

    For k-core purposes we only need undirected connectivity.
    Hyperedges of arity >= 3 are expanded to cliques among their members
    (k-core cares about degree, not about whether the connection was
    dyadic or n-ary in the source).
    """
    G = nx.Graph()

    for node in hg["nodes"]:
        G.add_node(node["id"])

    # Group incidences by edge
    edge_members = {}
    for inc in hg["incidences"]:
        edge_id = inc["edge"]
        node_id = inc["node"]
        edge_members.setdefault(edge_id, []).append(node_id)

    # Add edges (clique expansion for arity >= 3)
    for edge_id, members in edge_members.items():
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                G.add_edge(members[i], members[j])

    return G


def annotate_core_numbers(hg, core_numbers):
    """Add i2t:core-number to each node's attrs."""
    node_map = {n["id"]: n for n in hg["nodes"]}
    for node_id, core_num in core_numbers.items():
        if node_id in node_map:
            node = node_map[node_id]
            if "attrs" not in node:
                node["attrs"] = {}
            node["attrs"]["i2t:core-number"] = core_num


def split_by_shell(hg, core_numbers, stem, out_dir):
    """Write one hypergraph file per k-shell (nodes at exactly core number k)."""
    shells = {}
    for node_id, k in core_numbers.items():
        shells.setdefault(k, set()).add(node_id)

    written = []
    for k in sorted(shells.keys()):
        shell_nodes = shells[k]
        # Include nodes in this shell
        nodes = [n for n in hg["nodes"] if n["id"] in shell_nodes]
        # Include edges where ALL members are in this shell or deeper
        at_least_k = {nid for nid, cn in core_numbers.items() if cn >= k}
        edge_members = {}
        for inc in hg["incidences"]:
            edge_members.setdefault(inc["edge"], []).append(inc["node"])

        keep_edges = set()
        for eid, members in edge_members.items():
            if all(m in shell_nodes for m in members):
                keep_edges.add(eid)

        edges = [e for e in hg["edges"] if e["id"] in keep_edges]
        incidences = [i for i in hg["incidences"] if i["edge"] in keep_edges]

        shell_hg = {
            "metadata": dict(hg.get("metadata", {})),
            "nodes": nodes,
            "edges": edges,
            "incidences": incidences,
        }
        shell_hg["metadata"]["i2t:shell"] = k
        shell_hg["metadata"]["i2t:shell-node-count"] = len(nodes)

        out_path = os.path.join(out_dir, f"{stem}.shell-{k}.hypergraph.topothink.json")
        with open(out_path, "w") as f:
            json.dump(shell_hg, f, indent=2)
        written.append((k, len(nodes), len(edges), out_path))

    return written


def main():
    parser = argparse.ArgumentParser(description="k-core decomposition for TopoThink hypergraphs")
    parser.add_argument("input", help="Path to *.hypergraph.topothink.json")
    parser.add_argument("--split", action="store_true", help="Write per-shell layer files")
    parser.add_argument("-o", "--output", help="Output path (default: overwrite input with annotations)")
    args = parser.parse_args()

    hg = load_hypergraph(args.input)
    G = build_nx_graph(hg)

    # Compute core numbers
    core_numbers = nx.core_number(G)

    # Annotate
    annotate_core_numbers(hg, core_numbers)

    # Summary
    shell_counts = Counter(core_numbers.values())
    max_core = max(core_numbers.values()) if core_numbers else 0
    print(f"Nodes: {len(core_numbers)}")
    print(f"Max core: {max_core}")
    print(f"Shells:")
    for k in sorted(shell_counts.keys()):
        print(f"  k={k}: {shell_counts[k]} nodes")

    # Write annotated file
    out_path = args.output or args.input
    with open(out_path, "w") as f:
        json.dump(hg, f, indent=2)
    print(f"\nAnnotated: {out_path}")

    # Optional split
    if args.split:
        stem = os.path.basename(args.input).replace(".hypergraph.topothink.json", "")
        out_dir = os.path.dirname(args.input)
        written = split_by_shell(hg, core_numbers, stem, out_dir)
        print(f"\nShell files:")
        for k, nn, ne, path in written:
            print(f"  k={k}: {nn} nodes, {ne} edges -> {path}")


if __name__ == "__main__":
    main()
