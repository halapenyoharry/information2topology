---
title: "Chapter to Benchmark: Producing a Gold-Standard Topology from a Single Chapter of Fiction"
parent: "[[information-to-topology-whitepaper]]"
author: "Harold Young"
date: "2026-10-12"
version: "1.0.0"
status: "Released, with open items in Section 8"
license: "CC BY-NC-ND 4.0"
tags: [#i2t, #topothink, #benchmark, #gold-standard, #convergence-test, #edge-typology, #elinor-jones, #evidence-discipline]
links: ["[[information-to-topology-whitepaper]]", "[[edge-categories]]", "[[on-the-categories-of-relationship]]", "[[editorial-discipline]]"]
---

# Chapter to Benchmark: Producing a Gold-Standard Topology from a Single Chapter of Fiction

## Abstract

The i2t method claims that prose carries a recoverable topology and that independent readers recover the same one. Both claims are empirical and both were, until now, untested against a reference anyone could inspect. This paper sets out what a benchmark-grade extraction of a text is, gives the procedure that produces one, and reports the first instance: the opening chapter of *The Epic of Elinor Jones* ("Berry Thief", 14,588 characters), extracted by two annotators working independently from the same pinned file, audited, and published with every judgment call recorded. The result is 70 nodes and 117 relations, 54 of them n-ary, with 0 of 310 evidence quotes failing verbatim verification. The two annotators agreed exactly on 35 relations and differed in category or mode on 13; the audit found 4 errors in the hand extraction and 9 in the model's. Three gaps in the typology surfaced from the text itself and are stated as open questions. The chapter is now the north star against which every extractor, prompt, and model in this project is scored, and the procedure is the template for the rest of the book.

---

## 1. Why a benchmark, and why a chapter

The whitepaper's Central Theoretical Result partitions the method into an evidence side, where claims are checkable, and an interpretation side, where they are not. Extraction quality is an evidence-side claim. It can be measured only against a reference extraction whose own correctness has been argued in public, line by line. Without one, every improvement to a prompt or a model is reported as an impression.

A single chapter is the right unit for the first reference. It is long enough to contain every structure the typology names (containment, state change, interactivity, reference; n-ary relations; foretold and contested claims; narrating frames; a world-within-the-story) and short enough that one person can hold the whole of it and defend every edge. Berry Thief in particular contains, in order: a prolepsis in its first sentence, a constitutive relation (employment), a command whose execution the text denies, a disputed containment, an unresolved identity between three AIs, and a narrator who steps out of the story. A benchmark that covers these covers most of what fiction does.

The chapter is also public. Act 1 of the novel is published, so the source file can be committed verbatim and pinned by hash, and anyone can rerun any extractor against exactly the bytes the gold was built from.

## 2. What benchmark-grade means

An extraction is benchmark-grade when all of the following hold. Each is checkable; the first four by code.

| Criterion | Test |
|:--|:--|
| **Pinned source** | The exact text is in the repository with a content hash. The gold refers to those bytes and no others. |
| **Verbatim evidence** | Every node and every relation carries a quote that appears character-for-character in the source (after normalizing whitespace, emphasis markers, and quote glyphs). Zero failures. |
| **Closed structure** | Every participant resolves to a declared node; every relation has at least two participants; every directed relation has roles on its incidences; the canonical file passes the format's schema and structural validator. |
| **Located** | Every relation records which of the source's own divisions its evidence sits in, and the record agrees with where the quote is actually found. |
| **Typed throughout** | Every relation has exactly one of the four categories and exactly one mode (asserted, commanded, intended, foretold, hypothetical, attributed, contested, negated, unresolved); attributed and contested relations name who asserts them. |
| **Two annotators** | At least two extractions were made independently from the same file, and their agreement is reported. |
| **Audited** | Every disagreement between annotators was resolved by rereading the text and the typology, and the resolution is written down with its reason. |
| **Self-consistent with the rules** | The gold obeys the extraction rules it was scored by (no passing gestures, no speech act without an addressee, no possession as containment, no two named individuals in one node). |
| **Generated forms** | The canonical hypergraph and every projection are produced by code from one edit surface, so the files cannot drift from one another. |

A gold that meets these is not claimed to be *true*; it is claimed to be *defensible at every edge* and *reproducible to the byte*. Those are the properties a benchmark needs.

## 3. The procedure

### 3.1 Pin the source

Copy the production file unchanged into the example directory and record its SHA-256 in every generated file's metadata. For Berry Thief this is the published chapter including its Editor's Note line, hash `050e8dd9…ad62`. The prose is never corrected, even where it is visibly imperfect ("comons", "they they"); a benchmark against a cleaned text would not be a benchmark against the text.

### 3.2 Extract twice, independently

Annotator A extracts by hand from the text, relation by relation, with the typology and the extraction rules open but no model output in view. Annotator B is a model run once over the identical file with the project's extraction prompt. Neither sees the other's output until both are complete.

Both write the same form: a **relation list**, in which each relation is a predicate, a category, a mode, a verbatim quote, and a list of participants each with a role. This is the incidence form of the canonical hypergraph, written flat. It is the right edit surface because it is what a person can read and argue with; the hypergraph and the projections are derived from it.

### 3.3 Verify by code

Before any human audit, code checks both extractions for the first four criteria of Section 2: every quote found verbatim, every participant declared, every locus consistent with the quote's position. Anything that fails here is an error, not a disagreement, and is fixed or dropped before comparison.

### 3.4 Diff

Align B's nodes to A's by label and alias. Then match relations on participant set. Each of B's relations lands in one of four bins: same participants and same category and mode (agreement); same participants, different category or mode (classification disagreement); no participant match (B only). What remains of A is A only.

The "only" bins overstate disagreement when the annotators differ in arity. A attached channels (the phone, Reddit) and instruments (an arrow, a diamond sword, a collecting bag) as participants; B did not. These are the same relations at different resolution, and the audit treats them as such.

### 3.5 Audit every disagreement

For each classification disagreement and each one-sided relation, reread the passage and apply the typology's tests (the decision procedure in `edge-categories.md`; the constitutive-descriptive cut; the mode definitions). Record the outcome and the reason. The audit also turns on A: an annotator reading their own draft against the rules will find violations, and these are recorded as self-corrections.

### 3.6 Generate and validate

From the audited relation list, generate the canonical hypergraph (edge id `edge:<predicate>/<first participant>`, participants as incidences with roles, mode and evidence and locus as edge attributes), validate it against the schema, and project it to every downstream form with the project's own adapters. Confirm the projection loads in the viewer with no warnings.

### 3.7 Publish the record

Commit the source, both annotators' extractions as they were before audit, the gold, the generated forms, and an `annotations.md` that holds the agreement counts, every adopted and rejected change with its reason, the judgment calls that stand, and the open questions. The pre-audit extractions are kept so the convergence numbers can be recomputed by anyone.

## 4. The Berry Thief instance

### 4.1 Counts

| | Annotator A (hand) | Annotator B (Sonnet 5.5) | Gold |
|:--|--:|--:|--:|
| Nodes | 71 | 52 | 70 |
| Relations | 116 | 75 | 117 |
| Relations with 3+ participants | 53 | 39 | 54 |
| Modes in use | 9 | 9 | 9 |
| Quotes failing verification | 0 | 0 | 0 |
| Cost | — | $0.36 | — |

Gold by category: containment 16, state change 36, interactivity 49, reference 16. Gold by mode: asserted 80, attributed 13, contested 6, intended 5, hypothetical 4, unresolved 3, foretold 2, negated 2, commanded 2.

### 4.2 Agreement

| Bin | Count |
|:--|--:|
| Same participants, category, and mode | 35 |
| Same participants, different category or mode | 13 |
| B only | 27 |
| A only | 77 |

Of the 13 classification disagreements, four were resolved in B's favour and nine in A's.

### 4.3 What the model caught

Four relations the hand extraction had wrong or missing, all adopted:

1. **A disputed direction.** "his mom's rooms, unless he was being honest when he said she lives with him and not the other way around." A had encoded contested *ownership*. B encoded contested *co-residence*. The text contests who lives in whose house: a containment edge whose direction is disputed. The gold carries both readings as `lives_in`, mode `contested`, one per version, with `asserted_by` where the text names the claimant.
2. **A command reported two ways.** Lillian: "Zayne has informed me not to answer that question anymore." Zayne: "I said, if Eli asks that question make me sound cool or something." One instruction, two accounts. Two `commands` relations, mode `contested`.
3. **An asserted constitutive relation.** "her manager" asserts a `manages` edge; A had recorded only the hypothetical chat.
4. **A resulting containment.** The pots hold the samples after the potting. A had the transfer, not the state it produced.

B also flagged the rented room and the apartment as possibly the same place where A had merged them. The identity rule (keep two nodes and flag unless the text *states* identity) favours B, and the gold now splits them with `claimed_identical_to`.

### 4.4 What the hand extraction kept

- **Dialogue as `attributed`.** Zayne's account of his week (selling the car, moving the farm, ordering GPUs, signing the contract) is in his own speech and nowhere confirmed by the narration. B marked it asserted. The mode rule as written says attributed, and the gold follows the rule. This is the first item to revisit (Section 8).
- **Companionship over possession.** B had `owns` for Eli and Rook. The text never says "her dog", or "dog"; it says she "hated leaving Rook alone." The cut test gives a constitutive `lives_with`. Possession-as-reference is kept where the text is possessive ("Zayne's AI").
- **A refusal is an act.** Lillian declining to answer is `declines`, asserted, not `answers`, negated.

### 4.5 Self-corrections

Six relations in A broke A's own rules and were dropped: a bike ride, a steadied plant, a shower, a dog under a table, a joke about Taco Bell, and an election with Eli as "observer". Two were narrowed (what Rook licked; whom the creeper blows up, which the text gives as "the player" in general). One speech act lacked its addressee and was repaired.

### 4.6 Judgment calls that stand

Recorded in full in `annotations.md`. The ones with weight: the first sentence's negated *plan* and foretold *theft* are two relations; the Editor's Note and the digressing narrator are two frame nodes, each containing the chapter; the phone AI, Lumen, and Schpongle stay three nodes with two `claimed_identical_to` flags; Minecraft is a place containing the avatars and mobs, and the skeleton shoots the *avatar*; Lillian naming herself is the corpus's first self-edge.

## 5. Scoring an extractor against the gold

The gold is useful only if a run of any extractor can be scored the same way every time. The protocol:

1. **Run the extractor on the pinned file.** Any output that does not come from exactly those bytes is not scored.
2. **Verify evidence.** Count quotes that fail verbatim verification. Report the rate; relations with unverifiable evidence are excluded from the rest of the scoring and counted as errors.
3. **Align nodes** to the gold by id, label, and alias (the same alignment code the audit used).
4. **Match relations on participant set.** Report four numbers: exact agreement (participants, category, and mode), classification disagreement (participants only), extractor-only, gold-only.
5. **Score the hard cases.** A fixed checklist of the chapter's reading-dependent relations, each yes/no: the foretold theft; Elinor as alias; GhostInTheML as Zayne; an identity flag between the phone AI and Lumen; the commanded feed; the skeleton attacking the avatar and not the person; the contested co-residence; Eli's realization; Diane and Dick as separate nodes; more than one mode in use. These are the relations single-pass small models fail, and they separate reading from pattern-matching.
6. **Report arity.** The share of relations with three or more participants. An extractor that flattens speech acts to speaker-topic pairs will show it here before anywhere else.

Scores already on record for this chapter, from the extractor development that preceded the gold: Sonnet 5.5, one pass, 10/10 hard cases; gemma4 8B, one pass, 0/10; gemma4 with six focused follow-up passes, 0/10 and 155 relations, of which many were invented event-nodes. The gold makes these numbers reproducible rather than anecdotal.

## 6. What the chapter taught the typology

Three questions arose from the text, not from theory, and are placed with Section 9 of the whitepaper.

1. **Disputed direction.** A relation whose participants are agreed but whose direction is contested (who lives with whom) has no representation of its own. Two `contested` edges work but lose the fact that they are rival versions of one edge. The paper's `claimed_identical_to` handles a disputed *identity*; nothing handles a disputed *orientation*.
2. **Dialogue and `attributed`.** Applied strictly, nearly everything a character says about themselves becomes `attributed`, since narration rarely confirms it. The gold follows the rule. Whether fiction needs a clause (uncontradicted self-report in dialogue defaults to asserted, with the speaker recorded) is a decision for the typology, and the two readings are both scorable against this chapter.
3. **Channels as participants.** The phone and Reddit appear as `channel` participants on speech acts. If channels become common across the corpus, an incidence attribute may serve better than a role, since a channel does not take part in the relation the way a speaker does.

## 7. Division of labour, and what it implies for extractors

The audit makes the firebreak concrete at the level of a single chapter. Everything in Section 2 that code checked (evidence, closure, location, generated forms) is the evidence side; it needed no judgment and admits none. Everything the audit argued about (direction, attribution, companionship against possession, which AI is which) is the interpretation side; no string test decides it.

The extractor built alongside this benchmark follows the same line. The model is asked only for what needs reading: which entities, which words assert a relation, who plays what part, what kind of claim it is. Code does the rest: structure from the source's own breaks, ids and aliases, projection, verification, duplicate detection across passes. The gold shows how much of the remaining work is reading: of the 13 classification disagreements between a careful hand and a capable model, every one turned on a sentence's sense, not on a rule that could have been mechanized.

## 8. Open items

- **A third annotator who has not seen the prompt.** Both current annotators share one reading of the typology, because the model's prompt was written by the hand annotator. Convergence measured between them is a lower bound on disagreement. The author of the novel, extracting from the spec alone, is the obvious third.
- **The rest of Act 1.** The procedure is written to repeat. Each chapter adds coverage of structures this one lacks (multiple points of view, letters, a chapter that is itself a document).
- **Encoder-side evidence.** Named-entity, coreference, and quotation-attribution models label spans of the source and cannot paraphrase. They belong on the evidence side by construction and should be scored against this gold on the sub-tasks they cover (entities, aliases, speaker and addressee) before they are wired into the extractor.
- **A regeneration target.** The canonical and dyadic files were generated by a few lines of code run by hand. A Makefile target would make the gold editable by others without that knowledge.

## 9. Files

`data/examples/berry-thief/` in the information2topology repository: the pinned source, both pre-audit extractions, the gold relation list, the generated canonical hypergraph and dyadic projection, `annotations.md`, and a README with the load instructions for Exoskeleton.
