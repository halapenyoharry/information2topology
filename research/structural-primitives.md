# Structural Primitives

Four. Everything else is weight, direction, and axis.

---

## 1. Nested Containment

inside / outside, recursively. A is inside B is inside C, and the nesting depth IS information. Remove the container, contents lose context. Directed, transitive, antisymmetric.

## 2. State Change (over time)

A becomes B. Location, size, shape, content, any axis can change. Pure sequence is state change at weight zero (ordering without transformation). Metamorphosis is state change at maximum weight. Time is baked in, not separate.

## 3. Interactivity

Things doing things to each other. Giving, taking, exchanging, pushing, pulling, cooperating, opposing. Association is low-intensity interaction. Opposition is interaction with negative valence. Flow (input/output across a boundary) lives here. Directionality and sign are weights, not separate primitives.

## 4. Reference

Pointing at something without enclosing it, changing it, or exchanging with it. Attention, citation, allusion, dependency. Directed, not symmetric.

---

## Emergent (not primitives, not edges, lives in the rendering)

**Similarity:** computed from property overlap during rendering. Two nodes with similar attrs are placed near each other. Nobody declares it.

**Equivalence:** a declared reference where the weight is "this is the same thing."

**Boundary / Overlap:** when containment regions share nodes, the viewer renders the intersection.

**Field effects:** when nodes have intensive properties (mass, charge), interactions emerge from proximity during rendering.

**Stable points:** positions where fields balance. Emergent from nested, weighted containment.

Emergence is in the rendering. Understanding is in the viewing.

---

## Compounds

| Predicate     | =                                                            |
| ------------- | ------------------------------------------------------------ |
| foreshadows   | reference + state change                                     |
| loves         | reference + interactivity (positive)                         |
| hates         | reference + interactivity (negative)                         |
| parodies      | reference + interactivity (negative) + similarity (emergent) |
| betrays       | reference + interactivity (negative) + state change          |
| inspires      | reference + state change                                     |
| haunts        | reference + state change + interactivity (negative)          |
| employs       | nested containment                                           |
| co-authored   | interactivity (collaborative)                                |
| borders       | emergent (overlapping containment)                           |
| causes        | state change                                                 |
| depends-on    | reference                                                    |
| is-a          | nested containment                                           |
| resembles     | emergent (similarity)                                        |
| contradicts   | interactivity (negative)                                     |
| cites         | reference                                                    |
| becomes       | state change (high weight)                                   |
| follows       | state change (zero weight, pure ordering)                    |
| flows-through | interactivity (directional, across boundary)                 |

---

## What this replaces

An earlier list had seven, then six primitives derived from graph theory (containment, sequence, boundary, similarity, opposition, association, reference). Testing against real domains (the solar system, family structures, literary allusion, gravitational physics, stack ranking, conversation structure) collapsed the list:

- Boundary moved to emergent (visible when containment regions overlap)
- Similarity moved to emergent (computed from property overlap during rendering)
- Sequence folded into state change (sequence is state change at weight zero)
- Opposition folded into interactivity (opposition is interaction with negative valence)
- Association folded into interactivity (association is low-intensity interaction)

The earlier list described how things STAND to each other. This list describes what things can DO. Nest, change, interact, refer. Four verbs.

---

## Open questions

- Are we sure similarity is always emergent? Can the renderer reliably compute it from properties alone?
- Is dependency reference, or reference + containment? (removing the dependency breaks things, which sounds like containment)
- Can interactivity cover everything from co-occurrence to warfare? Is it too broad?
- Does state change need to be explicitly temporal, or can it be atemporal? (A mathematical proof transforms premises into conclusions, is that state change?)
- What are the axes of state change? Location, size, shape, content, what else?
- Are four too few? Test with hard cases.

---

*Four primitives. Closer, not final. We are still breathing.*

*This list records a conversation between Harold Young and Claude (Opus 4.6), 2026-05-10 to 2026-05-11. The conversation is ongoing.*
