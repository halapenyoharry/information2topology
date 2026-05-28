---
title: "Information to Topology: A Method for Turning Prose into Navigable Hypergraphs"
author: "Harold Young"
date: "2026-05-28"
version: "1.3.0"
status: "Released"
license: "CC BY-NC-ND 4.0"
---

# Information to Topology: A Method for Turning Prose into Navigable Hypergraphs

### Document Metadata
* **Author**: Harold Young
* **Published**: May 22, 2026
* **Current Version**: v1.3.0 *(Replaces v1.2.1)*
* **Status**: Released for Peer Review

### Document Control & Version History
For readers accessing this document outside of a version-controlled repository, the table below documents the lineage of structural and philosophical revisions:

| Version | Date | Status | Key Milestones & Structural Refinements |
| :--- | :--- | :--- | :--- |
| **v1.0.0** | May 22, 2026 | Initial Draft | Drafted core hypergraph specification (`S1-S7`), the evidence-interpretation firebreak, the four-category edge division, the Camus worked example, and decomposition mathematics. |
| **v1.1.0** | May 22, 2026 | Released | Integrated the Abhidhamma's *Paṭṭhāna* paccaya system as an ancient n-ary relational peer. Elevated the evidence-interpretation divide to the paper's *Central Theoretical Result*. Reframed the edge categories as an *Algorithmic Decision Procedure*. Formulated the dyadic-projection emission tension as a legacy substrate concession, projecting the specifications for a *Hyperedge-Native Renderer*. Expanded the *Structural-Isomorphism Recovery Hypothesis* into a full philosophical defense in Section 8. |
| **v1.2.0** | May 22, 2026 | Peer Review | Integrated Theravada oral-transmission lineage caveat in Footnote [^3a]. Framed the hyperedge-native renderer as an unbuilt specification and the immediate next artifact on our development roadmap. Formulated the Inter-Annotator Convergence Test as a rigorous falsification protocol in Section 8, linking shared empirical edges to topological consensus. |
| **v1.2.1** | May 26, 2026 | Peer Review | Editorial: renamed the n-ary→dyadic emission technique from "star projection" (and the inherited "synthetic hub" / "spokes" geometry language) to "dyadic projection" with a synthetic node per arity-≥-3 edge. The technique is unchanged; only the name moved, to stop the geometry metaphor from cueing readers (especially LLM consumers) to re-reify the schema-artifact synthetic node as an ontological center. |
| **v1.3.0** | May 28, 2026 | Peer Review | Established the **State-Change Layer** property (Section 4): the layer is a token-level directed acyclic graph (the history) whose type-quotient is a state-transition system that may cycle — a lossy projection in the project's own sense. Sharpened the no-reification constraint into the operational rule **reification is earned by reference**. Added a second worked example (the plot spine of *The Wizard of Oz*, re-extracted under full current discipline) and a labeled inter-annotator divergence set for the convergence test (Section 8). Added Section 9, *Open Questions*, marking the understanding still required. |

---

## Abstract

Most knowledge representation systems suffer from a historical accident, an ancient design choice that forces arbitrary information into simple pairs. This paper introduces a formal method for representing complex textual information as multi-dimensional hypergraphs without losing structural integrity or imposing a fixed vocabulary. By separating empirical evidence from reader interpretation, and by classifying relationships into four fundamental categories derived from first principles, this method provides a rigorous pathway for turning prose into navigable topology. We demonstrate this transformation using the philosophical structures in Albert Camus’s *The Myth of Sisyphus* and detail the mathematics of hypergraph decomposition that make high-dimensional information legible to human eyes.

---

## 1. The Problem: The Linear Prison and the Dyadic Constraint

We live in a world where complex thought is routinely flattened by its containers. A book is a linear sequence of pages, a narrative is a thread of assertions, and even our most advanced databases are collections of tables that split reality into rigid rows. When we attempt to represent knowledge using networks, we almost always default to the **dyadic constraint**, an architectural assumption that every relationship is a spring between exactly two point masses [^1]. This constraint is not a structural requirement of information itself, but rather a historical accident inherited from Leonhard Euler's 1736 analysis of the bridges of Königsberg [^2]. 

Euler wanted to know if a traveler could cross all seven bridges of the city without doubling back, and in solving this puzzle, he represented the landmasses as points and the bridges as lines. This simple vertex-and-edge model laid the foundation for modern graph theory, yet it left us with a persistent bottleneck. Because our visualization libraries and database engines model edges as line segments between two endpoints, we force every multi-party interaction, every chemical reaction, and every nuanced philosophical argument into a series of disconnected pairs [^3]. The loss is a transduction tax that destroys the unity of complex facts, substituting a tangle of pairwise approximations for what was originally a single, coherent event.

