# Adapters

Each script in this directory reads one data format and writes another. They are the seams between the canonical TopoThink hypergraph (the project's internal lingua franca) and everything outside it.

Most scripts are stand-alone Python 3 with no third-party dependencies. The one exception is `text_to_hypergraph_via_llm.py`, which requires the `anthropic` SDK and an `ANTHROPIC_API_KEY`. Run any adapter with `--help` for the exact CLI.

For guidance on which output format to hand to which AI collaborator (Claude vs Gemma vs visualization tooling), see [`../docs/ai-collaborator-format-guide.md`](../docs/ai-collaborator-format-guide.md).

## File taxonomy: source / canonical / projection

Every file the project produces or consumes sits in one of three classes relative to the canonical TopoThink hypergraph:

- **Source** — flows *into* canonical. Anything an ingest adapter reads: raw text, InstaGraph JSON extractions, property-graph JSON, manuscript markdown, home-network JSON. Loses information at ingest (normalized into incidences, predicate naming standardized, etc.).
- **Canonical** — the lingua franca. `*.hypergraph.topothink.json` files validated by [`../hypergraph.topothink.schema.json`](../hypergraph.topothink.schema.json). The format every adapter writes to or reads from.
- **Projection** — flows *out of* canonical. Anything an emit / transform adapter writes: normalized-dyadic JSON, predicate-layer files, k-hop sub-hypergraphs, future JGF / HIF / RDF emissions. Loses information at emit (arity ≠ 2 collapses in JGF; n-ary edges reify in dyadic; etc.).

Direction matters. A source and a projection are both *non-canonical* but related to canonical in opposite directions. The asymmetry is in the data, not in the file type.

**Special case — predicate-layer files** (`*.layer-PREDICATE.hypergraph.topothink.json`) are both canonical AND projection. Each one passes the canonical schema and round-trips losslessly with merge-by-id; collectively they're a projection of one parent hypergraph by predicate. The dual citizenship is what the multilayer-network architecture means.

To make a file self-describe its class, projection adapters write an **`i2t:relation_to_canonical`** key into the file's `metadata` block:

| Value | Used by | Meaning |
|---|---|---|
| `dyadic-projection` | `hypergraph_to_dyadic.py` | Output of dyadic flattening; every n-ary edge reified as edge-as-node plus per-incidence dyadic links |
| `predicate-layer` | `split_by_predicate.py` | One layer of a parent hypergraph; valid canonical hypergraph in its own right |
| `k-hop-neighborhood` | `extract_neighborhood.py` | Sub-hypergraph centered on anchor nodes; valid canonical hypergraph |
| *(absent)* | canonical files | A file with no `i2t:relation_to_canonical` IS canonical; absence is the signal |

Future projection adapters should pick a value and add a row above. Source files generally aren't under project control and don't carry this key; if a source adapter wants to mark its intermediate output, `extraction-intermediate` is reserved for that use.

## Pipeline shape

```
external source                canonical                  external target
─────────────────────────────────────────────────────────────────────────
unstructured text  ──┐
(any prose)          │ via LLM (text_to_hypergraph_via_llm.py)
                     │ — or paste the prompt template into Claude.ai
                     │
property-graph JSON  ─┤
(dirgraph/ghgraph)    │
                      ├─►  TopoThink hypergraph  ─►  normalized-dyadic JSON
InstaGraph JSON  ─────┤    (*.hypergraph.                (*.normalized-
(yoheinakajima        │     topothink.json)               dyadic.json)
 schema)              │           │                       — for D3, Cytoscape,
                      │           │                         react-force-graph,
                      │           ├─►  per-predicate           etc.
                      │           │     layers
home-network JSON  ──┤           │     (split_by_predicate.py)
novel manuscript ────┤           │
                      │           └─►  K-hop neighborhood
                      │                 sub-hypergraph
[future ingestors] ──┘                 (extract_neighborhood.py)
```

The canonical format is described in [`../hypergraph.topothink.spec.md`](../hypergraph.topothink.spec.md). Anything in the project either produces the canonical format (ingest adapters) or consumes it (transform / emit adapters).

## Unified BYO-AI Ingest CLI

### `i2t_cli.py`

**The modern unified extractor** (OpenRouter / Gemini / BYO CLI). Ingests raw text, classifies relational joints into the 4 TopoThink categories (`containment`, `state_change`, `interactivity`, `reference`), validates against the schema, saves the canonical hypergraph, and emits the Exoskeleton dyadic projection in a single step.

**Setup**:
Keys are automatically read from `~/.config/ai/keys.env` or standard environment variables (`OPENROUTER_KEY_INFO2TOPO`, `OPENROUTER_API_KEY`, or `GEMINI_API_KEY`). Default model is **`google/gemini-2.5-flash`** (~$0.0004 / run).

**Usage**:
```bash
# Sourced automatically from keys.env
source ~/.config/ai/keys.env

# Standard extraction (Canon + Exoskeleton Projection)
python3 i2t_cli.py extract data/raw/source.txt \
  --out data/canonical/source.hypergraph.topothink.json \
  --project
```

---

## Ingest from unstructured text (legacy Anthropic SDK path)

### `text_to_hypergraph_via_llm.py`

**Reads** any source text (essay, novel chapter, Wikipedia article, paper section, song lyric — anything in prose).

**Writes** an InstaGraph-with-i2t-extensions JSON file. Chain through `instagraph_to_hypergraph.py` for canonical-format and `hypergraph_to_dyadic.py` for the JVV-loadable form.

**How it works**: sends the source text to Claude (default `claude-opus-4-7`) along with the prompt template at [`../prompts/text_to_topothink_hypergraph.md`](../prompts/text_to_topothink_hypergraph.md). The prompt is the editorial-discipline rules and worked examples; the LLM produces a graph following them.

**Key conventions** (encoded in the prompt template, see [`../research/editorial-discipline.md`](../research/editorial-discipline.md)):
- Every edge carries a `label` containing **a text excerpt from the source** that justifies the edge — not a category name, not a paraphrase.
- Edge `relationship` is the categorical predicate (`speaker_of`, `cites`, `member_of`); the text evidence is the edge's identity.
- Incidence roles describe how each endpoint participates (`predecessor`/`successor`, `voice_carrier`/`speaker`, etc.).

**Setup**:
```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
```

**Usage**:
```bash
python3 adapters/text_to_hypergraph_via_llm.py source.txt -o out.instagraph.json
python3 adapters/instagraph_to_hypergraph.py out.instagraph.json
python3 adapters/hypergraph_to_dyadic.py out.hypergraph.topothink.json
```

**Cost transparency**: prints input / output / cached token counts and an estimated USD cost after each call. Default `claude-opus-4-7` is highest quality; pass `--model claude-sonnet-4-6` for ~5× cheaper extractions of similar shape (often sufficient).

**Prompt caching**: the system prompt (~14K chars) is cached with `cache_control: ephemeral`. Re-running on different sources within ~5 minutes pays only the cache-read cost for the prompt portion (~10× cheaper than re-uploading).

**Single-pass for now**: texts up to ~150K chars work in one call. Larger sources need to be chunked manually (split by chapter / section, run separately, merge by node ID).

### Without the API: paste-into-any-LLM path

If you don't want to set up the SDK, just open [`../prompts/text_to_topothink_hypergraph.md`](../prompts/text_to_topothink_hypergraph.md), paste the whole prompt into Claude.ai (or GPT, Gemini, any reasoning-capable LLM), then paste your source text after it. The LLM returns InstaGraph-with-extensions JSON. Save it, run `instagraph_to_hypergraph.py` and `hypergraph_to_dyadic.py` on it. Same pipeline, no API integration needed.

## Public sample fixtures

Worked examples in [`../data/`](../data/) demonstrating the full pipeline. Each comes in three forms: `.instagraph.json` (raw extraction), `.hypergraph.topothink.json` (canonical), and `.normalized-dyadic.json` (JVV-loadable).

| Fixture | Source | Shape | Notes |
|---|---|---|---|
| `myth-of-sisyphus.*` | Camus, *The Myth of Sisyphus* (1942) | 52 nodes / 82 edges / 164 incidences | Public-domain philosophy; Claude-direct extraction without reification or hyperedges. The cleanest baseline. |
| `wretched-of-the-earth.*` | Fanon, *The Wretched of the Earth* (1961) | 82 / 111 / 240 | Public-domain post-colonial theory; uses reification (the four case-event hyperedges + algerian_war + fanon_death) and rich incidence attrs. |
| `wizard-of-oz.*` | Baum, *The Wonderful Wizard of Oz* (1900); Project Gutenberg #55 | 1,203 / 1,208 / 3,532 | Public-domain fantasy; **two-layer fixture**: paragraph-as-node (1,118 paragraphs with full prose in `attrs.text`) **plus** entity layer (10 characters + 4 witches + 3 animated characters + 6 collectives + 12 places + 10 items + 6 themes + 7 reified narrative events). Three-act split (Act 1: ch 1-7 / Act 2: ch 8-13 / Act 3: ch 14-24) with reified chapter and act hyperedges. Demonstrates the architecture's two-layer claim concretely — the paragraph layer carries the actual book; the entity layer is the structural index over it. The paragraph-as-node convention (text in node attrs, slug as label hint only) is the same as the manuscript fixture. The 7 reified events (cyclone, killing-of-East-witch, wizard-appearing-differently, melting-of-West-witch, the unmasking, balloon departure, homecoming) carry role-rich incidences. |
| `wizard-of-oz-entities-only.instagraph.json` | Same source | 58 / 63 / 154 | The earlier entity-only extraction, retained for the register-comparison finding. Documents the entity/event distribution at extraction time without the paragraph layer. |
| `tics-and-topology-conversation.*` | Conversation between a user and Claude (claude.ai web, 2026-05-03), about Claude's recurring conversational tics, training-substrate causes, and the editorial-discipline architecture | 36 / 60 / 130 | **Recursive example:** graph of a conversation about the editorial discipline, made by following the editorial discipline. Every edge label is a quote from the conversation; reified entities (`the_jab`, `the_recognition_arc`) capture multi-turn patterns. Personal identifiers redacted. |

`tics-and-topology-conversation` is the existence proof that the prompt-template approach (without the SDK adapter) produces graphs of the same shape as the manually-extracted Camus / Fanon / Oz corpora. It was generated by claude.ai web pasted into the prompt; same output shape, no API integration needed.

**Register-comparison finding** (visible across the four fixtures): the format adapts honestly to register. Philosophy → concept-heavy, low reification (Camus). Political theory → balanced concept/event with rich case-study reification (Fanon). Fantasy → event-heavy, low concept (Oz). Meta-conversation → turn-pair-heavy with multi-turn arc reification (tics). Same schema, same editorial discipline; the resulting graph's *shape* is itself a measurement of what the source is.

---

## Ingest adapters (write the canonical format)

### `propgraph_to_hypergraph.py`

**Reads** property-graph JSON in the dirgraph / ghgraph / merged shape used by `~/Projects/github-graphing-thing` (`{meta, nodes:[{id, properties}], edges:[{id, source, target, label, properties}]}`).

**Writes** a TopoThink hypergraph (`*.hypergraph.topothink.json`).

**Key transformations**:
- Node property keys are prefixed with the URI scheme of the node ID (`fs:` properties → `fs:path`, `fs:name`; `gh:` → `gh:url`, etc.) so cross-source merges stay unambiguous.
- Edge `label` becomes `attrs["i2t:predicate"]`.
- Edge IDs are positional indexes (`edge:<tool>/<index>`) — the source's bare edge IDs may collide across pre-merged sources; the original ID is preserved in `attrs["i2t:original-id"]`.

### `instagraph_to_hypergraph.py`

**Reads** JSON in the schema used by [yoheinakajima/instagraph](https://github.com/yoheinakajima/instagraph) and any extractor following that convention (`{metadata, nodes:[{id, label, type, color, properties}], edges:[{from, to, relationship, direction, color, properties}]}`).

**Writes** a TopoThink hypergraph.

**Key transformations**:
- Node `label` / `type` / `color` flow into `attrs` (with `instagraph:` prefixing on `type` / `color` for provenance).
- Edge `relationship` becomes `attrs["i2t:predicate"]` so all downstream tooling sees the predicate in the same place.
- Edge `direction == "directed"` (the default) sets `directed: true`; one source-role and one target-role incidence per edge.
- Edge IDs default to positional namespace `edge:instagraph/<index>`.

**Two backward-compatible extensions** for richer extractions that need to exercise the hypergraph format more fully:

1. **Hyperedges (n-ary).** An edge MAY use `members` instead of `from`/`to`:
   ```json
   {"members": [
       {"node": "alice",   "role": "subject"},
       {"node": "bob",     "role": "object"},
       {"node": "tuesday", "role": "time"}
    ],
    "relationship": "Mary_kissed_John_on_Tuesday"}
   ```
   `members` accepts either bare node-id strings (role defaults to `member`) or `{node, role, attrs}` objects. Each member produces one incidence on the resulting edge.

2. **Reified edges.** An edge MAY include an explicit `id` field. When the same id ALSO appears as a node id in the same input file, the edge is reified — the same id appears in both the output's `nodes` and `edges` lists, per spec rule S4. Other edges can then refer to it as a node.

Vanilla InstaGraph files (no `members`, no edge `id`) still convert as before. The Camus fixture uses the vanilla path; the Wretched fixture uses both extensions.

### `network_to_hypergraph.py`

**Reads** Harry's home-network JSON (`{_meta, subnets:{cidr → {media, router, notes}}, routing:{name → {hops, status, ...}}, computers:{name → {network, type, services, ...}}}`).

**Writes** a TopoThink hypergraph.

**Framing chosen** (the picker-equivalent, hard-coded for this source shape):
- **V** = computers
- **E** = subnet membership (one hyperedge per subnet, connecting all hosts on it) and named routes (one reified hyperedge per route)
- **I** = how each entity participates — interface, IP, gateway, MTU, role (`member` / `router` / `source_host` / `destination_host`)
- **attrs** = everything else (config, os, services, hops, verification facts, notes)

**Reification policy:**
- *Routes* are reified — their id appears in both `nodes` and `edges`. They earn it because they have rich own-attrs (verification dicts, latency, hops) and other entities can plausibly assert facts about them.
- *Subnets* are NOT reified — they appear only in `edges`. They have own-attrs (media, router, notes) but nothing in the data points AT them; they're the medium through which hosts connect, not first-class objects of assertion. Subnet refs in routes ride as `attrs.subnets_involved` and `incidence.attrs.destination_subnet`, not as separate participants.

**Render hints** travel on the edge:
- Subnet edges carry `render_hint: "container"` — drawn as Venn-style enclosing regions for renderers that support it (multi-subnet hosts become overlapping-region members). Arity-2 subnets stay as plain dyadic links in the dyadic projection per the standard rule.
- Route edges carry `render_hint: "line"` — drawn as a directed path through the participating hosts.

Hosts with all-null IPs (laptops not yet attached) appear as isolated vertices — faithful to the data; they participate in zero edges.

This adapter is shape-specific to `data/private/network.json` and would need to be replaced (or generalized into a declarative framing spec) for other network-shape sources.

---

## Transform adapter (canonical → canonical)

### `split_by_predicate.py`

**Reads** a TopoThink hypergraph.

**Writes** one TopoThink hypergraph file per `i2t:predicate` value, named `<stem>.layer-<predicate>.hypergraph.topothink.json`.

**Why**: a single hypergraph file is the canonical superposition of distinct topological layers, one per relation type. Each per-layer file is itself a valid hypergraph; merging any subset of them by node-ID losslessly reconstructs the layered topology of those predicates. See [`memory/multilayer_architecture.md`](../../../.claude/projects/-Users-harold-Projects-information2topology/memory/multilayer_architecture.md) for the principle behind this.

### `extract_neighborhood.py`

**Reads** a TopoThink hypergraph plus an anchor specification (predicate, ID-prefix, or explicit ID list).

**Writes** a sub-hypergraph containing every node within K hops of any anchor, plus every edge whose endpoints all lie inside the kept node set, plus their incidences.

**Why**: large hypergraphs need slicing for visualization and analysis. The K-hop neighborhood preserves the local topology around a semantically meaningful seed (e.g., "everything within 1 hop of any node touched by a `mirrors` edge").

---

## Emit adapter (canonical → external)

### `hypergraph_to_dyadic.py`

**Reads** a TopoThink hypergraph.

**Writes** a `*.normalized-dyadic.json` file with shape `{metadata, nodes:[{id, label, kind, attrs}], links:[{source, target, label, directed, role, layer, attrs}]}` — consumable by general-purpose dyadic graph viewers (D3 force-directed, Cytoscape.js, react-force-graph, Sigma.js, etc.) without format-specific knowledge.

**Projection rules**:
- **Arity-2 edges that are NOT reified** → one plain dyadic link, attrs ride on the link.
- **Arity-≥-3 edges OR reified edges** → a synthetic node (`kind: "hyperedge"` for pure hyperedges, `kind: "edge-as-node"` for reified) plus one dyadic link per incidence. Link direction follows incidence role.
- **Predicate** (from `attrs["i2t:predicate"]` with fallbacks `predicate`, `relation`, `type`, `label`) populates both `link.label` and `link.layer` so consumers can use either independently.
- **Role** on incidences passes through verbatim.

**Output `metadata`** carries `i2t:relation_to_canonical: dyadic-projection` so consumers can recognize the file's class without inferring from filename. The synthetic node per arity-≥-3 edge is a *schema artifact* (the dyadic schema can only address relations by making them addressable as nodes), not an ontological entity — see [`../.claude/projects/-Users-harold-Projects-information2topology/memory/feedback_avoid_reification_triggers.md`](../.claude/projects/-Users-harold-Projects-information2topology/memory/feedback_avoid_reification_triggers.md) for why geometry metaphors ("star", "hub", "spoke") are avoided in describing this projection.

**The schema this targets is the `NormalizedGraph` shape negotiated with the json-visual-viewer in [`../correspondence/json-visual-viewer.md`](../correspondence/json-visual-viewer.md).** Any other dyadic viewer that wants a similar shape can consume the same files.

---

## Adding a new adapter

The convention: one external format = one adapter file. Name it `<source>_to_<target>.py`. Match the existing argparse / stdout-summary style. Add an entry above. If it's an ingest adapter, write directly to `*.hypergraph.topothink.json` so it composes with the rest of the chain.
