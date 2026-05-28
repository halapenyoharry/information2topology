# Decomposition, Rendering, and the Shape of What's Next

**Status**: Working paper. Captures the state of thinking and technology as of 2026-05-10.
**Context**: Conversation between Harold Young and Claude (Opus 4.6) exploring the universal schema question, the rendering problem, and the relationship between hypergraph decomposition and human visual cognition.

---

## Where We Are

The information2topology project has a working canonical format (`hypergraph.topothink.json`), a formal spec, a JSON Schema, and a pipeline of adapters that ingest property graphs, InstaGraph JSON, home-network JSON, unstructured text via LLM, and manuscripts. The format commits to three structural primitives (nodes, edges, incidences) and zero vocabulary constraints. Edges can connect any number of nodes. Edges can be nodes (reification). Incidences can be nodes. Merge-by-id enables federation across files.

The format is already universal in the structural sense. It handles network topology, novels, philosophy, post-colonial theory, conversations, and GitHub project structures without modification. The universality comes from the asymmetry: one structural commitment, zero vocabulary commitments.

The json-visual-viewer (JVV) renders the format in six views (Tree, Graph, Cytoscape, 3D Graph, Circles, Mass) via a normalized-dyadic projection. The correspondence protocol between the two projects is documented, and the layer toggle (v0.1.4) already enables per-predicate visibility switching.

The normalized-dyadic projection is lossy. Hyperedges of arity ≥ 3 are each reified as a synthetic node with one dyadic link per member. Reified edges are promoted to synthetic nodes. The loss is a transduction tax imposed by the rendering substrate: every visualization library in common use (D3, Cytoscape.js, Sigma.js, react-force-graph, three.js graph renderers) models edges as line segments between exactly two endpoints. This is a convention inherited from Euler's 1736 drawing of the Königsberg bridges, not a mathematical necessity.

---

## The Rendering Problem

The entire force-directed layout algorithm is built on the assumption that every edge is a spring between two point masses (vertices), with attraction and repulsion calculated between pairs. The physics simulation is dyadic. When a relationship connects three or more entities, the renderer has no primitive to express it. The available hacks are clique expansion (draw all pairs, losing the unity of the fact and creating O(k²) false edges) or dyadic projection (reify each hyperedge as a synthetic node with one dyadic link per member, preserving unity but introducing a non-existent entity).

There is no mathematical reason this has to be true. A hyperedge could be rendered as a region, a convex hull, a gradient field, a shared color, a container, a membrane. The dyadic constraint is an artifact of the rendering primitive, not of the topology.

### Existing non-dyadic renderers

The field is not empty. Several tools already render hyperedges as regions rather than line pairs:

- **HyperNetX** (PNNL, open-source Python): renders hyperedges as Euler diagram regions, convex hulls drawn around member nodes. Force-directed layout of the underlying bipartite representation positions the nodes, then hulls are computed. Users can move and pin nodes. Over 630 GitHub stars as of August 2025. (Praggastis et al., 2023)

- **HyperGodot** (Ficsor, Czvetko, Sebestyén, Abonyi, 2025): built in the Godot game engine (C++/GDScript). Chose a game engine over web-based tools specifically because real-time physics-based layout recalculation becomes a bottleneck in browser JavaScript. Renders hyperedges as convex hulls using Andrew's monotone chain algorithm. Supports force-directed and circular layouts, group comparison, vertex isolation on selection. Published in SoftwareX, August 2025.

- **XGI** (CompleX Group Interactions, open-source Python): provides both convex-hull rendering (`hull=True`) and multilayer visualization where each layer contains hyperedges of a given order. Edges colored by order by default. (Landry et al.)

- **HAT-VIS** (MATLAB-based): hypergraph analysis toolbox with visualization.

- **hypergraphx (HGX)** (open-source Python): analysis of higher-order networks with visualization support.

HyperGodot is the most structurally interesting precedent for TopoLand. The authors' reasoning for choosing a game engine matches the TopoLand instinct exactly: game engines handle real-time physics, interactivity, and rendering at a level that web-based tools cannot match for this class of problem.

---

## Decomposition: The Other Things Beyond Planarity

The `split_by_predicate.py` adapter performs the most basic decomposition: group edges by predicate type, produce one valid hypergraph per predicate. This is the foundational operation in multilayer network science, formalized by De Domenico, Solé-Ribalta, Cozzo, Kivelä, Moreno, Porter, Gómez, and Arenas in "Mathematical Formulation of Multilayer Networks" (Physical Review X, 2013). Their tensor-algebraic framework treats a complex network with multiple relationship types as a stack of layers, one per relationship type, with inter-layer connections where the same node appears across layers.

