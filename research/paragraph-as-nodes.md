# Paragraph-as-Nodes: Architecture Notes

**Status:** Resolved (2026-04-29). Implementation in `adapters/manuscript_to_hypergraph.py`. Editorial principle in `editorial-discipline.md`.

---

## What's a node? — by source of authority

(From Harry's notes, formalized.)

The book IS the graph. Two distinct sources of node-authority:

### Author-given structure (the writer chose this)
- Acts
- Scenes (partially — sometimes implicit)
- Paragraphs (where the author chose to break)
- Sentences
- Words
- Table of Contents
- Index
- Glossary
- Appendices

These come for free with the source — no interpretation required. The author already named these as structural units. Throwing them away to extract "concepts" loses topology that was already there.

### Reader-identified within author's prose (we name these from the text)
- Character identity
- Character interactions
- Character mentions
- Character actions
- Locations
- Scenes (partially — when not marked, we infer)

These are interpretive, but supported by patterns in the text — character names appear, dialogue tags can be parsed, vocatives are detectable. The text supports the claim even when the claim is ours.

The architectural payoff: **author-given structure becomes nodes-and-edges directly**; **reader-identified structure becomes incidences with roles + attrs** layered on top. Different layers, different commitments to the text. The author's choices stay author-shaped; ours stay marked as ours.

---

## Three primitives, three jobs

- **Vertex (node):** a thing with identity that other things can talk ABOUT.
  - Paragraphs (the author's chosen unit)
  - Characters (have life of their own — name, attrs, arc)
  - Places (named locations the prose references)
  - Themes / motifs (Sisyphus motif, AI hate, etc.)
  - Scenes / chapters / acts (containing structures, reified — same id appears as both node and edge)
  - Sentences and words *could* be nodes too (multi-granularity), with words merging by identity (one `violence` node with `mention_count: 50`); not implemented yet.

- **Edge:** the connection between nodes. Reports what the prose says.

- **Incidence:** the site of one node's participation in one edge. Carries the *role* (text-supported category) and *attrs* (interpretive annotations).

## Editorial discipline (edges report; incidences interpret)

Three layers of commitment to the source text:

1. **Edge label** = pure text. The actual prose excerpt that justified the edge. `"...the rock fell back. ¶ No one called her..."` — the seam itself, not a category name.
2. **Incidence role** = text-supported category. `predecessor` / `successor`, `voice_carrier` / `speaker`, `perspective_lens` / `perspective_holder`. Each role is a category, but it's derivable from a pattern in the text.
3. **Incidence attrs** = interpretive annotation. Reader-imposed. `narrative_significance: "turning_point"`, `confidence: 0.8`. Different readers may disagree; their disagreement lives here.

The edges report. The incidences interpret. See `editorial-discipline.md` for the principle in full.

## Predicate vocabulary (manuscript domain)

Each evidence-bearing edge in the manuscript adapter:

| Predicate         | Source-side role     | Target-side role        | Edge label content |
|-------------------|----------------------|-------------------------|--------------------|
| `next_paragraph`  | `predecessor`        | `successor`             | seam: last words of A + ¶ + first words of B |
| `POV_of`          | `perspective_lens`   | `perspective_holder`    | excerpt around the POV character's name |
| `speaker_of`      | `voice_carrier`      | `speaker`               | dialogue + speech-tag fragment |
| `addressee_of`    | `utterance`          | `addressee`             | the dialogue containing the vocative |
| `introduces`      | `debut_passage`      | `new_arrival`           | excerpt around the first appearance |
| `referenced_by`   | `mention_passage`    | `referent`              | excerpt around the named reference |
| `mentions`        | `mention_passage`    | `mentioned`             | excerpt (places, themes — non-character) |

Structural edges (`scene_contains`, `chapter_contains`, `act_contains`, `member_of_act`) keep simpler shapes — they're pure structure with no text-evidence label needed.

## Multi-granularity (not yet implemented)

Each word that appears in the index/glossary AND has its own life (it's defined, indexed, capitalized, or above some salience threshold) earns node status. Connective tissue (`the`, `and`, `however`) stays as attribute presence/absence on the paragraph, never gets a node.

For each indexed word: the word becomes a node; paragraphs that contain it have edges to it; the index entry has its own edge to the word. The word becomes a HUB connecting paragraphs and the index.

## Federation across readers / Rosetta-stone-as-topology

If multiple readers (or sources) tag the same content, their tags are themselves nodes. A canonical concept (like `violence` or `betrayal`) is a node; each reader's version of the tag is an incidence on the canonical node. Federation through structural alignment, not through ID-merging. Same data, multiple readings layered on top.

---

## Terminology used in this project

A few terms get conflated. Resolved:

- **Incidence** (sometimes mistyped as "indicies" — same word, conventional spelling): the relationship-record between an edge and one of the nodes it touches. `{edge: "...", node: "...", role: "...", attrs: {...}}`. Has its own attributes. Distinct from the edge.
- **Edge:** the connection itself, identified by its prose evidence (label) and a categorical key (predicate). Connects N nodes via N incidences.
- **Predicate:** the categorical type of an edge (`speaker_of`, `next_paragraph`). Lives on the edge for tooling; the *evidence* lives on the edge as the label; the *participation roles* live on the incidences.
- **Slug:** a short URL-friendly identifier. For paragraphs, derived from first ~6 content words (TF-IDF would be better; not yet implemented).
- **Field attribute:** dynamic / scalar per-node properties that the renderer can lift into perceptual channels — word count → node size, recency → opacity, tension → color intensity. Distinct from graph-theoretic attributes (predicate, role) which are part of the topology.

---

## Original exploratory notes (preserved with light copy-edits)

These are the questions and provocations that led to the resolved architecture above. Kept as a thinking trail.

> If a paragraph is a node, you could make sentences as nodes too — and each word, for goodness sake. But each word would get merged: every time the word is mentioned, increment a `mention_count` attribute on the same node. (One `violence` node, count = 50, list of paragraph-incidences pointing at it.)

> For paragraph attributes: if the author gives a title? Does the index mention it? Does the glossary have words from it? What tags would it have? (Tagging is the hardest part.) Then we have our Rosetta-tag-nodes that unify them — or we have a button to collapse the Rosetta nodes into connections directly between paragraphs. Either view available; same data underneath.

> If the paragraph node has "Act One" as an attribute — or perhaps that is an edge — if it's an edge, we make it a `member_of` edge. Is that different from a `next_paragraph` edge? **Yes — different.** `member_of` is containment; `next` is sequence. Both are valid layers; both can coexist on the same paragraph node.

> In a paragraph, the author might refer to another paragraph or chapter — does that become an edge? Yes. Predicate: `back_references` or `cross_references`.

> *(Tried opening TheBrain and downloaded it, but it broke the rule of asking to sign in before doing anything, so deleted it. Worth getting a free account? Skippable. The architectural lessons are visible in screenshots and docs; you don't need an account to learn from it. Logseq violates similar rules. Foam (VS Code extension) is the cleanest study object — works on any folder of markdown files with no account.)*

> Even though we use paragraphs as nodes, the paragraph gets a slug as its node label. The slug is the most important words of the paragraph that sum it up. Hard. (TF-IDF over the corpus would do this; first ~6 content words is a reasonable fallback.)

> We're throwing away valuable human work if we don't use paragraphs (and load-bearing sentences) as nodes. We can still get a semantic view via tags layered on top.

> Pipeline: find paragraphs → assign paragraph numbers → locate if paragraph is referenced in glossary, index, TOC, appendix → emit nodes/edges/incidences accordingly.

> If a paragraph contains a word that's mentioned in the index by page number, what is that? Is it the edge? Or the incidence? **The word is a NODE.** Paragraph → word (`contains`). Index entry → word (`indexed_under`). The word is the bridge; the path from paragraph to index entry runs through the word as a hub node.

> Paragraphs can also mention characters. The character is a node (because characters have identity, attrs, an arc). The connection between paragraph and character is an edge — and *what kind* of mention it is (POV-of, speaker-of, addressee-of, introduces, referenced-by) lives on the incidences as their role pair, with text evidence as the edge's label.

> If pA mentions Samara Wexler and pB also mentions Samara Wexler — is the incidence "character_mentioned"? Or is it [character + verb]? What's the label of the connection? **Resolved:** Samara is a node. Each paragraph has its own edge to her, with the role on the incidence (`speaker`, `addressee`, `referent`, etc.) and the text evidence on the edge as its label. Two paragraphs that both mention her share the same target node; they don't share an edge.

---

## Implementation pointers

- `adapters/manuscript_to_hypergraph.py` — emits the editorial-discipline shape
- `adapters/instagraph_to_hypergraph.py` — propagates `label` field through
- `adapters/hypergraph_to_dyadic.py` — uses `attrs.label` as link.label, `i2t:predicate` as link.layer
- `data/private/elinor-jones.{instagraph,hypergraph.topothink,normalized-dyadic}.json` — the working corpus
- `research/editorial-discipline.md` — the principle in full

Future iterations on the table:
- Word-level granularity (only for words appearing in index/glossary/character list)
- Sentence-level granularity for load-bearing sentences (epigraphs, theses, climax lines)
- Tension scalar field per word/sentence/paragraph (Harry's metric, in progress)
- Cross-paragraph reference detection (author cross-refs)
- Rosetta-stone-tag-node federation across multiple sources
