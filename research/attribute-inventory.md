# Attribute Inventory and Block Addressing

**Status:** Working paper (2026-08-19). Supersedes the ad-hoc `source_line` / `source_char_offset` anchoring introduced in the v3 Ramayana run.
**Related:** `editorial-discipline.md` (the firebreak), `paragraph-as-nodes.md` (author-given structure), `decomposition-rendering-and-whats-next.md`.

---

## The question this answers

What, exactly, can be ascertained per node and per edge from source material — and where does each fact come from?

The motivating problem is practical. The v3 Ramayana extraction anchors 68 of 72 nodes back to the source text, which works, but the mechanism was invented under pressure and never specified. Node text is pulled into the Exoskeleton text pane by a single character offset into a monolithic `.canonical.txt`. It functions. It is also brittle in a way that will not survive an editable manuscript.

Specifying it properly turns out to require answering a prior question: *what is the thing being pointed at?*

---

## 1. Provenance is the organizing axis

The editorial discipline already separates evidence from interpretation. Extending it to every attribute means each one declares where it came from. Three classes, and only three:

| class | meaning | may be contested? |
|---|---|---|
| **extracted** | Lifted from the source. A verbatim string, or a position in it. | No. It is either there or it is not. |
| **derived** | Computed from extracted material by a stated rule. | Only by disputing the rule. |
| **interpreted** | Reader judgment. | Yes, freely. This is the pluralistic layer. |

The value of the split is that a disagreement can be located. If two annotators differ on an extracted attribute, one of them made an error. If they differ on a derived attribute, they disagree about a rule, and the rule can be examined. If they differ on an interpreted attribute, they may both be right — that is the layer where divergence is permitted, and where the convergence test expects to find it.

### On render hints

An earlier draft of this note proposed a third tier for presentation data — a namespace of non-binding hints a viewer could ignore. That tier is rejected.

If the text says the cloak was red, the redness is **extracted**. It carries exactly the same evidential status as any other fact the text states, and a viewer may use it for color or ignore it entirely. If the text does not say the cloak was red, we have no business supplying a color. There is no case remaining for a presentation tier: text-stated appearance is evidence, and non-text-stated appearance is invention.

The viewer holds the strong opinions about rendering. We hold the text.

---

## 2. Block addressing: what the anchors point at

### The problem with character offsets

An offset into a monolithic string is a position in a coordinate system that has no structure. It has two failure modes:

1. **Edit fragility.** Insert one character at the top of the file and every downstream offset is wrong. Silently wrong — the graph still loads, the text pane still scrolls, and it scrolls to the wrong place. For a frozen corpus (Project Gutenberg, a published edition) this never happens. For a manuscript being written in a creative workspace, it happens constantly.

2. **Structural blindness.** The offset does not know it is inside a paragraph. It cannot say "this node is mentioned in the same paragraph as that one" without arithmetic over neighboring offsets.

### The resolution: the text is a sequence of blocks

Stop treating the source as one string. Treat it as an **ordered sequence of addressable blocks**, where a block is a unit the author already chose — a paragraph, most often; a sentence, a line of verse, or a stanza where the form calls for it.

```json
"blocks": [
  { "id": "b:0001", "text": "OM. Ná·rad, the saint, of hermits chief..." },
  { "id": "b:0002", "text": "The good Válmíki, first and best..." }
]
```

Each block carries a stable identifier that does not encode its position. `b:0042` stays `b:0042` when a paragraph is inserted above it.

This is the same move `paragraph-as-nodes.md` already made for node authority — author-given structure comes for free and should not be discarded. Here it is applied to addressing rather than to node extraction, but it is the same underlying commitment: **the units the author chose are the units we point at.**

### Anchors become block-relative

```json
"anchors": [
  { "block": "b:0001", "offset": 9, "length": 5 }
]
```

The block id is the load-bearing part. The offset and length are a refinement *within* the block.

This gives graceful degradation instead of catastrophic delamination. Edit a paragraph and only the sub-offsets inside that one paragraph go stale — every other anchor in the document is untouched, and the edited block's anchors still resolve to the right paragraph. The failure shrinks from "the entire document is misaligned" to "one paragraph needs its offsets recomputed," which is a job a re-anchoring pass can do locally.

Sub-offsets are optional. An anchor of `{ "block": "b:0042" }` alone is valid and means "somewhere in this paragraph" — enough to scroll a text pane, which is most of what the OSC bus needs.

### Consequence: the full text can live in the canonical file

Once the text is a structured sequence rather than an opaque blob, embedding it in the canonical hypergraph stops being unpleasant. The blocks are the thing everything points at, so they belong with the thing that points.

This deletes a requirement. A previous version of this design bound an external text file to the hypergraph by content hash, so that a mismatch would fail loudly rather than misrender silently. With the blocks inside the file, **there is nothing external to mismatch with.** The failure mode is gone rather than detected, which is strictly better.

The canonical unit becomes one file:

```
ramayana-canto1.hypergraph.topothink.json
  ├── blocks[]       ← the source text, in author-given units
  ├── nodes[]        ← anchored into blocks
  ├── edges[]        ← anchored into blocks
  └── incidences[]   ← interpretation
```

A note on size, since it will be asked: this file gets large, and that is acceptable. The renderer never loads it. Viewers load projections — a predicate layer, a k-hop neighborhood — which is what `split_by_predicate` and `extract_neighborhood` already produce. The canonical file is the source of truth, not the render payload. Confusing the two is what produced the current habit of committing `.normalized-dyadic.json` files as if they were artifacts rather than views.

