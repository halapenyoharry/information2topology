# Edge Category Typology

**Status**: Normative for all hypergraphs produced by i2t adapters.
**Version**: 0.1
**Date**: 2026-05-11
**Companion to**: [`../hypergraph.topothink.spec.md`](../hypergraph.topothink.spec.md)

## Premise

Every edge in an i2t hypergraph belongs to **exactly one of four categories**, identified algorithmically from what the edge asserts. The category drives visualization (each category gets its own visual idiom, see below) and supports filtering, query planning, and reasoning at extract time.

**The four categories work without reification.** No relation-as-node is created to make the categories fit. A marriage is an interactivity edge between two persons, not a Marriage node containing two members.

## The four categories at a glance

| Category | One-line definition | Visual idiom |
|---|---|---|
| **Containment** | Y encloses X along some named dimension | Nested regions; X drawn inside Y's area |
| **State change** | A transition along time (or another changing attribute) from one state to another | Positional flow, gradient, motion |
| **Interactivity** | An active channel between entities; something propagates (force, data, signal, communication) | Shared visual field, overlap, blend |
| **Reference** | A static pointer or comparative claim that doesn't transmit anything | Floating marker, callout, low visual weight |

## Decision procedure (algorithmic)

Given an edge with predicate P and its incidences, apply these steps in order. The first match wins.

1. **Does P assert a transition over time, from one state to another?**
   Test: would removing this edge mean a temporal arrow is also removed? Is there a from-state and a to-state asserted by the source?
   YES → **state change**
   NO → continue

2. **Does P assert that one end encloses another along a named dimension (spatial, temporal, set-membership, type-hierarchy)?**
   Test: is there asymmetric enclosure (X is in Y, Y is not in X along the same dimension)? Does removing X from Y leave Y diminished in a part-whole sense? Is Y a set/region/interval with a boundary, not just a metric?
   YES → **containment**
   NO → continue

3. **Does P represent a channel where something propagates between the ends — force, data, signal, energy, communication?**
   Test: can you imagine something flowing across the edge? Is the edge a channel rather than a label?
   YES → **interactivity**
   NO → continue

4. **Default (edge is a static pointer or comparative claim, no flow, no transition, no enclosure):**
   → **reference**

```json
{
  "decision_tree": [
    {"step": 1, "category": "state_change", "test": "asserts transition over time"},
    {"step": 2, "category": "containment", "test": "asserts asymmetric enclosure along a named dimension"},
    {"step": 3, "category": "interactivity", "test": "represents a channel where something propagates"},
    {"step": 4, "category": "reference", "test": "default: static pointer or comparative claim"}
  ]
}
```

## Operational definitions

### Containment

**What the edge represents.** An assertion that one end (Y) encloses the other (X) along a specific dimension. The edge captures that X exists within Y's extent.

**Required criteria.**
1. **Asymmetric enclosure** — X is in Y; Y is not in X along the same dimension.
2. **Named dimension** — the dimension of enclosure is identifiable: spatial, temporal, set-membership, type-hierarchy, conceptual subsumption.
3. **Part-whole flavor** — removing X from Y is a meaningful operation. Y has an extent; X occupies some portion of it.
4. **Set or region, not metric** — Y is a bounded set/region/interval, not a coordinate space.

**Distinguishing from reference.** Containment uses sets and boundaries; reference uses metrics and coordinates. "Apple is in the fruit category" is containment because *fruit category* is a set with a membership boundary. "Apple is heavier than orange" is reference because *heavier-than* uses the weight metric to compare two positions.

**Visual idiom.** Y is drawn as an enclosing region. X is drawn inside Y. No line connects them; the enclosure is the relation.

**Example predicates.**
- `member_of` (Y as set/category)
- `scene_contains`, `chapter_contains` (narrative containment)
- `during` (Y as a time interval enclosing X)
- `inside`, `located_in` (spatial enclosure)
- `subset_of` (set containment)
- `is_a_kind_of` (type hierarchy enclosure)

