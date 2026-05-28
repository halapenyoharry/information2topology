# The State-Change Layer: Token-DAG and Type-Quotient

**Status:** Working paper. Validated on the Wizard of Oz fixture (v2). Ready to distill into the whitepaper.
**Date:** 2026-05-28
**Companion:** [`../docs/edge-categories.md`](../docs/edge-categories.md) (the four-category typology this extends), [`../adapters/README.md`](../adapters/README.md) (the source/canonical/projection taxonomy this reuses).
**Worked fixture:** [`../data/wizard-of-oz.v2.hypergraph.topothink.json`](../data/wizard-of-oz.v2.hypergraph.topothink.json)

## 1. The claim

The four-category typology classifies each *edge* by what it asserts. But **state-change** has a structural property the other three do not, and it only becomes visible when you stop looking at individual edges and look at the *layer* — the subgraph of all state-change edges assembled together.

> The state-change layer, restricted to concrete event/state **tokens** indexed by actual time, is a **directed acyclic graph** — the covering relation of a temporal partial order. A topological sort of it recovers "the order in which things occurred." Collapsed to **types**, the same layer becomes a **state-transition system** that may contain cycles, and that collapse is a lossy quotient.

Two graphs, not one. Conflating them is a category error of exactly the kind the project exists to prevent.

## 2. Edge category is local; DAG-ness is a property of the layer

"Is it a cycle or a DAG?" is **not** an edge-category question. Each individual edge — `evaporation → condensation`, `the_cyclone → killing_witch_east` — is a state-change edge: it asserts a transition over time, which is the category's defining criterion. The acyclicity is a property of the *assembled layer* and of *which level you read it at*. So the typology is untouched: state-change remains the edge category. What this paper adds is a property of the layer those edges compose.

## 3. The two presentations

| | **History / trajectory** | **Transition system** |
|---|---|---|
| Nodes | dated occurrences (token-level) | state-*types* |
| Time | preserved — the arrow is real | abstracted into a recurring pattern |
| Topology | **DAG** (a chain when the narrative is linear) | may be **cyclic** |
| What it is | what actually happened, in order | the space of states and their habitual transitions |
| Faithful? | yes — every occurrence kept | lossy — occurrences collapsed |
| Standard name | trajectory, run, orbit, execution trace | state machine / automaton / phase portrait; an ENSO-style oscillator or Markov chain |

**The relationship is a quotient.** The transition system is the history-DAG quotiented under "same type": identify every El-Niño occurrence (or every "obstacle encountered" episode) as one node, and the timeline collapses into a loop. A quotient discards exactly the distinctions a faithful record keeps — *niño-1999* vs *niño-2010* — because it declares them the same node. The cycle is not a richer view of the history; it is a lossy compression of it.

**This is a projection in the precise sense the project already defines.** The type-quotient cycle is to the token-level state-change history what `normalized-dyadic` is to the canonical hypergraph: a more legible, strictly lossier view that must not be mistaken for the source of truth. It would carry the metadata tag `i2t:relation_to_canonical: type-quotient`. Same faithfulness-versus-legibility tension as the rest of the pipeline, one level up.

