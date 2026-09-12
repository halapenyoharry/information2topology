# TopoThink Hypergraph Format Specification

**Status**: Normative for all data ingested into or produced by the i2t project.
**Version**: 0.1
**Date**: 2026-04-27
**Filename convention**: `*.hypergraph.topothink.json`
**Companion docs**: [`docs/edge-categories.md`](docs/edge-categories.md) for the four-category typology that classifies every edge (containment, state change, interactivity, reference) without requiring reification.

## Premise

This format is the canonical internal representation of any topology the project handles. Every input format (raw text, nested JSON, RDF, CSV, etc.) gets *translated* into a TopoThink hypergraph by an ingestion adapter; every output format (JGF, JSON-LD, HIF, visualization-ready data) gets *projected* from a TopoThink hypergraph by an emitter. The format itself is fixed — that fixity is what lets code generalize across formats.

**One structural commitment, zero vocabulary commitments.** That asymmetry is the central design choice and is non-negotiable.

The base data model is a **hypergraph** (in the standard mathematical sense): a set of nodes plus a set of edges, where each edge can connect any number of nodes. The `topothink` qualifier signals this project's specific extensions on top of vanilla hypergraph: reified edges, open-vocabulary attribute objects on every entity, explicit incidence records with roles, and the merge-by-ID semantics required for federation across files.

## Structural Rules (closed — these MUST hold)

### S1. Three primitive types, no others.

A TopoThink hypergraph file consists of exactly three kinds of entities: **nodes**, **edges**, and **incidences**. Every datum maps to one of these three. Hierarchy is expressed as edges, not as containment. Nested objects-within-objects are forbidden as primary structure.

### S2. Every node has a globally unique identifier.

Each node MUST have an `id` whose value is a globally unique string. URIs (`https://github.com/luanti-org/luanti`), URNs (`urn:isbn:9780670020584`), and content hashes (`sha256:abc...`) are all valid. Locally-scoped identifiers are PERMITTED but disable cross-file merging — use only for ephemeral data.

**Why:** globally unique IDs are what make the topology federable. Two files that share a node ID are already talking about the same node and unify on merge without code.

### S3. Every edge has its own identifier and lists its incident nodes via incidences.

Each edge MUST have an `id`. The connection between an edge and the nodes it touches lives in the `incidences` list, NOT inline in the edge object. Each incidence is an `{edge, node}` pair, optionally with `role`, `attrs`, and its own `id` (see S4).

**Why:** decoupling edges from incidences lets the same edge naturally extend to any number of nodes without schema change. It also lets incidences themselves carry attributes (e.g., role of this node in this edge).

### S4. All three primitives are reifiable.

The same id may appear in more than one of `nodes` / `edges` / `incidences`. When it does, the entity is *reified* — addressable from another edge as a node, allowing statements ABOUT it.

- **Edge reification** is the most common: an edge's `id` also appears as a node's `id`. The edge can then be the source or target of yet another edge.
- **Incidence reification** is available when needed: an incidence MAY carry an optional `id` field, and that `id` MAY also appear as a node's `id`. The incidence becomes referenceable — facts can be asserted about a particular participation ("this membership was verified on Tuesday by halapenyoharry").
- **Vertex reification** is trivially the base case (every node is already a node).

Incidences without an `id` are valid and common — they're position-identified within the `incidences` list and cannot be referenced by other entities. Adding an `id` is the cost of making a particular participation talkable-about.

**Why:** relations and participations are ontological citizens, not properties of the things related. Without reification you cannot say anything about a relationship itself ("Mary loves John" → "this assertion was witnessed by Sam, on 2026-04-27"), nor about a particular participation ("Lothal-on-WiFi was confirmed by ping at 2026-04-22"). The recursion goes one step further than most graph models permit; the format permits it without forcing it.

### S5. Edges connect any number of nodes (≥1).

An edge with one incidence is a unary fact. Two incidences = a dyadic relation. Three or more = an n-ary hyperedge. Edges with zero incidences are forbidden.