**Counterexamples** (look like containment but aren't):
- `married_to` — no enclosure; bilateral relation → interactivity
- `older_than` — metric comparison, no set with boundary → reference
- `next_paragraph` — temporal succession, not temporal enclosure → state change

### State change

**What the edge represents.** An assertion that a transition occurs along time (or along some other attribute that changes over time). The edge captures the from-state and to-state, with directionality.

**Required criteria.**
1. **Time-keyed** — the relation requires a before/after distinction.
2. **Directionality** — there is a from-state and a to-state. The arrow is intrinsic.
3. **Asserted by the source** — the text reports the transition. We do not impose reader-state-change as state change unless the text claims it. ("p implies q" is reference; "after accepting p, the believer becomes Christian" is state change because the text claims the transition.)

**Distinguishing from interactivity.** State change is the *event of transition* (discrete, time-keyed). Interactivity is the *channel of ongoing flow* (continuous, may be in equilibrium).

**Distinguishing from containment.** "During" is containment (temporal enclosure, no transition). "Before/after" is state change (temporal succession, arrow present).

**Visual idiom.** Positional flow or motion — gradient between states, glow trail, animated transition. Direction implied by visual gradient rather than drawn as an arrowhead.

**Example predicates.**
- `causes`, `because_of`
- `transforms_into`, `evolves_into`, `becomes`
- `next_paragraph`, `precedes`, `follows`
- `derives_from`
- `supersedes` (the prior entity's status changes)
- `decays_to`

**N-ary case.** A causal chain `a → b → c → d` can be one edge with sequential roles on incidences (`predecessor`, `intermediate`, `intermediate`, `successor`). A reaction with multiple reactants and products is one state-change edge with role-distinguished members.

**Counterexamples:**
- `during` — temporal enclosure, no transition → containment
- `simultaneous_with` — co-occurrence, no transition → reference
- `married_to` — ongoing, not a single transition → interactivity

### Interactivity

**What the edge represents.** An active channel between entities through which something propagates: force, data, signal, energy, communication, attention.

**Required criteria.**
1. **Channel-shaped** — the edge represents a path of transmission, not a label.
2. **Something propagates** — force (gravity, impact), data (function call, pipeline stage), signal (utterance, broadcast), energy (chemical bond formation, heat exchange), communication (dialogue, message).
3. **Does not require state change** — transmission may be in equilibrium (gravity between stable orbiting bodies). The interactivity is the channel itself, not its downstream effects.

**Distinguishing from reference.** Interactivity is an active channel; reference is a passive label. If you can imagine something flowing across the edge, it's interactivity. If the edge is just a pointer that says "this connects to that," it's reference.

**Distinguishing from state change.** Interactivity is ongoing flow; state change is a discrete transition. A punch is both (force transmitted, target's state altered) — see *Mixed-mode edges* below.

**Visual idiom.** Shared visual field — overlapping color, animated particle flow, gradient blend at the interface. Both ends visibly affecting the visual space around each other. No arrow.

**Example predicates.**
- `married_to`, `partners_with`, `cooperates_with`
- `gravitates_toward`, `attracts`
- `depends_on`, `imports`, `calls` (at runtime, control/data flow)
- `speaks_to`, `addresses`
- `catalyzes`
- `attacks`, `defends_against`
- `binds_to` (chemical)
- `trades_with`

**N-ary case.** A meeting with multiple attendees, a multi-party negotiation, a group conversation — all interactivity hyperedges with each member having a participation role.

**Counterexamples:**
- `criticizes_idea` where the idea cannot receive — nothing propagates → reference
- `cites` — static pointer, no flow → reference
- `before` — temporal sequence, no channel → state change

### Reference

**What the edge represents.** A static pointer or comparative claim that does not transmit anything and does not change the target.

**Required criteria.**
1. **Passive** — nothing flows across the edge.
2. **Target unchanged** — the target's state, attributes, and position are unaffected by the relation.
3. **Often a claim** — comparative ("X is heavier than Y"), about-ness ("X is about Y"), citation ("X mentions Y"), or similarity ("X is analogous to Y").

**Distinguishing from containment.** Reference uses metrics; containment uses sets. "X is in the heavy class" is containment (the class is a set with a boundary). "X is heavier than Y" is reference (compares two positions on the weight metric).

**Distinguishing from interactivity.** Reference labels; interactivity transmits. If nothing propagates and the target is unaffected, it is reference even if the source has strong valence toward the target (Camus's criticism of nihilism is reference, because nihilism receives nothing).

**Visual idiom.** Floating marker, callout, or pointer with low visual weight. References should not dominate the visual field; they are noise relative to the relations that actually do something.

**Example predicates.**
- `mentions`, `cites`, `references`, `quotes`
- `analogous_to`, `similar_to`, `differs_from`
- `older_than`, `heavier_than`, `larger_than` (comparative metrics)
- `simultaneous_with`, `adjacent_to`, `north_of` (comparative positions)
- `is_about`, `documents`
- `contradicts` (proposition pointing at another with negative valence)
- `p implies q` (in static logic — reader-belief transitions, if asserted by the text, would be state change)

**N-ary case.** A group analogy ("these three philosophers all reach for the same idea"), a co-citation cluster, a similarity ranking with multiple members.

**Counterexamples:**
- `member_of` — enclosure in a set → containment
- `speaks_to` — utterance transmission → interactivity
- `causes` — temporal transition → state change

## What stays outside the four

### Identity / equivalence

`same_as`, `equals`, `is_identical_to` are not edges in the usual sense — they are **graph rewrites** asserting that two nodes should be collapsed into one. Acting on them modifies the graph rather than adding to it. Treat as a separate operational concern: encode them in metadata or in a separate `identifications` list, not as edges in the four categories.

Edge case: a *contested* identity claim (where the identity itself is disputed and shouldn't yet collapse) can be encoded as a reference edge with predicate `claimed_identical_to`. The reference category is the right home because such an edge is making a claim without acting on it.

### Mixed-mode edges (secondary tag)

Some edges legitimately carry facets of multiple categories. A punch transmits force (interactivity) AND changes the target's state (state change). Catalysis involves an interactive catalyst and a state-changing reaction.

The convention:
- Pick the **primary** category by what dominates the topology of the edge (the rendering decides which visual idiom takes precedence).
- Add `attrs['i2t:edge_category_secondary']` with the secondary category, if it matters for downstream consumers.

In practice, most edges land cleanly in one category. The mixed-mode tag is for the few cases where ignoring the second facet would lose information.

## No-reification constraint

The four categories work *without* introducing relation-as-node entities. This is a deliberate constraint.

**What this means in practice.**

- `married_to` between Bob and Jane is one interactivity edge between two nodes. We do **not** create a Marriage node containing Bob and Jane.
- `case_b_event` from the Fanon corpus (where multiple participants are involved in a single event) is an n-ary state-change edge with role-distinguished members. We do **not** require the event to be a node-and-edge simultaneously. The reified-edge pattern in the i2t spec is *available* but not required; the four-category system is the default.
- A meeting attended by five people is one n-ary interactivity edge with five member-incidences, each carrying a role. We do **not** make the meeting a node.

**Why no reification.**

1. **Avoids metaphysical imports.** Making a Marriage node implies that the marriage has its own existence, attributes, and relations. Unless the source text asserts this (Marriages-as-entities in a legal corpus, for instance, where contracts ARE entities), we are imposing structure the text doesn't claim.
2. **Visual category replaces semantic node.** The interactivity category communicates "Bob and Jane are in an active relationship" via rendering. The same information that a Marriage node would carry is encoded by the category, not by an extra entity.
3. **Reduces node count.** Reification multiplies entities. The four-category system keeps the graph proportional to what the text names.

**When reification is allowed.** Only when the source text itself treats the relation as an entity. Legal corpora that talk *about* contracts (their dates, jurisdictions, dissolutions) need Contract nodes because the text references those contracts as entities. The i2t spec permits reification (S4); this typology constrains it to source-driven cases.

## Encoding in the i2t hypergraph format

Add to every edge's `attrs`:

```json
{
  "id": "edge:bob-jane-marriage",
  "directed": false,
  "attrs": {
    "i2t:predicate": "married_to",
    "i2t:edge_category": "interactivity",
    "i2t:edge_category_secondary": null
  }
}
```

Values for `i2t:edge_category`:
- `"containment"`
- `"state_change"`
- `"interactivity"`
- `"reference"`

Values for `i2t:edge_category_secondary` (optional, when mixed-mode):
- same vocabulary
- `null` (default) when the edge is single-category

## Worked classifications

Common predicates run through the decision procedure:

| Predicate | Category | Reasoning |
|---|---|---|
| `member_of` | containment | Y is a set/category enclosing X |
| `scene_contains` | containment | Scene encloses paragraphs along narrative dimension |
| `during` | containment | Y is a time interval enclosing X |
| `inside` | containment | Spatial enclosure |
| `subset_of` | containment | Set enclosure |
| `is_a_kind_of` | containment | Type-hierarchy enclosure |
| `causes` | state change | Temporal transition with arrow |
| `next_paragraph` | state change | Reader-attention transitions in time |
| `transforms_into` | state change | Explicit transition |
| `supersedes` | state change | Prior entity's status changes |
| `derives_from` | state change | Origination via transformation |
| `married_to` | interactivity | Bilateral channel, no node-reification |
| `gravitates_toward` | interactivity | Force propagates |
| `depends_on` | interactivity | Control/data flow at runtime |
| `speaks_to` | interactivity | Utterance transmitted |
| `catalyzes` | interactivity | Acceleration transmitted (primary); reaction state-changes (secondary) |
| `attacks` | interactivity | Force transmitted (primary); state change if damage results (secondary) |
| `mentions` | reference | Static pointer, no flow |
| `cites` | reference | Static pointer |
| `analogous_to` | reference | Comparative claim, no transmission |
| `older_than` | reference | Metric comparison |
| `adjacent_to` | reference | Comparative spatial position |
| `simultaneous_with` | reference | Comparative temporal position |
| `is_about` | reference | Aboutness pointer |
| `contradicts` | reference | Proposition points at another |
| `same_as` | (outside the four) | Graph rewrite — identity, encode separately |

## Notes on application

- **The text drives the category.** Apply the decision procedure to what the source text asserts, not to what you interpret about reader cognition or downstream effects. "p implies q" in a logic text is reference; "the believer becomes Christian after accepting p" in a theological text is state change.
- **N-ary edges classify the same way.** Arity is independent of category. A two-member containment edge and a fifty-member containment edge are both containment.
- **Per-view classification is acceptable.** The same underlying edge may classify differently in a static analysis view vs a runtime view (e.g., `imports` static = reference; `imports` runtime = interactivity). Document which view the graph instantiation represents.
- **When uncertain, default to reference.** Reference is the catch-all for edges that don't clearly transmit, transition, or enclose. Better to under-claim than to over-classify.

## Open questions

- **Comparative containment** edges like "X is a stricter subset than Y" — these compare two containment relations rather than two entities. Current call: reference, because the comparison is about two relations rather than enclosure. Worth revisiting if these come up frequently.
- **Self-edges** (X relates to itself) — currently rare in i2t practice. If they appear, the category applies the same way: a self-state-change is a node's transition; a self-reference is a node pointing at itself; etc.
- **Higher-order edges** (edges between edges, allowed by i2t spec S4 reification) — when reification is source-driven and present, the higher-order edges classify under the same four categories as ordinary edges. The edge-as-node is treated as a node for classification purposes.
