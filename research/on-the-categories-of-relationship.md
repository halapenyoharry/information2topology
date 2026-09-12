# On the Categories of Relationship in a Hypergraph

A working paper. We are landing here only to take a breath.

---

## The question

If you have a universal format for representing information as a hypergraph, and the format commits to structure but not vocabulary (any predicate goes), then what are the structural primitives that every predicate decomposes into? Is the set finite? Can a renderer that knows only the primitives draw any topology from any domain?

## How we got here

The conversation started with the observation that every graph viewer draws edges as lines between dots. This is an inherited convention from Euler (1736), not a structural necessity. A hyperedge, which connects any number of nodes, has no natural representation as a line between two points. The existing tools (HyperNetX, XGI, HyperGodot) solve this by drawing regions, convex hulls around member nodes, instead of lines. But they still draw all relationships the same way, distinguished only by color. A "contains" edge and a "references" edge are both colored blobs.

The question became: if different relationships have different structural behaviors, shouldn't the renderer draw them differently? And if so, how many structurally distinct behaviors are there?

## First pass: seven, from the literature

We surveyed Allen's interval algebra (13 temporal relations that reduce to three structural ideas), RCC-8 (8 spatial relations), signed graph theory (positive/negative), mereology (parts and wholes), and ontology engineering (RDF/OWL). Every field, starting from a different problem, converged on a small set of structural primitives. We synthesized seven: containment, sequence, boundary, similarity, opposition, association, reference.

## Second pass: six, boundary is emergent

Testing against real domains (family structures, the solar system, gravitational physics) revealed that boundary isn't a declared relationship. Nobody draws an edge labeled "overlaps." Overlap appears when two containment regions share nodes, and the viewer renders the intersection. Boundary moved from the primitive list to the emergent list: visible when the topology is rendered faithfully, not declared in the edge data.

## The Aristotelian frame

Mortimer Adler, reading Aristotle, clarified the distinction. The declared primitives are RELATIONS (Aristotle's category four), describing how things stand to each other. Emergence is not a relation. It is potentiality becoming actuality: node properties are potentials that become actual when they interact during rendering.

Aristotle's four causes map onto the system:

**Material cause:** the nodes and their properties. What the things ARE.

**Formal cause:** the declared edges. The primitives. The structure of the topology.

**Efficient cause:** the rendering process. Emergence lives here. Boundary lives here.

**Final cause:** understanding. The reason the viewer exists.

Adler would insist these are not four separate layers. They are four views of one system.

This framing separated declared edges (formal cause) from emergence (efficient cause). Different questions, different lists, same system.

## Third pass: similarity is emergent too

Similarity is rarely declared as an edge. It is observed when nodes share properties, same type, same era, same keywords, same structural position. The viewer could compute this from property overlap during rendering, placing similar nodes near each other without a declared edge.

Equivalence (A = B, declared identity across sources) is not the same as similarity. Equivalence is a declared reference with a weight of "this is the same thing."

This moved similarity to the emergent list, leaving five declared primitives.

## Fourth pass: four, from verbs not adjectives

The five remaining primitives (containment, sequence, opposition, association, reference) described how things STAND to each other. Static relations. But testing kept producing relationships the static list couldn't hold: flow (input/output across a boundary), transformation (A becomes B), exchange (giving, taking).

The shift came from asking not what things ARE to each other but what things DO.

Sequence folded into state change: sequence is state change at weight zero (pure ordering without transformation). Metamorphosis is state change at maximum weight. Time is baked in, not separate. You cannot go from "A is A" to "A is B" without sequence, and the difference between ordering and transformation is the weight of change.

Opposition and association folded into interactivity: association is low-intensity interaction. Opposition is interaction with negative valence. Flow is interaction with directionality across a boundary. Exchange is interaction where something moves between nodes.

Four declared primitives remained, crossing Aristotle's categories rather than staying within one:

1. **Nested Containment.** Inside / outside, recursively. Nesting depth is information. (Relation.)

2. **State Change (over time).** A becomes B. Location, size, shape, content, any axis can change. Pure sequence is state change at weight zero. (Process.)

3. **Interactivity.** Things doing things to each other. Giving, taking, exchanging, pushing, pulling. Association, opposition, flow, and exchange are all interactivity at different weights and valences. (Action and passion.)

4. **Reference.** Pointing at something without enclosing it, changing it, or exchanging with it. Attention, citation, allusion, dependency. (Relation.)

The four primitives are no longer pure relations. They mix Aristotle's categories: relation, process, action, passion. This might mean they are closer to the actual structure than a list constrained to one category.

## What emerged (not declared, lives in the rendering)

**Similarity:** computed from property overlap during rendering. Two nodes with similar attrs are placed near each other. Nobody declares it.

**Equivalence:** a declared reference where the weight is "this is the same thing."

**Boundary / Overlap:** when containment regions share nodes, the viewer renders the intersection.

**Field effects (gravity, etc.):** when nodes have intensive properties (mass, charge), interactions emerge from proximity. Nobody declares them.

**Stable points (Lagrange, etc.):** positions where fields balance. Emergent from nested, weighted containment.

Emergence is in the rendering. Understanding is in the viewing.

## Where we are not satisfied

We are not confident the four primitives are correct or complete. We are closer, not finished.

- Is interactivity too broad? It swallowed association, opposition, and flow. Can one primitive cover everything from co-occurrence to warfare?
- Does state change need to be explicitly temporal, or can it be atemporal? A mathematical proof transforms premises into conclusions without a clock.
- What are the axes of state change? Location, size, shape, content, what else?
- Can the renderer reliably compute similarity from properties alone, or does it sometimes need to be told?
- Is dependency reference, or reference + containment?
- Does "knowing/perceiving" (one thing taking in the structure of another without consuming it) fit into reference, or is it a fifth primitive?

## What this is for

These primitives are the contract between the hypergraph format and the renderer. The format declares edges with predicates. The renderer maps predicates to primitives. Each primitive gets a visual behavior. Emergence is rendered by letting node properties interact through the physics of the layout.

The renderer only needs to know four things and one process. Every topology from any domain, if the adapter produces the primitive mapping, renders without the renderer knowing anything about the domain.

That is the claim. We have not yet tested it.

---

*This paper records a conversation between Harold Young and Claude (Opus 4.6), 2026-05-10 to 2026-05-11. The conversation is ongoing. The categories are provisional. We are landing here only to take a breath.*