To assume that relational thinking began with graph theory, or that the flattening of complex dynamics into simple pairs is a native property of human reasoning, is to succumb to the bias of our physical computing substrates. Two millennia before Euler abstracted the pathways of Königsberg, the Theravada Abhidhamma formulated the *Paṭṭhāna*, a massive cognitive and ontological treatise mapping the universe as a network of twenty-four classes of conditional relations, known as *paccaya* [^3a]. In this classical system, causality is never a simple linear arrow between a single cause and a single effect, but rather a multi-dimensional emergence from complex, n-ary dependency webs where multiple simultaneous conditions must cooperate. The *Paṭṭhāna* understood that physical states, mental processes, and moral acts are bound by spatial, temporal, and functional overlaps, utilizing typed, non-dyadic structures that predated Euler's vertex-and-edge model by two thousand years. The modern database's binary junction table is not an evolutionary apex of human organization, but a historical regression, a substrate-imposed cage that we must escape to recover our classical relational heritage.

Information does not exist in simple pairs, nor does it yield its secrets to linear reading alone. As Stephen Downes has argued in his connectivist work, knowledge is not a static repository of assertions, but rather a distributed representation of states of affairs created by our interactions with each other [^4]. The graph is at once the outcome of these interactions and the source of truth about those states of affairs. To learn is to experience the growth, development, and traversal of this network, but our current tools make the topology invisible. They present us with the linear narrative, guessing at motives and inner thoughts, rather than showing us the complexity and interdependence of the underlying ideas [^5].

To break out of this linear prison, we must reclaim our topological intuition. We need a method that can turn arbitrary prose into navigable graphs, representing relationships exactly as they are written, without requiring us to pre-determine what those relationships mean. The challenge is not to build more complex databases, but rather to establish a structural discipline that respects the native shape of our thoughts, reviving a relational worldview that predates the very tools we use to model it.

---

## 2. The Format: One Structural Commitment, Zero Vocabulary Commitments

The solution begins with a radical asymmetry: we commit absolutely to a closed set of three structural primitives, while remaining entirely open to any vocabulary the writer or domain requires. This asymmetry is the core design choice of the TopoThink hypergraph format (`*.hypergraph.topothink.json`). The base data model is a hypergraph in the mathematical sense, a set of nodes and a set of edges where each edge can connect any number of nodes, extended by four specific rules that make it federable and expressive.

The format consists of exactly three primitive types, with no other structures permitted:

1. **Nodes**: The entities being related, each carrying a globally unique identifier.
2. **Edges**: The relationships themselves, which connect any number of nodes and carry their own unique identifiers.
3. **Incidences**: The explicit records of participation, which connect a single edge to a single node and define the role that node plays in the relationship.

```
                  +-----------------------------------+
                  |           Edge Object             |
                  |  - id: "edge:thesis-revolt"       |
                  |  - attrs: { "i2t:predicate"... }  |
                  +-----------------------------------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
            v                                               v
+-----------------------+                       +-----------------------+
|   Incidence Object    |                       |   Incidence Object    |
| - edge: "edge:..."    |                       | - edge: "edge:..."    |
| - node: "absurd"      |                       | - node: "revolt"      |
| - role: "source"      |                       | - role: "target"      |
+-----------------------+                       +-----------------------+
            |                                               |
            v                                               v
+-----------------------+                       +-----------------------+
|      Node Object      |                       |      Node Object      |
|  - id: "absurd"       |                       |  - id: "revolt"       |
+-----------------------+                       +-----------------------+
```

By separating edges from their endpoints using an explicit incidence list, the format satisfies seven structural rules that must hold for any valid topothink file:

* **S1. Three primitive types, no others.** Hierarchy is expressed through edges, not through nested containment. A nested `children` array inside a node is forbidden.
* **S2. Every node has a globally unique identifier.** Two files that share a node identifier are already talking about the same entity, unifying on merge without intermediate code.
* **S3. Every edge has its own identifier and lists its incident nodes via incidences.** Decoupling edges from incidences lets the same edge naturally extend to any number of nodes without schema changes.
* **S4. All three primitives are reifiable.** An edge or an incidence can be given its own identifier and treated as a node, allowing us to make statements about relationships themselves.
* **S5. Edges connect any number of nodes ($\ge 1$).** Unary, dyadic, and n-ary relationships are handled by the same structure, avoiding information-destroying pairwise hacks.
* **S6. Direction is optional and per-edge.** Edges distinguish source and target roles when directed, while remaining undirected by default.
* **S7. Nodes, edges, and incidences may carry attributes.** Every entity supports an open-vocabulary `attrs` object holding arbitrary key-value pairs.

This schema is deliberately designed to prevent the creation of hierarchical trees as primary structures. By forcing relationships to live in a flat, explicit list of edges and incidences, we ensure that the topology remains open, flexible, and federable across multiple files. We do not restrict what keys may appear in the attribute objects, nor do we validate them against a closed list of allowed predicates. Vocabulary collisions are resolved by ingestion adapters during merge, not by the schema itself. The structure is fixed, but the language remains entirely free.

---

## 3. The Editorial Discipline: Edges Report, Incidences Interpret

A format alone cannot guarantee honest graphs. When an artificial intelligence or a human annotator reads a text, there is a constant temptation to bake subjective interpretations directly into the structural predicates of the graph, welding categories like "antagonist" or "turning_point" onto the edge itself. When we commit this error, we weld our opinions directly into the topology, which means that any subsequent reader who disagrees with our reading must fork the database itself to represent their disagreement, destroying the possibility of shared research.

