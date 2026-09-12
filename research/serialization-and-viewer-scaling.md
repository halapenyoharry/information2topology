# Hypergraph Serialization and Viewer Scaling

**Date:** 2026-04-27
**Context:** Generated in response to three connected questions raised after the first run of `propgraph_to_hypergraph.py` produced a 15MB hypergraph file that broke the custom JSON viewer.

The questions:

1. Is JSON the right serialization for the TopoThink hypergraph?
2. Do hypergraphs / multigraphs necessarily create massive redundancy?
3. The viewer breaks or locks up on the large files we produced. How do we get efficient about how much data we ship to our systems? Cosmograph is one option — what else is on the table?

---

## Is JSON right?

Right at the **spec** layer (readable, universally parseable, debuggable; future-Claude can `cat` a hypergraph file and understand it). Wrong at the **wire** layer once size matters.

JSON's known efficiency problems all bite at scale:

- Keys are repeated strings on every object
- Numbers are decimal text, not native ints/floats
- Every wrapper is `{...}` overhead
- Parsed JSON in JS occupies 3–5× its serialized size in RAM

The 15MB hypergraph file probably explodes to 50–75MB in the viewer's heap before rendering even starts.

The architectural fix isn't to abandon JSON — it's to keep JSON as the **canonical** form and produce **wire formats** alongside it. Spec layer reads, wire layer ships.

## Do hypergraphs create massive redundancy?

No — the redundancy is a property of *this serialization*, not of the hypergraph data model. The model itself is information-theoretically tight:

- Simple graph: `|E|` edges of `(src, tgt)`
- Multigraph: `|E|` edges of `(src, tgt, label)`
- Hypergraph (dyadic case): `|E|` edges + `2|E|` incidences = `2|E|` `(src, role)` pairs — **the same as an adjacency list**

For dyadic data, the incidence model has zero structural overhead vs an edge list. What's bloating the file is the JSON wrapper around each row:

```json
{"edge":"edge:dirgraph/e1","node":"fs:/Users/harold/...","role":"source"}
```

That's ~120 bytes for what's really 2 integers + 1 enum.

So: the spec is fine, the data model is fine, the serialization for big data needs help.

## Three fixes, ordered by cost/benefit

### 1. Dictionary-encode the hypergraph

Pull all the repeated strings (node IDs, predicate names, role values) into a flat index, replace inline strings with integer references. Same logical content, still JSON, **~70% size reduction** on the current data because every `fs:/Users/harold/Projects/...` long path appears 3+ times right now (once as a node id, once in a source incidence, once in a target incidence).

A `compact` emitter for the hypergraph plus a matching loader is roughly 150 lines, no new dependencies. Filename convention: `*.hypergraph.topothink.compact.json`.

### 2. Binary JSON-superset (MessagePack or CBOR)

Drop-in replacements for JSON with the same logical model. Typical **30–50% smaller** plus **5–10× faster parsing**. Native libs in JS, Python, Rust, Swift.

Lower payoff than dictionary encoding for graph data specifically — because the redundancy here is in repeated keys, not in number encoding — but composes well on top of (1).

### 3. Emit CSV pairs (`nodes.csv` + `edges.csv`)

Lossy — drops attribute objects and reified edges — but Cosmograph, Gephi, Graphology+Sigma, and most GPU graph viewers want exactly this format. Typically **10–100× faster to load** than JSON because the parser is a `split(',')` rather than a recursive-descent parse.

## The right architecture for the project

The canonical TopoThink hypergraph file stays JSON — one source of truth. Each emitter (dictionary-compact, MessagePack, CSV-pair, JSON-LD, HIF) is a separate file in `adapters/` that produces a wire format from the canonical. The viewer chooses which wire format it consumes; the spec doesn't change.

## On Cosmograph and alternatives

Cosmograph is genuinely good for the size class we're hitting and above — it's WebGPU-native and handles millions of nodes by treating the layout as a GPU shader. Downsides: commercial / closed-source-ish for some features, and CSV-input means closed vocabulary at the column level.

Alternatives worth knowing about:

- **Sigma.js + Graphology** — open-source, WebGL, comfortably handles 100k nodes. Graphology is a JS multigraph library that maps cleanly to the TopoThink hypergraph format (first-class edges with IDs and attributes). Probably the best fit for continuing to build a custom viewer.
- **VivaGraph.js** — older but very fast WebGL force-directed.
- **Apache Arrow + custom WebGPU** — full control. Arrow is columnar binary, IPC-efficient, with JS bindings. Steeper to implement.
- **Cytoscape.js** — easier API but starts struggling above 10k nodes. Probably below the threshold needed here.

## Verify the bottleneck before optimizing

Before optimizing the wire format: **is the viewer's bottleneck actually data size, or rendering / layout?**

A 15k-node force-directed layout in vanilla D3 is `O(N²)` per tick and chokes regardless of how fast the data loaded. If the layout uses naive force-directed rather than a Barnes-Hut tree or GPU shader, the optimization target is the rendering loop, not the file format.

Profile before optimize. Knowing which side the problem is on changes the recommendation.

## Recommended next move

Write two emitters from the canonical TopoThink hypergraph:

1. **Dictionary-compact JSON emitter** — ~70% size reduction on existing files, still JSON, no new dependencies. Output: `*.hypergraph.topothink.compact.json`.
2. **CSV-pair emitter** — `nodes.csv` + `edges.csv` for Cosmograph-style viewers.

That produces two wire formats from one canonical source. Compare load times side by side in the viewer.
