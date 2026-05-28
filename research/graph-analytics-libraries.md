# Graph-Analytics Libraries: Why Not cuGraph (Yet), Alternatives at Current Scale, When Later

**Date:** 2026-05-03
**Status:** Project stance on adopting graph-analytics libraries. Resolves a question that came up while evaluating [rapidsai/cuGraph](https://github.com/rapidsai/cugraph).

---

The question this doc answers: which graph-analytics library should the i2t project add when (or if) it acquires analytics capabilities? The short answer is "none right now, NetworkX or igraph when the first analytics use case appears, HypergraphX if we want to honor the data model exactly, cuGraph only when scale demands it." This document explains the reasoning so future-self doesn't have to re-derive it.

## What cuGraph is and what it's good for

cuGraph is NVIDIA's GPU-accelerated graph analytics library, part of the RAPIDS ecosystem. It exposes classic graph algorithms — PageRank, Louvain community detection, betweenness centrality, BFS, SSSP, weakly/strongly connected components, K-truss, triangle counting — running on CUDA-capable GPUs via cuDF dataframes. NetworkX-compatible Python API. Scales to billions of edges across multi-GPU setups. Strong story for graph neural networks via cuGraph-DGL.

For the use cases it targets — large-scale graph analytics where the dataset doesn't fit comfortably in CPU memory, and where you need centrality / clustering / shortest-paths fast — it's genuinely state-of-the-art and not really competing with the CPU-based libraries below.

## Why not now

Three reasons, each independent.

**1. Scale.** Our largest fixture today is `data/ai-lumen.*` at ~15,644 nodes. cuGraph's value kicks in at 10⁶–10⁹ edges where GPU parallelism dominates host RAM/CPU. Below ~100k nodes, GPU memory transfer + kernel-launch overhead eats the win. NetworkX is comfortable to ~50k; igraph and graph-tool reach 1M+ on CPU. The project hits cuGraph's win zone only if it grows by 100× or more.

**2. cuGraph is dyadic-only.** Its `PropertyGraph` wraps `(src, dst)` edges with attributes; it has no native hypergraph primitive. Our format's reified edges, n-ary hyperedges, and incidence role pairs would have to flatten through `adapters/hypergraph_to_dyadic.py` first — which is fine, we already do that — but you'd be analyzing the *dyadic projection*, not the hypergraph. Centrality on the dyadic projection of a hypergraph isn't centrality on the hypergraph; it's centrality on a specific projection of it. The numbers come out, but they may not mean what someone reading them assumes.

**3. The project's bottleneck isn't analytics.** It's faithful representation (the editorial discipline) and perception (the visualization layer). Adding graph algorithms doesn't make any current task faster or any current rendering better. RAPIDS is a heavyweight install (CUDA toolchain + cuDF + cuGraph + version-pinning across that stack) that doesn't pay back until there's an analytics use case to justify it. There isn't one yet.

## Alternatives at current scale

| Library | Scale comfort | Native model | Install weight | Fit |
|---|---|---|---|---|
| **NetworkX** | up to ~50k nodes | dyadic + multigraph | pure Python, zero pain | The right first analytics move. Has every classic algorithm; readable code; nothing to install beyond `pip install networkx`. |
| **igraph (Python)** | 100k – 1M | dyadic + multigraph | C-backed wheel | ~10–100× faster than NetworkX on the same algorithms. Solid mid-scale option. |
| **graph-tool** | similar to igraph; sometimes faster | dyadic | C++ wheel; heavier install (Boost) | Fastest CPU library most of the time. Worth it if you're doing many runs on graphs in the 100k–10M range. |
| **HypergraphX** | smaller scales; pure Python | **incidence-based hypergraphs** | `pip install hypergraphx` | The only entry that natively models what our format actually represents. Section below. |
| **Graphology** | already in JVV's stack | dyadic + multigraph | npm | If analytics belong on the rendering side, JVV already has it. |
| **cuGraph** | 10⁶+ edges | dyadic | RAPIDS stack; needs CUDA GPU | Right tool for the wrong scale right now. |

## HypergraphX as the underrated fit

HypergraphX is a Python library for incidence-based hypergraphs. Unlike everything else on the list, it doesn't require us to project to dyadic before analyzing — its primitives are nodes, hyperedges of arbitrary arity, and incidences. It supports temporal hypergraphs, multilayer hypergraphs, and includes algorithms for hyperedge centrality, hypergraph community detection, and motif counting that are formulated *natively* on hyperedges, not on a projection.

The trade is community size and scale ceiling. HypergraphX has fewer contributors and fewer algorithms than NetworkX or igraph; it's pure Python so it doesn't reach igraph's speed on equivalent graphs.

For this project the structural alignment is unique. If we want to compute "how central is this character across all the case-event hyperedges in *Wretched of the Earth*" without flattening Fanon's case-events into pairwise edges first, HypergraphX is the only library that gives a first-class answer. For "what does this hypergraph look like topologically without lossy projection," same.

It's worth a serious look the first time we want analytics that actually depend on hypergraph structure (rather than just summary statistics over the projection).

## When cuGraph would earn its keep

Concrete future conditions, any one of which would justify the install:

- Ingesting an entire bookshelf, codebase, or wiki dump and producing a graph of 10⁶+ edges
- Cross-corpus federation where merged hypergraphs cross 10⁵ nodes (per the multilayer-network principle, federation is the natural pressure on scale)
- Repeated analytics passes (recompute community structure on every ingestion, recompute centrality nightly) where CPU latency becomes the bottleneck
- Graph-neural-network experiments — embedding nodes for similarity search, link prediction, GNN-based completion of partial graphs. cuGraph-DGL is the right path for these.
- An interactive analytics layer in the viewer: "show me all paragraphs within K hops of these tagged nodes, weighted by something" needs to be sub-second over a large corpus.

None of those are pressing. They're all plausible 6–24 month directions if the project continues to scale outward.

## Architectural note: canonical-format-plus-emitters keeps this cheap

The reason this document can recommend "later" without anxiety is that the project's architecture already treats external libraries as emitter targets. The canonical hypergraph format is the truth; everything beyond it is a seam.

`adapters/hypergraph_to_dyadic.py` is the existing pattern: take the canonical hypergraph, project it to a different consumer's expected shape (in that case, the `{nodes, links}` shape JVV accepts). Adding NetworkX, igraph, graph-tool, HypergraphX, or cuGraph is the same move repeated:

- `hypergraph_to_networkx.py` — `pip install networkx`, build a `nx.MultiDiGraph`, return it
- `hypergraph_to_igraph.py` — same shape, different library
- `hypergraph_to_hypergraphx.py` — preserves the hypergraph structure exactly
- `hypergraph_to_cugraph.py` — only when the install cost is justified

Each emitter is small (50–150 lines), decoupled from the others, opt-in by import (no library is loaded unless that emitter runs). The canonical format never has to know which analytics layer it's flowing into. The choice of "do we want analytics now" is independent of "if we do, which library" — and both are independent of the schema and the editorial discipline.

This is also why "later" doesn't feel like deferred work. It's deferred *cost*. The architecture is already shaped for it.

## Recommended next step (when an analytics use case appears)

Build `adapters/hypergraph_to_networkx.py` first. Reasons:

1. NetworkX is in every Python install path; zero infrastructure
2. Every graph algorithm in the standard analytics vocabulary (PageRank, centrality, community detection, shortest paths) is one function call away
3. It gives us a real test of whether analytics on the dyadic projection of our hypergraphs is meaningful, before committing to anything heavier
4. If results suggest we're losing too much in the projection, that's the trigger to look at HypergraphX as the next emitter — and it's a small follow-up, not a rewrite

The first concrete analytics question worth asking on i2t graphs is probably **"what's the centrality distribution of paragraph-nodes across the manuscript, weighted by `mentions` edges?"** — i.e., which paragraphs structurally anchor the most cross-references? That maps cleanly to a NetworkX one-liner over the dyadic projection. If the answer is interesting, we have a use case. If it isn't, we don't, and we've spent ~100 lines of code to learn that.

cuGraph stays on the radar but off the path until scale demands it. The architecture means that's a one-day add when the day comes.