To prevent this structural gridlock, we introduce the **central theoretical result of this methodology**: a strict three-layer editorial firebreak that separates empirical evidence from interpretive annotation.

$$\text{Edge Label} \quad \longleftarrow \quad \text{Pure text, zero interpretation (Empirical Anchor)}$$
$$\text{Incidence Role} \quad \longleftarrow \quad \text{Weak interpretation (Text-mappable syntax)}$$
$$\text{Incidence Attrs} \quad \longleftarrow \quad \text{Strong interpretation (Reader-imposed opinion)}$$

Under this discipline, **the edges report, while the incidences interpret.**

### Edges as Pure Text Evidence: The Anchor of Consensus

An edge between nodes represents the historical or textual connection itself, carrying the actual phrase, sentence, or prose excerpt that brought the relationship into being as its primary label. This excerpt is an empirical anchor, verifiable against the physical manuscript, making the graph a reproducible index of the text rather than a subjective claim about it. Anyone looking at an edge can verify it by reading the passage that justified it. By keeping the edge's structural existence completely independent of what the relationship *means*, we establish a shared, objective evidence layer.

### Incidence Roles as Text-Mappable Syntax

The role of each incidence describes how a particular node participates in the relationship, using text-supported categories like `speaker`, `addressee`, `predecessor`, or `successor`. These roles reflect the grammar of the sentence itself, serving as a transitional layer between raw text and formal topology. For example, the sentence "Samara spoke to the traveler" is represented by an interactivity edge carrying the raw quote, with one incidence assigning `speaker` to Samara and another assigning `addressee` to the traveler, mapping the text's active syntax without asserting its deeper psychological meaning.

### Incidence Attributes: The Pluralistic Interpretation Layer

This is where the reader's conscious, subjective interpretation lives, captured as key-value attributes on the incidence object rather than on the edge. If an annotator believes that Samara’s speech serves as a "turning point" in the chapter, or that her character is an "antagonist," these claims are written as attributes on her specific incidence.

Because these interpretive annotations are pushed entirely to the incidences, different readers can disagree profoundly without changing the underlying network structure. Their disagreements exist as distinct, overlayable attribute layers that occupy the exact same topological coordinates. This separation solves the federability problem: two scholars who hate each other's interpretations are still standing on the same shared edges, reading the same empirical anchors, and collaborating on the same mathematical structure. Honesty and federability turn out to be the exact same property, realized by pushing our opinions off the edges and onto the incidences that connect them. 

---

## 4. The Four Categories of Relationship: A Structural Decision Procedure

To translate complex prose into a visual medium without introducing false nodes, we classify every edge into exactly one of four fundamental categories, derived from first principles. Rather than handing the reader or the annotator a static taxonomic vocabulary of relationship types to memorize, this methodology provides a dynamic **algorithmic decision procedure**, which is a four-step structural test that resolves any relationship to its core mathematical type based on its temporal, spatial, and functional characteristics.

```
                           Is there a transition over time?
                                     /          \
                                  (Yes)         (No)
                                   /              \
                           [State Change]     Is Y enclosing X?
                                               /          \
                                            (Yes)         (No)
                                             /              \
                                      [Containment]    Does something propagate?
                                                         /          \
                                                      (Yes)         (No)
                                                       /              \
                                               [Interactivity]     [Reference]
```

This procedure is structural rather than lexical, which means that the resulting visual idioms are mathematically downstream of these structural commitments rather than superficial decorations slapped on top of a generic network. The geometry of the visualization is the logical form of the thought itself.

### 1. State Change: Flow along Time

* **The Structural Test**: *Is there a directed transition along time (or along another attribute that changes over time) from one state to another?* If the source text reports a clear before/after sequence, the edge resolves to a State Change.
* **The Visual Idiom**: A positional flow, gradient, or motion trail that implies direction through structural layout and visual weight rather than a legacy arrowhead. Because the structural commitment is to a transition, the rendering engine must position the nodes along a directional axis.
* **Example Predicates**: `causes`, `transforms_into`, `next_paragraph`, `supersedes`.

### 2. Containment: Asymmetric Enclosure

* **The Structural Test**: *Does Y enclose X along a spatial, temporal, set-membership, or type-hierarchy dimension without X enclosing Y?* This category requires asymmetric enclosure, where removing $X$ from $Y$ is a meaningful operation that leaves $Y$ diminished in a part-whole sense.
* **The Visual Idiom**: $Y$ is rendered as a physical enclosing region, and $X$ is drawn directly inside $Y$'s boundary. Crucially, **no line connects them**; the spatial enclosure itself is the relationship. To draw a line between a container and its contents is to violate the structural commitment, cluttering the view with redundant dyadic links.
* **Example Predicates**: `member_of`, `scene_contains`, `during`, `inside`.

### 3. Interactivity: Active Propagation

* **The Structural Test**: *Is there an active channel between entities through which force, communication, data, signal, or energy propagates?* Unlike State Change, Interactivity does not require a temporal transition; it can represent an ongoing, multi-directional channel in stable equilibrium.
* **The Visual Idiom**: A shared visual field, overlapping boundary, or gradient blend at the interface. This idiom shows both ends actively shaping the space between them, reflecting the propagation of influence without creating synthetic intermediate nodes.
* **Example Predicates**: `married_to`, `speaks_to`, `depends_on`, `binds_to`.

