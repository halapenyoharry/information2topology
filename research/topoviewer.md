# TopoViewer

**What it is, before how it's built.**

---

## One sentence

TopoViewer is a graph viewer where the node is the node.

---

## The problem it solves

Every graph viewer that exists treats nodes as dots and labels as metadata. You get a field of identical circles with tiny text you have to squint at or hover over, and the thing the node actually is, a paragraph, a person, a concept, a file, a container, disappears behind the abstraction. The visual lies about the data because it renders every node the same way regardless of what it is.

Labels are treated as optional decoration on the "real" visual, which is the dot. But the dot is nothing. The dot is the renderer's convenience, not the user's. When labels are hidden, the topology is visible but the content is gone. When labels are shown, they overlap and become unreadable because the renderer doesn't treat them as the primary visual object that everything else serves.

The result is that graph viewers are tools for people who already understand the data. They confirm what you know. They don't teach you what you don't know. The topology is there but the meaning is stripped, so you spend your time hovering, clicking, squinting, and mentally reassembling what the tool took apart.

---

## The principle

The node is the node. Visually and logically.

If the node is a paragraph, you see text. If the node is a person, you see the name, large, readable, it IS the node, not a tooltip that appears when you remember to hover. If the node is a project, you see the project name as the object itself. The visual representation and the logical identity are the same thing. Minimum transduction tax between what the node is and what you see.

The dot, if it exists at all, is background. Not foreground.

---

## What it reads

The TopoThink hypergraph format (`*.hypergraph.topothink.json`). Three primitives: nodes, edges, incidences. Open vocabulary attributes on everything. Edges connecting any number of nodes. Reification (edges that are also nodes). Merge-by-id for federation across files.

Also: any graph-shaped JSON that can be detected and normalized. D3 force format (`nodes` + `links`), JGF (`graph.nodes` + `graph.edges`), Cytoscape JSON (`elements.nodes` + `elements.edges`), plain edge lists. If it's a graph, TopoViewer reads it. The hypergraph format is canonical, everything else is recognized and projected.

---

## What it shows

Topology. Nodes positioned by their structural relationships, not by arbitrary grid or random placement. Edges rendered according to what they structurally are, not as uniform lines between uniform dots.

The viewer has layers. Each predicate type (contains, references, follows, authored_by, contradicts) is a layer that can be toggled. Each decomposition (k-core shells, communities, connected components) is a layer that can be toggled. You never see everything at once unless you want to. You navigate the topology one meaningful slice at a time, and each slice is honest and comprehensible on its own.

---

## What it doesn't do

TopoViewer is not TopoLand. TopoLand is Minecraft, actual Minecraft, Cuberite server, Lua plugin reading hypergraph data, generating the world, walking through the topology. TopoLand is a future project.

TopoViewer is a daily-use tool for looking at information topology. It runs on a desktop. It loads a file. It shows you the shape of the data with the content still visible. It is useful today, not someday.

TopoViewer does not edit hypergraphs. The adapters produce the data, TopoViewer displays it. Read-only by default. If editing ever comes, it comes later.

---

## How edges work

Edges are not all the same. An edge that means "contains" is structurally different from an edge that means "references" or "contradicts" or "follows." Current viewers draw all of them as identical lines, distinguished only by color or a tiny label. TopoViewer renders edges differently based on what they structurally are:

- **Containment** edges render as enclosure. The contained node is visually inside the containing node. Not a line between two dots, a region.
- **Sequence** edges render as directed paths. Before flows to after. The arrow isn't decoration, it's the structural fact.
- **Reference** edges render as arcs. One thing points at another. The directionality is visible without labels.
- **Similarity** edges render as proximity. Things that resonate are near each other. The closeness IS the relationship.
- **Opposition** edges render as distance or visual tension. Things that contradict are far apart or visually distinct. Repulsion.

The predicate on the edge (from `i2t:predicate` or `link.layer`) determines which rendering primitive is used. The user doesn't configure this per edge. The topology tells the viewer what to do.

---

## How hyperedges work

A hyperedge connects more than two nodes. Current viewers cannot draw this without faking it (dyadic projection with synthetic nodes, or clique expansion). TopoViewer renders hyperedges as regions, convex hulls or enclosing shapes around the member nodes, following the approach demonstrated by HyperNetX, XGI, and HyperGodot. A co-authorship of three people is one region containing three names, not a fake dot in the middle with three lines radiating out.

---

## How decomposition works

The viewer includes unfuzzballers. Built-in decomposition tools that find the natural low-dimensional structure within a high-dimensional topology:

- **Predicate split**: one layer per relationship type. Already exists in the adapter pipeline (`split_by_predicate.py`), but TopoViewer should also do this at view time from a single merged file.
- **k-Core decomposition**: peel the onion. Show the nested density shells. The periphery fades, the dense core emerges.
- **Community detection**: find the clusters. Groups of nodes more connected internally than externally.
- **Connected components**: identify separate systems.

Each decomposition produces layers that can be toggled, same as predicate layers. The user navigates between views of the same data, each revealing different structural properties.

---

## What the node looks like

The node's visual is determined by its content, not by the renderer's convenience.

- `attrs["schema:name"]` or `label` or `id` (fallback chain) provides the display text.
- `kind` (node, hyperedge, edge-as-node) determines shape treatment.
- The text IS the primary visual element. It is sized to be readable at the current zoom level. It does not shrink to nothing when you zoom out, it either remains readable or disappears cleanly (semantic zoom), never becomes a smear of illegible characters.
- At overview zoom, nodes that are too small to read are rendered as their kind-shape (circle, diamond, square) with color encoding their community or core number or layer membership. Clicking or zooming in reveals the text.
- At reading zoom, the text fills the node. You can read the content without hovering.

---

## What "daily use" means

Harold uses this tool every day to look at the topology of things he's working on: the manuscript, projects, conversations, networks. It needs to:

- Open a file and render in under a second for graphs up to 3,000 nodes
- Handle up to 10,000 nodes without hanging (progressive rendering acceptable)
- Work on macOS as a native or near-native application
- Load files from disk, not require a server
- Export static images (SVG or PNG) for use in articles and the manuscript
- Remember window size and last-opened file across sessions

---

## What it replaces

JVV (json-visual-viewer) in its current form, or becomes its next major version. JVV's Tree, Circles, and Mass views may survive as alternate views. JVV's Graph, Cytoscape, and 3D Graph views are what TopoViewer replaces and improves upon. The core improvement is: the node is the node, the edge is structural, the decomposition is built in, and the viewer reads hypergraphs natively without lossy dyadic projection.

---

## Relationship to other projects

- **information2topology**: produces the data TopoViewer displays. Adapters, format spec, schema, editorial discipline, test corpora. Upstream.
- **TopoLand**: the Minecraft version. Downstream, future. Consumes the same hypergraph format. Different rendering substrate (voxel world vs. graph layout). Different interaction model (walking vs. clicking). Same data.
- **TopoThink (the book)**: the framework that explains why this matters. TopoViewer is one of the "usable by anyone" deliverables the book promises.
- **BAE (Brane Audio Environment)**: the audio renderer. Same hypergraph, edges become sound parameters instead of visual parameters or physics parameters. Third rendering substrate.

---

*Zero em dashes in this file.*
