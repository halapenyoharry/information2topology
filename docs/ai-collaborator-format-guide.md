# AI Collaborator Format Guide

When you hand a graph to another AI to reason about, the right file depends on which AI. Different models have different strengths in schema interpretation, context budget, and tolerance for indirection. This document records those choices and the reasoning behind them, so the decision survives the conversation it was made in.

The three formats this project produces:

| File | Structure | Size class |
|---|---|---|
| `*.instagraph.json` | InstaGraph + i2t extensions, dyadic edges with i2t hyperedge encoding | source format |
| `*.hypergraph.topothink.json` | Canonical hypergraph: nodes + edges + explicit `incidences` array | structurally richest |
| `*.normalized-dyadic.json` | Flattened: every n-ary edge becomes an edge-as-node plus dyadic links to its members | flattest, library-friendly |

## Quick reference

| AI collaborator | Best file | Why |
|---|---|---|
| **Advanced reasoning models (large context)** | `hypergraph.topothink.json` | Handles reified hyperedges and incidence lookups natively; preserves topology |
| **Local models (7B-30B, via ollama etc)** | `normalized-dyadic.json` | Self-contained rows; no indirection; `layer` field lets the model filter by relationship type |
| **Smaller open models (7B-13B)** | `normalized-dyadic.json` | Smaller models reason best on flat, explicit-everything structures |
| **D3 / Cytoscape / Sigma / react-force-graph** | `normalized-dyadic.json` | These libraries assume dyadic links; the hypergraph format requires a custom adapter |
| **Tooling that already speaks InstaGraph** | `instagraph.json` | Native; no schema briefing needed |

## Why the rule of thumb works

The split is about **indirection tolerance**, not capability ceiling.

The hypergraph format encodes an n-ary edge once as a single object, then declares its members in a separate `incidences` array indexed by edge id. To reason about "what's in scene s1," an AI must: (1) find the edge with id `s1`, (2) scan `incidences` for entries with `edge: s1`, (3) collect the `node` ids, (4) look those up in `nodes`. Four steps, three of which are cross-references.

The dyadic format does that work upfront: every member of every n-ary edge already appears as its own row, with `source` (the edge-as-node), `target` (the member node), and a `layer` field naming the relationship type. To reason about scene s1, an AI filters links where `source == s1` and reads `target` directly. One step, no cross-reference.

A model with strong schema reasoning handles the four-step lookup without losing the thread. A model in the 7B-30B range tends to drop a step or conflate ids when the schema requires holding multiple lookup tables in working memory. The cost of dyadic flattening is loss of topological elegance — but for the AI consuming the file, the flatter form preserves *more* of the structure that gets used in answers.

## Schema briefings

Hand these verbatim to the AI before the data file. The briefing format matters: smaller models need flatter language, larger models can take richer schema explanations.

### For large-context models (hypergraph file)

> Nodes have `id` and `attrs`. `attrs['instagraph:type']` is the entity class (Paragraph, Character, Scene, Chapter, Act, Place, Theme). Paragraph nodes carry full prose in `attrs.text`. Edges are dyadic when arity is 2; n-ary edges are reified — look up `incidences` by edge id to find members and their roles. `attrs['i2t:predicate']` names the relationship; `attrs.label` carries a prose excerpt anchoring the edge to source.

### For smaller models (dyadic file)

> Each link has `source`, `target`, `label` (a prose excerpt). `source_role` and `target_role` give narrative function. `layer` names the relationship type — filter by `layer` to focus on one type at a time. Nodes have `id`, `kind`, `label`, `attrs`. Paragraph nodes have full prose in `attrs.text`.

### For tooling that needs no briefing (InstaGraph-native)

> Standard InstaGraph schema. Edges with `relationship` of `scene_contains`, `member_of_act`, etc. encode the n-ary structure as repeated dyadic edges sharing the same edge id prefix. Use the prefix to recover the n-ary group if needed.

## Operational notes

- **Token budget**: the Elinor files are ~880-984KB, roughly 200-250K tokens. Advanced models with 1M+ context handle the whole file. Models with 128K context can hold most of it but may need filtering for tight prompts. Smaller-context local models need the file sliced — usually filtering by `layer` (dyadic) or by chapter/act (either format).
- **Filtering by layer**: in the dyadic file, every link carries a `layer` field. Filter to one layer (e.g. `scene_contains`) for relationship-specific questions. The full file is the union of all layers.
- **Filtering by neighborhood**: for character-centric or scene-centric questions, run [`adapters/extract_neighborhood.py`](../adapters/extract_neighborhood.py) on the hypergraph file to get a k-hop subgraph, then convert to whichever format the collaborator wants.
- **Chained pipelines**: it is fine (and often correct) to give an advanced model the hypergraph file, have it produce a structured intermediate, and then hand that intermediate to a faster local model for bulk processing. Different models for different layers of the same task.

## Updating this doc

When you discover a new AI collaborator, a new format, or a constraint that changes the rule of thumb, add a row to the quick-reference table and (if the reasoning is non-obvious) a short paragraph explaining why. The point of the doc is that future sessions can read it and inherit the decisions, rather than rediscovering them. Date stamps not required — git history is the changelog.

## Related

- Canonical format spec: [`../hypergraph.topothink.spec.md`](../hypergraph.topothink.spec.md)
- Adapters that produce these formats: [`../adapters/README.md`](../adapters/README.md)
- Multilayer architecture (per-predicate layers as the loadable unit): see project memory
