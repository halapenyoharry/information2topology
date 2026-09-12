"""Validates that a JSON document conforms to the closed structural commitments
of the TopoThink hypergraph format (hypergraph.topothink.schema.json).
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any


class SchemaValidationError(Exception):
    pass


def validate_topothink_hypergraph(doc: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validates structural integrity of a TopoThink Hypergraph document.
    
    Checks:
    1. Top-level required keys: 'nodes', 'edges', 'incidences'
    2. Nodes have non-empty string 'id'
    3. Edges have non-empty string 'id'
    4. Incidences have non-empty string 'edge' and 'node'
    5. Every incidence 'edge' points to a declared edge id
    6. Every incidence 'node' points to a declared node id
    7. If edge.directed == True, incidences have a non-empty 'role'
    """
    errors: list[str] = []

    for req in ("nodes", "edges", "incidences"):
        if req not in doc or not isinstance(doc[req], list):
            errors.append(f"Missing or invalid top-level key: '{req}' (must be a list)")

    if errors:
        return False, errors

    node_ids: set[str] = set()
    for idx, node in enumerate(doc["nodes"]):
        if not isinstance(node, dict) or "id" not in node or not isinstance(node["id"], str) or not node["id"]:
            errors.append(f"Node at index {idx} lacks a valid non-empty string 'id'")
        else:
            node_ids.add(node["id"])

    edges_by_id: dict[str, dict] = {}
    for idx, edge in enumerate(doc["edges"]):
        if not isinstance(edge, dict) or "id" not in edge or not isinstance(edge["id"], str) or not edge["id"]:
            errors.append(f"Edge at index {idx} lacks a valid non-empty string 'id'")
        else:
            edges_by_id[edge["id"]] = edge

    for idx, inc in enumerate(doc["incidences"]):
        if not isinstance(inc, dict):
            errors.append(f"Incidence at index {idx} is not an object")
            continue

        e_ref = inc.get("edge")
        n_ref = inc.get("node")

        if not e_ref or not isinstance(e_ref, str):
            errors.append(f"Incidence at index {idx} lacks valid 'edge' reference")
        elif e_ref not in edges_by_id:
            errors.append(f"Incidence at index {idx} references undefined edge id '{e_ref}'")

        if not n_ref or not isinstance(n_ref, str):
            errors.append(f"Incidence at index {idx} lacks valid 'node' reference")
        elif n_ref not in node_ids:
            errors.append(f"Incidence at index {idx} references undefined node id '{n_ref}'")

        # Directed constraint
        if e_ref and e_ref in edges_by_id:
            parent_edge = edges_by_id[e_ref]
            if parent_edge.get("directed") is True:
                role = inc.get("role")
                if not role or not isinstance(role, str):
                    errors.append(f"Incidence at index {idx} belongs to directed edge '{e_ref}' but lacks required 'role'")

    return len(errors) == 0, errors


def assert_valid_topothink(doc: dict[str, Any]) -> None:
    valid, errors = validate_topothink_hypergraph(doc)
    if not valid:
        msg = f"TopoThink Schema Validation Failed with {len(errors)} error(s):\n" + "\n".join(f"- {e}" for e in errors[:10])
        if len(errors) > 10:
            msg += f"\n... and {len(errors) - 10} more."
        raise SchemaValidationError(msg)