The predicate split is mechanical: the data already tells you how to slice because the predicates are labeled. But there are other decompositions where the structure itself reveals the natural slices, even when nobody labeled anything. These are the "other things" beyond planarity.

### Planarity

A planar graph can be drawn on a flat surface with no edge crossings. Many per-predicate layers extracted from a real hypergraph are close to planar or actually planar, because removing most edge types removes most crossings. Planarity is one kind of low-dimensional regularity, the kind where a 2D surface suffices without distortion.

### k-Core decomposition

Recursively remove all vertices with fewer than k connections until every remaining vertex has at least k connections. The result is a nested sequence of increasingly dense, increasingly central subgraphs: the 1-core is the whole graph, the 2-core strips away the periphery, the 3-core strips further, and so on until you reach the densest, most connected core. The nesting is the key property: k-cores are like onion layers, and the core number of each vertex tells you how deep it sits. This decomposition reveals the hierarchical density structure of the graph without any labeled categories.

The k-core decomposition was introduced by Seidman (1983) and has become a standard operation in graph mining. It runs in linear time (Batagelj and Zaversnik, 2003), making it practical for large graphs. Alvarez-Hamelin et al. (2005) demonstrated its use as a visualization tool, showing that it reveals "network fingerprints" that distinguish graphs with seemingly similar global properties.

### Community detection

Identify densely connected subgroups with sparse connections between them. Unlike k-core (which finds nested shells), community detection finds lateral clusters, regions of the graph that are more connected internally than they are to the rest. Many algorithms exist: modularity optimization (Newman, 2006), the Louvain method (Blondel et al., 2008), spectral clustering, stochastic block models, label propagation. Each makes different assumptions about what a "community" is, which is why there's no single canonical algorithm. Schaub et al. (2017) provided a taxonomy of the different motivations behind community detection, arguing that the choice of algorithm should depend on what you're trying to learn, not on which one is "best."

### Connected components

The simplest decomposition: which parts of the graph can reach each other? A connected component is a maximal set of nodes where every node can reach every other node via some path. If the graph has multiple connected components, they are completely separate topologies, islands with no bridges between them. Identifying them is the first thing you do because it tells you whether you're looking at one system or several.

### Bipartite structure

A bipartite graph has two groups of nodes where edges only connect nodes in different groups, never within the same group. Author-paper networks are bipartite (authors connect to papers, never author-to-author or paper-to-paper directly). Detecting bipartite structure reveals a fundamental asymmetry in the relationships: there are two kinds of things, and the edges always cross between kinds.

### Trees and spanning trees

A tree is a connected graph with no cycles, the simplest possible connected structure. Any connected graph has spanning trees, subgraphs that connect all nodes with the minimum number of edges and no loops. Extracting a spanning tree from a dense graph reveals the backbone, the minimal structure that maintains connectivity. The edges removed to get from the full graph to the spanning tree are the "extra" connections, the ones that create cycles, redundancy, and alternative paths.

### Simplicial complexes and higher-order structure

This is where the math gets closest to what Harold intuited about "finding the planar topologies within the hypergraph." A simplicial complex generalizes a graph to higher dimensions: nodes are 0-simplices, edges are 1-simplices, triangles are 2-simplices, tetrahedra are 3-simplices, and so on. A hypergraph can be represented as a simplicial complex, and the tools of algebraic topology (homology groups, Betti numbers) then tell you about the "holes" at each dimension.