### Why not inline markers in the prose

The rejected alternative was to mark the text itself: `[nodeid:1234]...[nodeid:1234]`.

It fails on overlap. Two annotations whose spans partially overlap without nesting cannot both be expressed — one must be split into fragments, and the fragment boundaries are artifacts of the other annotation rather than of the text. This is the oldest known failure in text encoding, fought under the name *overlapping hierarchies* since the early days of SGML.

The deeper objection is that inline markup **is the tree-prior**. It requires the annotations to form a single well-nested hierarchy, which is precisely the constraint this project exists to reject. Rejecting JSON's tree-prior while adopting markup's tree-prior would be inconsistent.

Block addressing keeps the prose clean. Structure lives in the block sequence; the text of each block is exactly what the author wrote, with nothing interpolated.

---

## 3. The inventory

### Per node

| attribute | provenance | notes |
|---|---|---|
| `id` | assigned | globally unique (S2) |
| `quote` | extracted | surface form exactly as it appears in the source |
| `label` | interpreted | normalized display form |
| `anchors[]` | extracted | **plural** — see §4 |
| text-stated properties | extracted | only what the source predicates of the entity |

The `quote` / `label` split is the fix that took anchoring from 5/74 (v2) to 68/72 (v3). Local models normalize spellings by reflex — `Daśaratha` for `Dasaratha` — and fighting that instinct failed twice. Giving the model somewhere to put the normalized form, while requiring the verbatim one alongside it, worked immediately. The lesson generalizes: **when a model reliably wants to do something, give it a field for that thing rather than a prohibition against it.**

### Per edge

| attribute | provenance | notes |
|---|---|---|
| `id` | assigned | |
| `quote` | extracted | the excerpt evidencing the relation — this is the firebreak |
| `anchors[]` | extracted | where that evidence sits |
| `predicate` | interpreted | verb normalized from the quote |
| `edge_category` | derived | four-category decision procedure (whitepaper §4) |
| `edge_category_review` | derived | set when the edge sits on a category boundary |
| `constitutive` \| `descriptive` | derived | the cut test (v1.4.0 changeset, Addition 1) |
| `directed` | derived | S6 |

Edges are the weak half of the current extraction and it shows: 69 of 102 anchored, against 68 of 72 for nodes, and `edge_category` missing on all 102. Since edges are where the evidence lives, an unanchored edge is an assertion without a citation. The v3 edge `{ predicate: "invokes", label: "OM." }` is the failure in miniature — "OM." is not evidence that anything invokes anything.

### Per incidence

`edge` · `node` · `role`, plus `attrs`. Unchanged. This is the interpretation layer and is meant to be contested.

---

## 4. Anchors are plural

A node's anchor set is **every mention**. Nárad appears repeatedly in Canto 1; the current schema stores the first hit and discards the rest, so clicking Nárad scrolls to occurrence one and never to any other.

An edge's anchor set is normally **one** — the specific passage where the relation is asserted. An edge may carry several if the text asserts the same relation in several places, but each anchor must independently evidence the relation.

This asymmetry has a direct consequence for the text pane. Node selection wants *highlight all occurrences, then step through them*. Edge selection wants *go to this passage*. Those are different interactions and the schema should make the difference legible rather than leaving the viewer to guess.

---

## 5. Open: when is a text-stated property an attribute, and when is it an edge?

"The cloak was red." Two readings:

- `attrs: { color: "red" }` on the cloak node
- a Reference edge from `cloak` to a `red` node

The edge-first commitment leans toward the edge. But taken to its conclusion every adjective becomes a node, and the graph inflates into exactly the hairball this project exists to avoid.

The proposed rule is the one already derived for reification, applied one level down:

> **A property stays an attribute until something else points at it.**

If `red` is only ever the cloak's color, it is an attribute — nothing is gained by promoting it. If three objects are red and the text draws a connection between them, `red` has earned nodehood by being referenced.

This is *reification is earned by reference* (whitepaper §4) operating on properties rather than on relations. That the same rule governs both is mild evidence it is the right rule.

The question is left open here because it is entangled with node categorization — whether nodes admit a small closed typology the way edges do — which is deliberately deferred.

---

## Summary of decisions

1. Every attribute declares provenance: **extracted**, **derived**, or **interpreted**.
2. No presentation tier. Text-stated appearance is evidence; non-text-stated appearance is invention.
3. The source text is an **ordered sequence of author-given blocks** with stable ids, not a monolithic string.
4. Anchors are **block-relative**, with optional sub-offsets. Edits degrade locally instead of globally.
5. The blocks live **inside** the canonical file. One file is the canonical unit; the hash-binding requirement is thereby deleted rather than satisfied.
6. Dyadic and InstaGraph forms are **projections generated on demand**, not artifacts to commit.
7. Anchors are **plural** on nodes, normally singular on edges, and the two drive different text-pane interactions.

## Open

- Attribute versus edge for text-stated properties (§5).
- Node categorization — whether a closed typology exists for nodes as it does for edges. Deferred.
- Block granularity: paragraph by default, but verse, dialogue, and aphoristic prose may want sentence or line. Whether granularity is per-document or per-region is unresolved.
- Sub-block re-anchoring after an edit: recomputing offsets within a changed block is mechanical, but nothing implements it yet.