**Why:** real-world relationships are often not pairwise (chemical reaction, co-authorship, meeting attendees). Forcing them into pairs introduces information-destroying intermediate nodes.

### S6. Direction is optional and per-edge.

An edge MAY include a `directed: true` flag. If set, the edge MUST distinguish source incidences (`role: "source"`) from target incidences (`role: "target"`). Otherwise the edge is undirected.

### S7. Nodes, edges, and incidences MAY carry attributes.

Each entity supports an `attrs` object holding arbitrary key-value pairs. There is no constraint on what keys may appear, what types values may have, or what kinds of facts attach to which entity types.

## Vocabulary Rules (open — ANY key is permitted)

### V1. No predicate, type, label, or attribute key is constrained.

There is no list of allowed keys. New keys can appear in any file at any time without coordination.

### V2. Keys SHOULD be URI-prefixed.

For federability, attribute keys SHOULD be drawn from named vocabularies and prefixed accordingly: `schema:license`, `i2t:engineFramework`, `dcterms:creator`. Bare keys (`license`, `name`) are permitted but ambiguous on merge.

### V3. Vocabulary collisions resolve at ingest, not at schema.

If two files disagree about what `name` means, the conflict is resolved by the ingestion adapter (typically by namespacing one or both), not by rejecting files at the schema layer.

## Prohibitions

The following are invalid in this format and MUST be rejected by adapters:

- **Trees as primary structure.** Hierarchy is edges, not containment. A nested `children` array inside a node violates S1.
- **Anonymous edges.** Every edge has an ID (S3). Edges without IDs cannot be reified (S4) or referenced.
- **Closed enumerations of predicate keys.** The schema MUST NOT validate that attribute keys are drawn from a fixed list (V1).
- **Coordinates as primary data.** Visual layout (x/y, color, line style) is not part of the topology. It belongs in a separate rendering layer that consumes the hypergraph.

## Minimal example

```json
{
  "metadata": { "topothink-version": "0.1" },
  "nodes": [
    {"id": "https://github.com/luanti-org/luanti", "attrs": {"schema:name": "Luanti"}},
    {"id": "lang:cpp",                              "attrs": {"schema:name": "C++"}},
    {"id": "edge:luanti-written-in-cpp",            "attrs": {"i2t:reified": true}}
  ],
  "edges": [
    {"id": "edge:luanti-written-in-cpp", "directed": true,
     "attrs": {"i2t:predicate": "schema:programmingLanguage"}}
  ],
  "incidences": [
    {"edge": "edge:luanti-written-in-cpp", "node": "https://github.com/luanti-org/luanti", "role": "source"},
    {"edge": "edge:luanti-written-in-cpp", "node": "lang:cpp",                              "role": "target"}
  ]
}
```

The edge appears in both `nodes` and `edges` because it's reified — another edge can now state facts about this fact.

## Compatibility map

The TopoThink hypergraph format is structurally a superset of every format we use. Adapters do the projection work:

| Target format | Maps how |
|---|---|
| **HIF** (Hypergraph Interchange Format) | Direct: TopoThink ≈ HIF + reified-edge convention + URI-as-id convention |
| **JSON-LD / RDF** | Each incidence → a triple; reified edges → RDF-star quoted triples |
| **PG-JSON** (Neo4j-shaped) | Direct: reified edges become labeled relationships with their own properties |
| **JGF** (JSON Graph Format) | Lossy: drops hyperedges of arity ≠ 2 and reified-edge structure |
| **D3 force-directed** | Lossy: keeps node-pair edges only; collapses or drops everything else |

The lossiness of an emitter is a property of the target format, not a defect of the source.

## Vocabulary note

**This document deliberately does not use the word "substrate."** In Harry Tajchman's TopoThink work, *substrate* refers to the medium being transcended (filesystem, GitHub, JSON, RDF, language) — substrate-INDEPENDENCE is the thesis. Using "substrate" to name our specific file format would invert that meaning. The format is just a hypergraph (math) with TopoThink-specific extensions (reification, open-vocabulary attrs, incidence roles, merge-by-ID semantics).
