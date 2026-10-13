# Berry Thief: annotation record

Gold-standard extraction of *The Epic of Elinor Jones*, Act 1, Chapter 1 ("Berry Thief"), built by hand against the i2t v1.4.0 typology and audited against an independent model extraction. This file records every judgment call so the gold can be disputed line by line.

Source: `berry-thief.source.md` (sha256 `050e8dd9…ad62`, the production chapter file including the Editor's Note). The prose is used exactly as it exists; nothing in it was corrected.

## Method

Two annotators worked from the same file without seeing each other's output:

- **A, by hand**: `berry-thief.hand.relations.json`, written relation by relation from the text (71 nodes, 116 relations).
- **B, Sonnet 5.5**: `berry-thief.sonnet-5.5.relations.json`, one pass of the Exoskeleton extraction prompt (52 nodes, 75 relations, $0.36).

Then A was audited against B. Every disagreement was resolved by rereading the passage and the typology, and the result is the gold: `berry-thief.relations.json` (70 nodes, 117 relations). The canonical hypergraph and the dyadic projection are generated from it by code (`berry-thief.hypergraph.topothink.json`, `berry-thief.normalized-dyadic.json`), so the three files never drift.

Evidence discipline held for all three documents: 0 of 310 quotes failed verbatim verification against the source.

## Agreement between the two annotators

Matching on participant set, then on category and mode:

| | count |
|---|---|
| Same participants, same category, same mode | 35 |
| Same participants, different category or mode | 13 |
| Only B (Sonnet) | 27 |
| Only A (hand) | 77 |

The "only" counts overstate the disagreement. Most are the same relation at different arity: A attached channels (`phone`, `reddit`) and instruments (`arrow`, `diamond sword`, `collecting bag`) as participants; B left them out. The gold keeps them: the typology's own worked example gives speech acts a `channel` role, and a weapon or a waypoint is part of the relation, not decoration.

The 13 classification disagreements are the useful ones. Four went B's way, nine A's.

## What Sonnet caught (adopted into the gold)

1. **Co-residence direction is contested.** "his mom's rooms, unless he was being honest when he said she lives with him and not the other way around." A had encoded this as contested *ownership* of the rooms. B encoded contested *living-with*. The text contests who lives in whose house, which is a containment edge whose **direction** is disputed. The gold carries both: two `owns` (reference, contested) and two `lives_in` (containment, contested, one per version). This is a case the typology does not yet cover: `claimed_identical_to` handles a disputed identity, nothing handles a disputed direction. Candidate for Section 9.
2. **Zayne's instruction to Lillian is told two ways.** Lillian: "Zayne has informed me not to answer that question anymore." Zayne: "I said, if Eli asks that question make me sound cool or something." A had only Zayne's version, as attributed. These are two accounts of one command, so the gold records two `commands` relations, mode `contested`, `asserted_by` lillian and zayne.
3. **The manager relation is asserted.** A had only the hypothetical chat. "her manager" asserts that Eli has one: `manages` (interactivity, constitutive, asserted) is added; the chat stays hypothetical.
4. **The pots hold the samples.** A had the move into the pots but not the resulting containment. Added.

Also adopted on reflection: B flagged the rented room and the apartment as `claimed_identical_to` where A had merged them as one node. The text says "rented her the room above a garage" and elsewhere "the apartment"; that they are the same place is implied, never stated. The identity rule says keep two nodes and flag. Split, with the flag.

## Where the hand extraction was kept over Sonnet

- **Zayne's account of his week is `attributed`, not `asserted`.** Selling the car, moving the farm, ordering GPUs, signing the contract, driving his mom: all in Zayne's dialogue, nothing confirmed by narration. B marked them asserted; the mode rule says attributed. This is the strict reading and it is the one the gold takes, but it is the first thing to revisit if the rule proves too strict for dialogue-heavy fiction: nearly everything characters say about themselves would become `attributed`.
- **Eli and Rook: `lives_with`, not `owns`.** B used `owns` (reference). The text never calls Rook "her dog" or a dog at all; it says she "hated leaving Rook alone." A constitutive companion relation fits the cut test (sever it and Rook stops being Eli's companion). Possession-as-reference is kept where the text is possessive: `owns` zayne → lillian ("Zayne's AI") is in the gold, per the typology.
- **Lillian declining to answer** is one `declines` act (A), not a negated `answers` (B). Same content; a speech act that happened should not carry mode `negated`.

## Self-corrections (A violated its own rules)

Dropped: `rides` (bike), `steadies` (the wobbling plant), `showers`, `hides_under` (the table is not a node), `patronizes` (the Taco Bell joke), and `elected` with Eli as "observer" (an observer is not a participant). All passing actions or non-relations. The Taco Bell node went with its relation.

Narrowed: `licks` no longer lists the berries as consumed (it is juice and blood on a shirt); `explodes` no longer names Eli's avatar as the victim (the creeper paragraph is about "the player" in general).

Fixed: `criticizes` zayne → president lacked its addressee. Zayne says it to Eli, so it is `complains_to` with speaker, addressee, topic.

## Judgment calls that stand, and why

- **The theft is foretold.** "didn't plan on stealing a super intelligent machine, but life is mostly made up of things people never planned on doing." Two relations: `plans_to_steal` negated, `steals` foretold. The negation covers only the plan; the second clause implies the event.
- **Two frames.** The Editor's Note is an author-given frame that contains the chapter; the narrator who says "We digress" and "now back to the epic" is a second frame, speaking from a later era. Both are `frame` nodes containing `source-text`.
- **Three AIs, two identity flags.** The phone AI (scene 1), Lumen (scene 2) and Schpongle (scene 2) are kept separate. Phone AI = Lumen is likely ("The AI she used daily, who she nicknamed Lumen"); Schpongle = Lumen is possible (Lumen designed the routine "for Rook's food"); neither is stated. Both are `claimed_identical_to`, mode `unresolved`.
- **Minecraft is a place.** Avatars and mobs are contained in it; the skeleton attacks Eli's *avatar*, Zayne's *avatar* slices the skeleton, and Eli *controls* her avatar. The one edge that crosses the boundary is Eli warning Zayne about the creeper, which is a speech act between the people with the mob as topic.
- **Attacks are mixed-mode.** `attacks` is interactivity with `secondary_category: state_change`, per the typology's punch example.
- **Lillian named herself.** A self-edge, `names` lillian → lillian (state change). The typology allows self-edges and this is the first one in the corpus.
- **The Lumen chain is spelled out.** `suggests` (fewer sensors) → `saves_money` → `realizes` (AI changes lives), plus `thrives_because_of` (plants ← automation). The text asserts each link with a causal connective.
- **Zayne's causal chain, attributed.** car sold → room in the garage → GPUs ordered → paid for by the contract (`enables`, attributed; `funds`, foretold).
- **Diane and Dick are two nodes.** No group node. The rental is one four-party relation (two landlords, tenant, property).

## Open questions this chapter raises for the typology

1. **Disputed direction** of a containment or interactivity edge (who lives with whom). `contested` on two edges works but loses the fact that they are rival versions of one edge.
2. **Dialogue and `attributed`.** Whether a character's uncontradicted statements about themselves should default to attributed or asserted. The gold follows the rule; the rule may need a fiction clause.
3. **Channels as participants.** The phone and Reddit appear as `channel` participants on speech acts. If channels become common, a dedicated incidence attribute may serve better than a role.

## Files

| File | What |
|---|---|
| `berry-thief.source.md` | The chapter, verbatim |
| `berry-thief.hand.relations.json` | Annotator A, pre-audit |
| `berry-thief.sonnet-5.5.relations.json` | Annotator B |
| `berry-thief.relations.json` | **Gold**, relation-list form (the edit surface) |
| `berry-thief.hypergraph.topothink.json` | Gold, canonical hypergraph (generated) |
| `berry-thief.normalized-dyadic.json` | Gold, dyadic projection for Exoskeleton (generated) |
