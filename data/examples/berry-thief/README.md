# Berry Thief (gold extraction)

Reference topology for *The Epic of Elinor Jones*, Act 1, Chapter 1. Use it to score extractors and prompts: run any model over `berry-thief.source.md` and diff against `berry-thief.relations.json`.

- 70 nodes, 117 relations (54 with three or more participants), 9 modes in use, 0 unverified quotes.
- Built by hand and audited against an independent Sonnet 5.5 extraction. Every judgment call is in `annotations.md`.
- The canonical hypergraph and the dyadic projection are generated from the relation list; edit the relation list, then regenerate.

## Regenerate

The canonical hypergraph was generated from the relation list (edge ids `edge:<predicate>/<first participant>`, participants as incidences with their roles, mode/evidence/locus as edge attrs), validated with `engine/validator.py`, and projected with `adapters/hypergraph_to_dyadic.py`. No build script is checked in yet; the generation is a few lines and can be added as a Makefile target if this example gets edited often.

## Load in Exoskeleton

Open `berry-thief.normalized-dyadic.json` in json-edit (☰ → Open file). The dyadic viewer shows 79 layers, one per predicate; `contains` is the structure, `asks`/`tells`/`messages` the dialogue, `moves`/`digs_up`/`steals` the plot.
