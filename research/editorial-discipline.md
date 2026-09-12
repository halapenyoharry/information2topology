# Editorial Discipline: Edges Report, Incidences Interpret

**Status:** Architectural convention for the i2t project.
**Date:** 2026-04-29

## Principle

The format gives us three primitives — nodes, edges, incidences. Each has a different relationship to the source text, and the convention here is to keep that relationship principled instead of ad hoc.

```
Edge label              ← pure text, zero interpretation
Incidence ROLE          ← weak interpretation (text-mappable patterns)
Incidence ATTRS         ← strong interpretation (reader-imposed)
```

In one sentence: **the edges report; the incidences interpret.**

## What this means in practice

### Edges = text evidence

An edge between two nodes is the *connection itself*. Its identity should be the textual evidence that the connection exists — the actual phrase, sentence, or excerpt that brought the edge into being. Not a category label, not a predicate, not an abstraction.

If paragraph 42 contains the words `"Samara whispered, 'Lookout's on the way.'"`, the edge from paragraph 42 to the Samara node carries that excerpt as its `label`. Anyone looking at the edge can read what justified it. The graph becomes a textual index of itself — pointing at any edge tells you the passage that produced it.

For sequence edges between adjacent paragraphs, the label is the seam: last few words of the predecessor + first few words of the successor. `"...the rock fell back. ¶ No one called her..."`. 423 unique seams instead of 423 identical `next_paragraph` tags.

### Incidence ROLE = text-supported category

The role of each incidence describes how that particular endpoint *participates* in the connection. Roles can be categorical (`speaker`, `addressee`, `predecessor`, `successor`) — but each role should be derivable from a pattern in the text. The text *supports* the role even though the role is a category.

The role is the place where structural categorization lives. `speaker_of` doesn't belong on the edge as its identity; it belongs on the incidence pair as `(role: voice_carrier)` and `(role: speaker)`. The fact that this pattern adds up to "speaker_of" is metadata derivable from the role pair.

### Incidence ATTRS = interpretive annotation

This is where reader-imposed meaning lives. Functional roles ("antagonist," "ally," "mentor"), narrative significance ("turning point," "foreshadow"), confidence levels — anything the reader is consciously claiming about the participation. Different readers can disagree; their disagreement lives as different incidence attrs over the same edges.

Incidence attrs are the federation surface for reader-level annotation. Same text, same edges, different readers — different attrs.

## Why this division

It separates *reporting* from *interpretation* with a hard line:

- **Reporting** belongs to the edge layer. The text speaks. The label is what was said. Anyone who reads the source can verify any edge by looking up its passage.
- **Interpretation** belongs to the incidence layer. We — readers, annotators, downstream tools — get a sanctioned place to name what we think the participation means. Our claims are visibly ours, on incidences, not silently embedded in edge predicates.

This makes the graph honestly two-layered:

1. The *evidence layer* (edges) is reproducible across readers — anyone running the same extractor on the same text gets the same edges.
2. The *interpretation layer* (incidence attrs) is per-reader — annotators add their reading without changing the underlying topology.

Multi-reader federation becomes natural. Same edge graph, different incidence-attr layers per reader. Pivots between layers are pivots between readings.

## Concrete shape

For an evidence-bearing edge:

```json
edge: {
  "id": "edge:voice/p:ch01:042->samara",
  "directed": true,
  "attrs": {
    "label":          "Samara whispered, \"Lookout's on the way.\"",
    "i2t:predicate":  "speaker_of"
  }
}

incidences: [
  {
    "edge": "edge:voice/p:ch01:042->samara",
    "node": "p:ch01:042",
    "role": "voice_carrier",
    "attrs": { "alias_form": ["Samara"] }
  },
  {
    "edge": "edge:voice/p:ch01:042->samara",
    "node": "samara",
    "role": "speaker",
    "attrs": { "alias_form": ["Samara"] }
  }
]
```

Reading this:
- The edge carries the prose evidence as its label.
- The edge keeps `i2t:predicate` for tooling that filters/groups by relation type (downstream tools, layer detection).
- Each incidence carries a specific role (voice_carrier on the paragraph side, speaker on the character side) — both are categorical but text-supported.
- Each incidence can carry attrs — alias_form is one (which alias of the entity matched), but `narrative_significance: "turning_point"` could be another (interpretive).

## What changes from the prior 5-predicate version

What we built first put the predicate on the edge as `i2t:predicate`. Both ends of the edge had generic `source`/`target` roles, and the edge label defaulted to the predicate.

The shift is small but meaningful:
- Edge label moves from "speaker_of" to the actual prose excerpt that made the edge true.
- Incidence roles move from generic source/target to specific names (voice_carrier/speaker, predecessor/successor, perspective_lens/perspective_holder, etc.).
- Edge `i2t:predicate` stays on the edge for downstream tooling — it's not the edge's identity, just a categorical key for filtering.

Tools that group edges by predicate continue to work. JVV's layer panel continues to work. What changes is that *every edge in JVV now shows distinguishing information* — the actual text — rather than thousands of identical category labels.

## Naming conventions for incidence roles

For text-supported roles in the manuscript domain:

| Edge type             | Source-side role     | Target-side role        |
|-----------------------|----------------------|-------------------------|
| `next_paragraph`      | `predecessor`        | `successor`             |
| `POV_of`              | `perspective_lens`   | `perspective_holder`    |
| `speaker_of`          | `voice_carrier`      | `speaker`               |
| `addressee_of`        | `utterance`          | `addressee`             |
| `introduces`          | `debut_passage`      | `new_arrival`           |
| `referenced_by`       | `mention_passage`    | `referent`              |
| `mentions` (place/theme) | `mention_passage` | `mentioned`             |
| `scene_contains`      | `container`          | `member`                |
| `chapter_contains`    | `container`          | `member`                |
| `act_contains`        | `container`          | `member`                |
| `member_of_act`       | `member`             | `container`             |

These are the project's conventional role-pair names. Other domains will use different ones — same principle, different vocabulary.

## What this is NOT

- It's not a semantic web ontology. We're not trying to define universal predicates that everyone shares. We're naming what fits the manuscript-graph use case; other use cases will name differently.
- It's not RDF reification. The incidence is its own thing in this format, not a workaround for triples-only models. Reification (giving an incidence its own id and letting other edges reference it) is available but separate from the editorial-discipline convention here.
- It's not "text mining." We're not pulling triples *out of* unstructured text. We're producing graphs *from* deliberately authored text, where the text is the substrate of truth.

## Implementation

See:
- `adapters/manuscript_to_hypergraph.py` — emits edges with `label` (text evidence) and `members` form with role pairs.
- `adapters/instagraph_to_hypergraph.py` — propagates `label` through.
- `adapters/hypergraph_to_dyadic.py` — uses `attrs.label` as the visual edge label in the dyadic projection (with predicate as fallback and as the `layer` field for grouping).
