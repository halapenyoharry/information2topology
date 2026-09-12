"""Adjudicates relationships into the 4 canonical TopoThink categories:
1. Containment (Mereology / Scopes)
2. State Change (Transitions / Delta across t0 -> t1)
3. Interactivity (Constitutive Role Pairs - severance destroys endpoint roles)
4. Reference (Descriptive Pointers - severance leaves endpoints unchanged)
"""
from __future__ import annotations
from typing import Literal

EdgeCategory = Literal["containment", "state_change", "interactivity", "reference"]

# Built-in predicate dictionaries grounded in i2t v1.4.0 specification
PREDICATE_MAP: dict[str, EdgeCategory] = {
    # 1. Containment (Enclosures, Part-Whole, Scoping)
    "contains": "containment",
    "member_of": "containment",
    "part_of": "containment",
    "encloses": "containment",
    "subnet_of": "containment",
    "scope_of": "containment",
    "belongs_to": "containment",
    "includes": "containment",
    "has_chapter": "containment",
    "has_paragraph": "containment",
    "has_section": "containment",

    # 2. State Change (Temporal Deltas, Event Transitions, Motion)
    "next_paragraph": "state_change",
    "next_state": "state_change",
    "transitions_to": "state_change",
    "evolves_into": "state_change",
    "amends": "state_change",
    "transforms_to": "state_change",
    "transfers_possession": "state_change",
    "ptrans": "state_change",
    "moves_to": "state_change",
    "result_of": "state_change",
    "causes_state": "state_change",

    # 3. Interactivity (Constitutive Relations - severed edge destroys roles)
    "atrans": "interactivity",
    "hires": "interactivity",
    "is_hired_by": "interactivity",
    "lends": "interactivity",
    "borrows": "interactivity",
    "sues": "interactivity",
    "is_sued_by": "interactivity",
    "marries": "interactivity",
    "allied_with": "interactivity",
    "communicates_with": "interactivity",
    "speaks_to": "interactivity",
    "runtime_requires": "interactivity",
    "peering_with": "interactivity",
    "coauthors": "interactivity",
    "exchanges_with": "interactivity",
    "binds_to": "interactivity",

    # 4. Reference (Descriptive Relations - static pointers, citations, mentions)
    "cites": "reference",
    "mentions": "reference",
    "references": "reference",
    "mtrans": "reference",
    "static_imports": "reference",
    "imports": "reference",
    "criticizes": "reference",
    "endorses": "reference",
    "derives_from": "reference",
    "points_to": "reference",
    "links_to": "reference",
    "describes": "reference",
    "quoted_by": "reference"
}


def classify_relation(predicate: str, roles: list[str] | None = None, is_runtime: bool = False) -> EdgeCategory:
    """Classify a relation predicate into one of the four TopoThink categories.
    
    Adjudication Rules:
    - If explicit in PREDICATE_MAP, returns the canonical mapping.
    - If is_runtime is true for 'imports', resolves to 'interactivity' per v1.4.0 Addition 1.
    - Falls back to heuristic Severance / Boundary / Delta analysis.
    """
    p_norm = predicate.lower().strip().replace(" ", "_")

    # Special Case: 'imports' view-dependence (v1.4.0 Addition 1)
    if p_norm == "imports":
        return "interactivity" if is_runtime else "reference"

    if p_norm in PREDICATE_MAP:
        return PREDICATE_MAP[p_norm]

    # Heuristic checks on verb patterns
    # A. Containment patterns
    if any(k in p_norm for k in ("contain", "member", "inside", "parent", "child", "part")):
        return "containment"

    # B. State Change patterns (transitions, temporal sequence)
    if any(k in p_norm for k in ("next", "then", "after", "evolv", "becom", "transform", "shift", "delta", "result")):
        return "state_change"

    # C. Constitutive Interactivity (contractual role pairs, mutual actions)
    if any(k in p_norm for k in ("with", "between", "hire", "lend", "borrow", "trade", "deal", "socket", "call")):
        return "interactivity"

    # D. Default is Reference (descriptive, low optical weight)
    return "reference"