### 4. Reference: The Passive Pointer

* **The Structural Test**: *If the relationship is a static comparison or a passive citation that does not involve time-transitions, asymmetric enclosures, or active propagations, it falls to the default case.*
* **The Visual Idiom**: A floating marker or callout with very low visual weight. This prevents passive references from dominating the visual layout, leaving the active topology clean and legible.
* **Example Predicates**: `mentions`, `cites`, `analogous_to`, `older_than`.

### The Visual Perception of Logic

When a reader looks at a hypergraph generated by this method, they immediately comprehend the conceptual connections. This immediate comprehension occurs because their visual system is perceiving the direct output of the decision procedure rather than parsing an arbitrary vocabulary of abstract types. They do not need to look up a legend to understand that a node inside a boundary is contained, or that a shared color field represents interaction; the spatial cognition of the human eye maps directly to the logical structure of the prose.

### The No-Reification Constraint

A key discipline of this categorization system is that it operates without reifying relationships into intermediate nodes unless the source text explicitly treats them as entities [^6]. We do not invent a synthetic node for a marriage or a meeting to make the categories fit. A marriage is represented as a single interactivity edge connecting two people, and a meeting is a single n-ary interactivity edge connecting all attendees. By avoiding the multiplication of entities, we keep the graph proportional to what the text names, ensuring the visual category itself does the work that traditional schemas delegate to structural nodes.

This constraint admits a precise operational test. Because every edge already carries its own attributes (Rule S7), reifying an edge — letting its identifier also appear as a node — buys nothing except the ability to become the *target* of another edge. Reification is therefore **earned by reference**: an edge should be reified only when another edge points at it as a node. The Wizard of Oz extraction illustrates both the failure and the fix. An early version reified seven narrative events, six of which were referenced by no other edge — inert reification, the precise reflex this constraint forbids. The remedy was not deletion but justification: wiring the six pivotal events into a token-level history graph via `precedes` edges supplied the references that earn their reification. The same audit reclassified the seventh "event," the Wizard appearing differently to each petitioner, as an Interactivity edge — a one-to-many deception channel, not a temporal transition — which correctly removed it from the narrative spine and left it unreified, since nothing points at it.

### The State-Change Layer: Token-DAG and Type-Quotient

The four categories classify each edge in isolation, but State Change carries a structural property the other three do not — one that becomes visible only when its edges are assembled into a single layer. Consider the subgraph of all State Change edges. When its nodes are concrete, dated occurrences — *tokens* — the layer is a **directed acyclic graph**, the covering relation of a temporal partial order. Physical time has an arrow and does not loop, so no occurrence can precede itself, and a topological sort of this layer returns precisely the order in which events happened. This is the *history*, or trajectory, of the system the text describes.

The same layer behaves differently when its nodes are *types* rather than tokens. Collapse every occurrence of an event-type into a single node — every El Niño into "El Niño," every evaporation into "evaporation" — and the timeline folds into a recurring pattern that may now contain cycles: evaporation $\rightarrow$ condensation $\rightarrow$ precipitation $\rightarrow$ evaporation. This cyclic object is a **state-transition system** (a state machine in the discrete case; a phase portrait or oscillator in the dynamical-systems case), and it is fundamentally a different graph from the history. It is the **quotient** of the token-DAG under the equivalence "same type," and a quotient discards information by construction: identifying *niño-1999* with *niño-2010* as one node erases the distinction between them. The cycle is therefore not a richer view of the history but a lossy compression of it.

