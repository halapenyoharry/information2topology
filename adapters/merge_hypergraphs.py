#!/usr/bin/env python3
"""Merge N TopoThink hypergraph files into one, by ID (spec rule S2's payoff:
two files that share a node ID are already talking about the same node).

Non-destructive merge policy — nothing is lost:
  - Nodes merge by id. Attrs union; on a conflicting key the FIRST value wins
    and the losing value is recorded under attrs["i2t:conflicts"] as
    {key, value, from} so corrections remain visible instead of silently
    overwriting.
  - Edges merge by id under the same policy.
  - Incidences dedupe on (edge, node, role, id); otherwise concatenate.
  - Output metadata lists every input file, preserving each input's own
    metadata block under "i2t:merged_inputs".

Usage:
  python3 adapters/merge_hypergraphs.py layer1.json layer2.json ... -o merged.hypergraph.topothink.json
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from engine.validator import validate_topothink_hypergraph  # noqa: E402


def merge_attrs(existing: dict, incoming: dict, source_name: str) -> None:
    for k, v in incoming.items():
        if k not in existing:
            existing[k] = v
        elif existing[k] != v:
            conflicts = existing.setdefault("i2t:conflicts", [])
            conflicts.append({"key": k, "value": v, "from": source_name})


def merge(paths: list[Path]) -> dict:
    nodes: dict[str, dict] = {}
    edges: dict[str, dict] = {}
    incidences: list[dict] = []
    seen_inc: set[tuple] = set()
    merged_inputs = []

    for path in paths:
        doc = json.loads(path.read_text())
        ok, errors = validate_topothink_hypergraph(doc)
        if not ok:
            raise SystemExit(f"{path}: input failed validation:\n" + "\n".join(errors))
        merged_inputs.append({"file": str(path), "metadata": doc.get("metadata", {})})
        name = path.name

        for node in doc.get("nodes", []):
            target = nodes.setdefault(node["id"], {"id": node["id"], "attrs": {}})
            merge_attrs(target.setdefault("attrs", {}), node.get("attrs", {}), name)

        for edge in doc.get("edges", []):
            target = edges.setdefault(edge["id"], {"id": edge["id"], "attrs": {}})
            if edge.get("directed"):
                target["directed"] = True
            merge_attrs(target.setdefault("attrs", {}), edge.get("attrs", {}), name)

        for inc in doc.get("incidences", []):
            key = (inc["edge"], inc["node"], inc.get("role"), inc.get("id"))
            if key not in seen_inc:
                seen_inc.add(key)
                out = {"edge": inc["edge"], "node": inc["node"]}
                for opt in ("role", "id", "attrs"):
                    if opt in inc:
                        out[opt] = inc[opt]
                incidences.append(out)

    return {
        "metadata": {
            "topothink-version": "0.1",
            "title": "merged hypergraph",
            "merged_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "i2t:merged_inputs": merged_inputs,
        },
        "nodes": list(nodes.values()),
        "edges": list(edges.values()),
        "incidences": incidences,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", type=Path, help="canonical hypergraph files to merge, in priority order")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--title", default=None, help="title for the merged file's metadata")
    args = ap.parse_args()

    doc = merge(args.inputs)
    if args.title:
        doc["metadata"]["title"] = args.title
    ok, errors = validate_topothink_hypergraph(doc)
    if not ok:
        raise SystemExit("merged output failed validation:\n" + "\n".join(errors))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    conflict_count = sum(
        len(e.get("attrs", {}).get("i2t:conflicts", [])) for e in doc["nodes"] + doc["edges"]
    )
    print(
        f"merged {len(args.inputs)} files -> {args.out}: "
        f"{len(doc['nodes'])} nodes / {len(doc['edges'])} edges / {len(doc['incidences'])} incidences; "
        f"{conflict_count} attr conflicts recorded"
    )


if __name__ == "__main__":
    main()