The 0th Betti number counts connected components (how many separate pieces). The 1st Betti number counts independent cycles (loops that don't bound a filled-in triangle). The 2nd Betti number counts voids (enclosed cavities). Each Betti number is a different kind of "hole" at a different dimensional scale, and together they form the topological signature of the structure.

Topological Data Analysis (TDA) uses persistent homology to compute these signatures across multiple scales, revealing which topological features persist (are real structure) and which are noise.

### Spectral decomposition

The eigenvalues and eigenvectors of a graph's adjacency matrix (or Laplacian matrix) reveal structural properties that are not visible from local inspection. The second-smallest eigenvalue of the Laplacian (the Fiedler value) measures how well-connected the graph is, and the corresponding eigenvector (the Fiedler vector) provides a natural bisection, splitting the graph into two parts with minimum edge-cutting. Higher eigenvectors reveal finer-grained structural divisions. Spectral methods are the mathematical backbone of many clustering and layout algorithms.

---

## The Planar Intuition, Restated

Harold's intuition: a hypergraph contains multiple natural low-dimensional substructures, and the skill (human or machine) is finding which decompositions are structurally natural rather than arbitrary. The current rendering problem is that tools project the entire high-dimensional object down to 2D in one shot, superimposing all relationship types, all densities, all structural levels, producing noise where there should be signal.

The solution is not one decomposition but a toolkit of decompositions, each revealing a different structural property:

| Decomposition | What it reveals | Analogy to architectural drawing |
|---|---|---|
| Predicate split | Layers by relationship type | Separate sheets for electrical, plumbing, structural |
| k-Core | Density hierarchy, center vs periphery | Section cut showing foundation depth |
| Community detection | Lateral clusters, neighborhoods | Floor plan showing rooms |
| Connected components | Separate systems | Separate buildings on the same site |
| Bipartite detection | Two-kind structure | Distinction between load-bearing walls and partition walls |
| Spanning tree | Minimal backbone | Structural frame without cladding |
| Simplicial / homology | Holes at each dimension | Identifying atriums, courtyards, voids |
| Spectral | Natural bisections, embedding coordinates | Finding the axis of symmetry |

Each decomposition is an unfuzzballer. Each takes a complex, high-dimensional structure and produces a lower-dimensional view that is honest, structurally meaningful, and comprehensible to a human eye. The full topology is the stack of all views.

The connection to art: an architect does not draw one picture of a building. They draw plans, sections, elevations, details, each a different decomposition of the same 3D object onto a 2D surface. The skill is knowing which drawing to pull for which question. The untrained hand finds a natural projection because it isn't overriding its own structural perception with a theory about what the drawing should look like. The trained-but-rigid hand forces a projection. The best artists hold the full dimensionality in peripheral awareness and let the right collapse point emerge.

The connection to the TopoThink framework: each decomposition is a measurement (Chapter 6). Measurement selects one view from a superposition and discards the rest. A good measurement is negentropic: it selects the view that maximally increases local order, that makes the most structure visible. A bad measurement is premature collapse: it forces a projection before the topology is clear, destroying information that cannot be recovered. The rendering problem is a measurement problem.

---

## What Exists, What Doesn't, What's Next

**Exists:**
- The universal hypergraph format (topothink spec + schema + adapters)
- Predicate-split decomposition (`split_by_predicate.py`)
- Neighborhood extraction (`extract_neighborhood.py`)
- Six-view rendering in JVV with layer toggle
- HyperGodot as proof that game engines are the right substrate for hypergraph rendering
- XGI, HyperNetX, and others as proof that convex-hull region rendering works for hyperedges

**Doesn't exist yet:**
- k-core, community detection, bipartite detection, spectral decomposition adapters for the topothink format
- A renderer that consumes the hypergraph directly without dyadic projection
- A renderer that uses different visual primitives for different edge types (regions for containment, paths for sequence, arcs for reference)
- TopoLand: a renderer where edge predicates map to physics parameters (gravity, wind, proximity, repulsion) rather than to line styles
- The training loop: humans finding natural decompositions across enough topologies that the pattern becomes trainable for AI

**Next steps (suggested, not prescribed):**
1. Add k-core decomposition as a transform adapter (`kcore_decomposition.py`), since it runs in linear time and produces immediately useful nested-density views
2. Investigate whether JVV's existing layer toggle could support decomposition-as-layers (each k-core shell as a toggleable layer, each community as a toggleable layer)
3. Study HyperGodot's architecture as prior art for a Godot-based topology navigator
4. Hold the TopoLand vision open without premature collapse into implementation

---

## References

- Alvarez-Hamelin, J. I., Dall'Asta, L., Barrat, A., & Vespignani, A. (2005). "k-core decomposition: a tool for the visualization of large scale networks." arXiv:cs/0504107.
- Batagelj, V., & Zaversnik, M. (2003). "An O(m) Algorithm for Cores Decomposition of Networks." arXiv:cs/0310049.
- Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008). "Fast unfolding of communities in large networks." Journal of Statistical Mechanics, P10008.
- De Domenico, M., Solé-Ribalta, A., Cozzo, E., Kivelä, M., Moreno, Y., Porter, M. A., Gómez, S., & Arenas, A. (2013). "Mathematical Formulation of Multilayer Networks." Physical Review X, 3(4), 041022.
- Ficsor, A., Czvetko, T., Sebestyén, V., & Abonyi, J. (2025). "HyperGodot: Interactive hypergraph visualization tool." SoftwareX.
- Newman, M. E. J. (2006). "Modularity and community structure in networks." PNAS, 103(23), 8577-8582.
- Praggastis, B., et al. (2023). "HyperNetX: A Python package for modeling complex network data as hypergraphs." arXiv:2310.11626.
- Schaub, M. T., Delvenne, J.-C., Rosvall, M., & Lambiotte, R. (2017). "The many facets of community detection in complex networks." Applied Network Science, 2(4).
- Seidman, S. B. (1983). "Network structure and minimum degree." Social Networks, 5(3), 269-287.

---

*Zero em dashes in this file.*