This places the transition-system precisely within the architecture of Section 5. The type-quotient cycle is a **projection** of the token-DAG, in the same sense that the normalized-dyadic form is a projection of the canonical hypergraph: a more legible, strictly lossier view that must not be mistaken for the source of truth. It carries the same metadata discipline — tagged `i2t:relation_to_canonical: type-quotient` — and the same faithfulness-versus-legibility tension that governs the whole pipeline. Whether the history or the transition-system is *primary* depends on the domain: in empirical settings (a weather record, a biography, a novel's plot) the history is the source and the cycle is an abstraction derived from it; in designed settings (a traffic signal, a protocol, the rules of a game) the transition-system is the specification and each history is a run of it. The split between the two graphs holds either way.

A short worked example makes the property concrete. The plot of L. Frank Baum's *The Wonderful Wizard of Oz*, re-extracted under the full current discipline (1,202 nodes / 1,213 edges / 3,542 incidences), contains six pivotal events that form the narrative's State-Change spine:

$$\text{cyclone} \rightarrow \text{killing of the East Witch} \rightarrow \text{melting of the West Witch} \rightarrow \text{unmasking} \rightarrow \text{balloon departure} \rightarrow \text{homecoming}$$

A topological sort of the spine returns exactly this story-time order, and the layer is confirmed acyclic. Because Oz is a linear quest, no two spine events share a type, so its type-quotient is **trivial** — it contains no cycle. This near-degenerate result is itself instructive: Oz exhibits the token-DAG in its cleanest form while simultaneously demonstrating why a second corpus — one built on genuine recurrence, such as a character who repeats a behavior, a seasonal cycle, or a returning motif — is required to display a nontrivial cyclic quotient standing over an acyclic token-history. The only recurrence in Oz lives at the episodic level (the repeated "threat encountered, threat overcome" of the Kalidahs, the fighting trees, and the Hammerheads), precisely where such a quotient would begin to form.

---

## 5. The Operational Pipeline: From Text to Topology

The transformation of raw prose into a canonical hypergraph follows a strict, four-stage pipeline: **Ingest $\longrightarrow$ Canonical $\longrightarrow$ Transform $\longrightarrow$ Emit**. In this pipeline, the artificial intelligence is treated not as a collaborative writer, but as a precise parser and instrument, executing the editorial discipline under human supervision.

```
Raw Text (Prose)
       │
       ▼   [LLM Parser with Canonical Prompt]
 Ingest Adapter
       │
       ▼   [Enforces S1-S7 and Decouples Incidences]
Canonical TopoThink Hypergraph (*.hypergraph.topothink.json)
       │
       ▼   [Transform: Predicate Split / k-Core Decomposition]
Transform Layer
       │
       ▼   [Emit: Normalized-Dyadic Projection]
Emitter Layer  ───► Output: D3 / Cytoscape / JVV
```

### Ingestion

The raw manuscript or structured data source is parsed by an ingestion adapter. When dealing with unstructured text, the adapter uses an LLM configured with a canonical system prompt [^7]. This prompt directs the model to extract nodes, edges, and incidences, enforcing the three-layer editorial discipline by using actual text excerpts as edge labels and assigning specific, text-supported roles to incidences.

### Canonical Enclosure

The raw extraction is normalized into the TopoThink JSON schema. The adapter ensures that all node identifiers are globally unique, that every edge is decoupled from its incident nodes, and that all three primitives conform to the S1–S7 structural rules. 

### Transformation

The canonical hypergraph is run through various transform adapters to prepare it for rendering or analysis. The most basic transformation is the predicate split, which groups edges by predicate type to produce separate, single-relationship layers [^8]. Other transforms compute density hierarchies, extract local neighborhoods around specific nodes, or flag multi-layer overlaps.

### Emission: The Legacy Substrate Bottleneck

Because standard visualization libraries cannot render hyperedges of arity $\ge 3$ or reified edges, the emitter layer projects the canonical hypergraph into a target format. For traditional tools like D3.js or Cytoscape, the emitter performs a **normalized-dyadic projection**. This projection is lossy: each hyperedge of arity $\ge 3$ is reified as a synthetic node with one dyadic link per member, and reified edges are promoted to synthetic vertices in the same way.

We must be honest about the discomfort of this step: it is a legacy substrate concession that directly violates our own no-reification discipline. While the canonical TopoThink layer keeps the network clean, the emission step forces the creation of synthetic nodes (one per arity-≥-3 hyperedge) to satisfy the dyadic constraint of the rendering engine. When these synthetic nodes leak back up into the visual field, they contaminate the reader's intuition, making a single, multi-party event look like an artificial coordinate tree. The transduction tax is paid in the form of visual clutter.

This tax, however, is a historical relic of the libraries we currently use, not an inherent requirement of the model itself. The four visual idioms defined in Section 4, consisting of enclosure regions for containment, shared fields for interactivity, and directional flows for state change, are not merely design suggestions, but are a complete functional specification for a **hyperedge-native renderer** that bypasses the transduction tax entirely. We must explicitly acknowledge that this renderer is currently an unbuilt specification, an open engineering problem that represents the immediate next artifact on our developmental roadmap rather than a completed tool. By formalizing this specification, we convert the current vulnerability of leaking synthetic nodes into a concrete roadmap, designing our way out of the dyadic constraint to ensure that our rendering engines eventually match the non-dyadic relational thinking they are built to display.

---

## 6. Worked Example: Camus’s *The Myth of Sisyphus*

To see this method in action, we examine its application to Albert Camus’s *The Myth of Sisyphus*. The essay explores the dialectical movement from the absurd, which is born of the confrontation between human nostalgia for unity and the silent, irrational world, through lucidity to revolt, freedom, and passion. 

The canonical hypergraph represents these concepts as nodes, using globally unique identifiers and capturing their textual justifications in the edge labels. Below is a subset of the nodes extracted from the corpus, demonstrating the open vocabulary and attribute structure:

```json
{
  "nodes": [
    {
      "id": "camus",
      "attrs": {
        "label": "Albert Camus",
        "i2t:type": "Philosopher",
        "lifespan": "1913-1960",
        "role": "author of the essay; the philosophical voice"
      }
    },
    {
      "id": "absurd",
      "attrs": {
        "label": "the Absurd",
        "i2t:type": "Concept",
        "definition": "born of the confrontation between human longing for unity and the silent, irrational world"
      }
    },
    {
      "id": "suicide",
      "attrs": {
        "label": "Suicide",
        "i2t:type": "Concept",
        "role": "called the only truly serious philosophical problem; rejected as a response"
      }
    },
    {
      "id": "revolt",
      "attrs": {
        "label": "Revolt",
        "i2t:type": "Concept",
        "role": "first consequence of the absurd: the conscious refusal to consent to it"
      }
    },
    {
      "id": "sisyphus",
      "attrs": {
        "label": "Sisyphus",
        "i2t:type": "MythologicalFigure",
        "source": "Greek myth; Homer",
        "role": "wisest of mortals; condemned to roll the rock; the absurd hero"
      }
    }
  ]
}
```

Now, consider a single complex relationship in the text: Camus's assertion that the absurd is born of the confrontation between human nostalgia and the silent world, and that this absurd is bounded by death. We represent this as an n-ary interactivity edge (`edge:absurd-genesis`) and a directed state change edge (`edge:absurd-boundary`). 

The JSON representation below shows how the incidences decouple the nodes, allowing roles and attributes to carry the interpretive weight:

```json
{
  "edges": [
    {
      "id": "edge:absurd-genesis",
      "directed": false,
      "attrs": {
        "label": "The absurd is born of this confrontation between the human need and the unreasonable silence of the world.",
        "i2t:predicate": "born_of_confrontation",
        "i2t:edge_category": "interactivity"
      }
    },
    {
      "id": "edge:absurd-boundary",
      "directed": true,
      "attrs": {
        "label": "The absurd ends with death; there is no absurd outside this world.",
        "i2t:predicate": "bounded_by",
        "i2t:edge_category": "state_change"
      }
    }
  ],
  "incidences": [
    {
      "edge": "edge:absurd-genesis",
      "node": "absurd",
      "role": "emergent_product"
    },
    {
      "edge": "edge:absurd-genesis",
      "node": "nostalgia_for_unity",
      "role": "human_term"
    },
    {
      "edge": "edge:absurd-genesis",
      "node": "irrational",
      "role": "worldly_term"
    },
    {
      "edge": "edge:absurd-boundary",
      "edge_role": "source",
      "node": "absurd",
      "role": "bounded_entity"
    },
    {
      "edge": "edge:absurd-boundary",
      "edge_role": "target",
      "node": "death",
      "role": "limiting_boundary"
    }
  ]
}
```

By applying the decision procedure:
1. `edge:absurd-genesis` represents an active confrontation where the absurd emerges from two opposing terms. Because something propagates (the confrontation itself), it is classified as **interactivity**.
2. `edge:absurd-boundary` represents a temporal limit that terminates the absurd at death. Because it asserts a transition along the boundary of existence, it is classified as **state_change**.

---

## 7. Decomposition, Rendering, and the Visual Bottleneck

When we attempt to render a complex hypergraph, we immediately run into a visual bottleneck. If we project the entire, high-dimensional structure onto a flat screen in a single force-directed layout, we produce an incomprehensible "hairball" of overlapping lines. The current rendering problem is a measurement problem: we force a premature collapse of the topology, destroying structural information before the human eye can parse it.

The solution is to perform structural **decomposition**, slicing the high-dimensional object into natural, low-dimensional views that are honest and legible. Like an architect drawing plans, sections, and elevations of a three-dimensional building, we use a toolkit of mathematical decompositions to isolate specific structural layers:

### Multilayer Slicing

Using the tensor-algebraic framework formalized by Matteo De Domenico and colleagues, we slice the hypergraph by predicate type to produce a stack of single-relationship layers [^9]. Each layer contains only one class of edge (such as containment or reference), and inter-layer edges connect the same node where it appears across different sheets.

### k-Core Decomposition

We recursively strip away vertices with fewer than $k$ connections to reveal the nested density hierarchy of the network. This linear-time algorithm, introduced by Stephen Seidman, acts like an onion skin, separating the peripheral noise of transient mentions from the highly connected core where the primary arguments reside [^10].

### Connected Components and Community Detection

We identify lateral clusters and completely isolated subgraphs. By applying modularity optimization or the Louvain method, we group nodes that are more densely connected internally than they are to the rest of the network, revealing the "neighborhoods" of the concept space [^11].

### Simplicial Homology

To find the natural low-dimensional regularities within the hypergraph, we represent it as a simplicial complex. By calculating its Betti numbers, we count its connected pieces ($B_0$), its independent cycles ($B_1$), and its enclosed cavities or voids ($B_2$), producing a topological signature that describes the holes in our knowledge [^12].

The whole structural-isomorphism claim is fucking interesting if you sit with it long enough: the shapes we find when we decompose these text-derived hypergraphs are not arbitrary, but instead reflect the native attention patterns of the human mind that wrote the prose. When a graph is half-well thought out, with meaningful edges and minimal opinionated reification, it functions not merely as a repository, but as a perceptual system.

---

## 8. The Recovery Hypothesis: Structural Isomorphism and Cognitive Liberation

This brings us to the boldest, most radical claim of this methodology: structural decomposition is not a process of arbitrary mathematical construction, but rather one of **topological recovery**. We are not imposing an arbitrary network model onto Albert Camus’s prose; we are reading off the exact topology that his attention already possessed, a structure that was temporarily flattened and hidden by the linear prison of printed text.

This structural-isomorphism claim is a falsifiable, cognitive hypothesis:

$$\text{Prose Narrative (Linearized)} \quad \stackrel{\text{De-linearize}}{\longrightarrow} \quad \text{TopoThink Hypergraph} \quad \stackrel{\text{Decomposition}}{\longrightarrow} \quad \text{Recovery of Attention Structure}$$

A crucial counterargument arises here: a skeptic may rightly argue that any recovered isomorphism exists not between the topology and the author's cognitive attention, but between the topology and our own subjective reading of the text. To defend against this projection bias, we must construct a rigorous falsification protocol that links the recovery hypothesis directly back to the empirical firebreak established in Section 3. The exact mechanism of this validation is the **Inter-Annotator Convergence Test**. If multiple independent annotators, working in isolation and applying the strict algorithmic decision procedure of Section 4, build hypergraphs whose edges are strictly constrained to pure text excerpts, we can mathematically compare their resulting topologies. If their separate hypergraphs yield convergent structural signatures, specifically matching $k$-cores, modularity communities, and identical Betti numbers, then the recovered topology cannot be dismissed as the subjective projection of an individual reader. Instead, the structure must reside objectively in the prose itself, proving that the text is a stable, structural linearization of the author's attention patterns to the degree that the prose is well-constructed.

The decision procedure also yields a natural, labeled test set for this protocol. Most edges classify unambiguously: structural relations such as paragraph succession and chapter containment are fixed by their predicate, and the great majority of semantic relations resolve cleanly. A minority sit on genuine category boundaries — possession versus set-containment, a road as a spatial reference versus a channel through which travel propagates, a precondition versus a runtime dependency. The extraction can flag exactly these (`i2t:edge_category_review`), partitioning the edge set into the edges where independent annotators *must* converge and the smaller set where divergence is itself the signal. The convergence test thereby becomes measurable over a labeled set rather than asserted in the abstract: high agreement on the determined edges establishes that the structure is objective, while the distribution of disagreement on the flagged edges localizes precisely where the text underdetermines its own form. In the Wizard of Oz re-extraction, this flagged set numbered thirteen edges out of more than twelve hundred — a small, well-defined locus of legitimate interpretive freedom against a large body of forced agreement.

If this hypothesis holds, it explains why presenting a highly connected, well-conceived graph to a student immediately unlocks deep comprehension. We are not handing them a new, artificial vocabulary of relationship types to memorize, nor are we forcing them to parse a decorative visual layout. Instead, we are presenting their visual cortex with a spatial map that is isomorphic to the conceptual organization of the author's mind. When a graph is drawn with honest, empirical edges and zero opinionated reifications, it ceases to be a static repository of assertions and becomes an active connectivist instrument.

The visual layout provides a set of structured paths, and the human mind, recognizing its own native architecture, immediately does the rest. By breaking the dyadic constraint and escaping the physical limits of our legacy computing substrates, we do not merely build better databases; we liberate the structural forms of human thought, recovering an ancient relational heritage that has waited for millennia to be seen.

---

## 9. Open Questions: The Understanding Still Required

The State-Change layer and its type-quotient sharpen one category, but they open as much as they close. We record the principal unresolved questions here, both to mark the boundary of the present claim and to set the agenda for the work that follows.

**A corpus with genuine recurrence.** The Wizard of Oz is the near-degenerate case: a linear history whose type-quotient is trivial. The cyclic transition-system has been characterized but not yet *exhibited* on real extracted text. A second fixture is required whose narrative carries true recurrence — a behavioral loop, a seasonal cycle, a returning motif — so that a nontrivial quotient cycle can be shown standing over a token-history that is genuinely acyclic underneath. Until that fixture exists, the cyclic half of the claim rests on constructed examples (the water cycle, the El Niño–Southern Oscillation) rather than on a faithful extraction. This is the single most important next artifact, because it determines whether the central new claim of this revision can be demonstrated rather than merely defined.

**Is the token/type axis orthogonal to all four categories, or peculiar to State Change?** The history/transition-system distinction was discovered in State Change, but the token-to-type collapse is a general operation. A Containment layer collapsed by type yields a class hierarchy rather than a set of concrete enclosures; an Interactivity layer collapsed by type may yield recurring interaction patterns. Whether each category possesses its own layer-level structure under quotient, and whether those structures are useful, is unexamined.

**The boundary edges.** The category boundaries that produce the flagged review set — possession versus containment, channel versus reference, precondition versus dependency — are not yet governed by adjudication rules. Several may be genuinely *view-dependent*: an `imports` relation is a static Reference in a dependency listing and an active Interactivity at runtime. Whether the format should record the view explicitly, or admit per-view classifications of the same edge, remains open.

**Should the type-quotient be a first-class adapter?** The projection is presently described but not implemented. A `quotient_by_type` emitter — producing a transition-system tagged `i2t:relation_to_canonical: type-quotient` — would make the lossy abstraction inspectable alongside the faithful history, and would force an explicit definition of what constitutes "same type," which the source text does not always supply.

**Should reification-by-reference be normative?** The operational test — reify only what another edge references — currently lives as extraction practice. Promoting it to a normative rule in the format specification would convert the inert-reification failure from a matter of discipline into a validation error, at the cost of forbidding a class of files that may have legitimate reasons to reify in advance of reference.

These questions are not peripheral. The first decides whether this revision's central claim is empirical or merely formal; the remainder decide whether the State-Change layer's structure generalizes to the rest of the typology or remains a property of one category alone.

---

## Endnotes and Technical Specifications

[^1]: The dyadic constraint refers to the mathematical limitation where edges are defined strictly as pairs of vertices: $E \subseteq V \times V$. This is the default structure of standard GraphJSON, GML, and most SQL schema patterns (where a junction table contains exactly two foreign keys: `node_a_id` and `node_b_id`).
[^2]: Euler, L. (1736). "Solutio problematis ad geometriam situs pertinentis." *Commentarii Academiae Scientiarum Imperialis Petropolitanae*, 8, 128-140. Euler's paper is widely considered the birth of graph theory, formulating the Königsberg bridge problem as a network of landmasses (vertices) and bridges (edges).
[^3]: The transduction tax is the computational and structural cost of converting a higher-order relation into a set of binary relations. For example, a three-member hyperedge $\{A, B, C\}$ must be represented either as a clique of three binary edges $\{(A,B), (B,C), (A,C)\}$, which implies false pairwise relationships, or as a dyadic projection that reifies the hyperedge as a synthetic node $H$ with three dyadic links $\{(A,H), (B,H), (C,H)\}$, which artificially inflates the vertex count.
[^3a]: The *Paṭṭhāna* is the seventh and final book of the Abhidhamma Piṭaka, the philosophical and cognitive core of the Theravada Buddhist canon. While modern scholars attribute its compilation to the third century BCE, the canonical Theravada tradition traces its oral origin back to the lifetime of the historical Buddha, stating that the systematized matrix was first preached in detail by the Apostle Sāriputta before being preserved through generations of communal oral recitation. The text presents an exhaustive relational mapping of reality, categorizing all mental and physical phenomena in terms of twenty-four distinct classes of conditional relations (*paccaya*), such as root condition (*hetu-paccaya*), object condition (*ārammaṇa-paccaya*), and proximity condition (*anantara-paccaya*). This ancient model represents perhaps the earliest formalized network of typed n-ary dependencies in human history.
[^4]: Downes, S. (2018). "EL30 - Graph." Personal Weblog and Lecture Series. Downes argues that learning is connectivist: knowledge is represented in the connections of a network, and the growth of the network is the physical process of learning.
[^5]: Rosenberg, A. (2018). *How History Gets Things Wrong: The Neuroscience of Our Alien Lives*. Rosenberg argues that linear narrative structures are evolutionary adaptations that seduce us into assuming simple causal explanations, whereas real historical and physical events exist as highly complex, non-linear networks of interdependence.
[^6]: Vertex and edge reification in TopoThink is handled by identifying the same string in both the `nodes` list and the `edges` (or `incidences`) list. If an edge carries `id: "edge:foo"`, and a node also carries `id: "edge:foo"`, the edge is reified: another edge can now list `"edge:foo"` in its incidences, making assertions about that relationship.
[^7]: See `prompts/text_to_topothink_hypergraph.md` for the canonical prompt template. The prompt forces the LLM to output valid JSON matching the `hypergraph.topothink.schema.json` schema, using regular expressions to validate that every incidence has an associated edge and node identifier.
[^8]: See `adapters/split_by_predicate.py` for the implementation. The script reads a canonical JSON hypergraph and groups edges by their `attrs["i2t:predicate"]` value, writing separate JSON files for each distinct predicate layer to support modular rendering.
[^9]: De Domenico, M., Solé-Ribalta, A., Cozzo, E., Kivelä, M., Moreno, Y., Porter, M. A., Gómez, S., & Arenas, A. (2013). "Mathematical Formulation of Multilayer Networks." *Physical Review X*, 3(4), 041022. This paper establishes the tensor-algebraic framework for representing networks where nodes exist across multiple thematic layers, allowing formal calculations of multi-layer centrality and diffusion.
[^10]: Seidman, S. B. (1983). "Network structure and minimum degree." *Social Networks*, 5(3), 269-287. The k-core of a graph is the maximal subgraph in which every node has at least degree $k$. The algorithm runs in $O(m)$ time where $m$ is the number of edges, as proven by Batagelj, V., & Zaversnik, M. (2003) in "An $O(m)$ Algorithm for Cores Decomposition of Networks."
[^11]: Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008). "Fast unfolding of communities in large networks." *Journal of Statistical Mechanics: Theory and Experiment*, 2008(10), P10008. This paper introduces the Louvain method, a heuristic method based on modularity optimization that runs in time $O(n \log n)$ on typical networks.
[^12]: Persistent homology and simplicial complex calculations are described in Topological Data Analysis (TDA). The Betti numbers ($\beta_n$) correspond to the rank of the $n$-th homology group: $\beta_0$ represents the number of connected components, $\beta_1$ the number of two-dimensional loops, and $\beta_2$ the number of three-dimensional voids.