**Direction of primacy flips by domain.** In empirical/historical domains (weather, biography, a novel's plot) the history is primary and the cycle is an abstraction derived from it. In designed/normative domains (a traffic light, a protocol, the rules of a game) the transition system is the specification and the histories are runs of it. Either way the token/type split holds, and either way a specific run is a DAG.

## 4. Reification is earned by reference

The no-reification constraint (edge-categories.md) forbids reifying a relation into a node *by reflex*. Operationally:

> Reify an edge (let its id also be a node) only if another edge references it as a node. Edges already carry their own `attrs` (spec S7), so reification buys nothing except the ability to be a **target**. If nothing targets it, the reification is inert.

The Wizard of Oz fixture (createdDate 2026-05-04, pre-typology) reified seven narrative events. Six were referenced by **zero** edges — inert reification, reflexive promotion of relations to entities. This is the failure mode the constraint names.

The fix is not to delete the reification. It is to ask whether the events *should* be referenced — and for a plot, they should: their order is part of the structure. **Wiring the token-level history-DAG (pairwise `precedes` edges) is what references the events, and that reference is what justifies their reification.** The events stay reified, legitimately, the moment the DAG points at them.

```
the_cyclone → killing_witch_east → melting_witch_west → unmasking → balloon_departure → homecoming
```

(Confirmed acyclic; topological sort returns exactly this story-time order.)

## 5. The four-category audit catches "event ≠ state-change"

Of the seven Oz "events," the decision procedure reclassifies one. `wizard_appearance_each` ("Oz could take on any form he wished … a fairy … a ferocious beast …") asserts no transition over time — it is a **one-to-many deception channel** from the wizard to each petitioner. That is **interactivity**, not state-change. It therefore does **not** belong on the history-DAG, and nothing references it, so it is correctly de-reified to an edge-only hyperedge. The discipline catches, on its own, the reflex of treating every "event" as a temporal transition.

## 6. Oz v2: the numbers

Full current-schema re-extraction, `data/wizard-of-oz.v2.hypergraph.topothink.json` (1,202 nodes / 1,213 edges / 3,542 incidences):

| Edge category | Count | Notes |
|---|---|---|
| state_change | 1,119 | dominated by 1,094 `next_paragraph` (reader-attention transitions) + the plot spine + transformation events |
| interactivity | 27 | dialogue, gifts, governance, the deception channel |
| containment | 51 | `chapter_contains`, `member_of_act`, `act_contains` |
| reference | 16 | desire (`wants`, `covets`), comparison, possession, exemplification |

95% of edges (the 1,094 paragraph-sequence + 51 containment) are structurally determined by predicate and assigned by rule with high confidence. The remaining ~63 semantic edges were judged individually against the decision procedure.

## 7. The near-degenerate finding

Oz's plot-spine history-DAG is a **chain** — a linear total order. No two spine events share a type, so its **type-quotient is trivial: no cycle.** Oz is the *near-degenerate case*. That is itself the useful result: it demonstrates the token-DAG cleanly, and it proves *why a second fixture is required* to exhibit the cyclic type-quotient. The only recurrence in Oz lives at the episodic obstacle level (Kalidahs → fighting trees → hammerheads, a repeated "threat encountered → threat overcome" type), not on the main spine. A novel built on recurrence — a character who loops a behavior, seasonal time, a returning motif — is the needed companion fixture, and is the cleanest way to show a nontrivial quotient cycle against a token-DAG that is genuinely acyclic underneath.

## 8. The inter-annotator divergence set

Thirteen edges were flagged `i2t:edge_category_review: true` — genuinely ambiguous calls, defaulted but not asserted: `ward_of`, `owned`, `owns`, `leads_to`, `requires`, `instantiates`, `embodies`, `cannot_kill_due_to_kiss`, `obstructs`, `constrains`, `blocks_path`, `rules`, `reveals_power_of`. Each sits on a real boundary — possession-status vs. set-containment (`owns`), a road as spatial reference vs. a channel travel flows through (`leads_to`), a precondition vs. a runtime dependency (`requires`).

These are not noise to be cleaned up. They are precisely the edges where two independent annotators would diverge, and so they are the natural test set for the **Inter-Annotator Convergence Test** the whitepaper proposes (Section 8). The empirically-grounded edges (the 1,145 structural + the unambiguous semantic) are where annotators *must* converge; the 13 are where divergence is informative. Recording the flag at extraction time turns the convergence test from a thought experiment into a measurable protocol over a labeled set.

## 9. To fold into the whitepaper

A distilled version of §§3–4 belongs in the whitepaper's treatment of the state-change category and the emission/projection discussion: the two presentations, the quotient-as-projection framing, and reification-earned-by-reference. The Oz spine (§4) is a compact second worked example alongside Camus. §8 strengthens the existing Inter-Annotator Convergence Test by giving it a concrete labeled divergence set. This would be a substantive v1.3.0, not an editorial patch — flagged for author review before promotion.
