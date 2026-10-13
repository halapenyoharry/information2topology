# Dead, Detained, Deported — a living hypergraph

Canonical TopoThink hypergraph of U.S. immigration detention deaths, concealment
mechanisms, and deportation pipelines, built from
[`~/Projects/DeadDetainedDeported.website/_research/ICE Detention Data and APIs.md`](../../../../DeadDetainedDeported.website/_research/)
and designed to stay current as its sources update.

Built 2026-10-04. Current contents: **264 nodes / 142 edges / 301 incidences**,
including **98 death events** across five ledger statuses:

| `ddd:ledger_status` | count | meaning |
|---|---|---|
| `official` | 88 | On ICE's Detainee Death Reporting ledger (FY2024–FY2026 register + FY2018–23 cohort) |
| `post-removal` | 5 | Died after deportation (HRW *Deported to Danger*); outside all US monitoring |
| `excluded-post-release` | 2 | Released/paroled days before death → systematically uncounted |
| `excluded-enforcement-op` | 1 | Lethal force during arrest operations → outside custodial registries |
| `audit-documented` | 2 | Documented through PHR/ACLU clinical audits (medication discontinuation, solitary) |

The exclusion categories are the point: **the official registry is modeled as a
containment set, and the deaths it refuses to contain are first-class nodes with
`excludes_death` reference edges carrying the evidence quote.** The gap between
what the state counts and what happened is not a footnote here — it is explicit
topology you can render.

## Files

```
ddd_lib.py                      shared assembly: deterministic IDs, GraphBuilder,
                                add_death() — all builders go through this
build_initial_hypergraph.py     the research document as data-as-code → base layer
update_pipeline.py              status / fetch / rebuild
sources.registry.json           operational manifest of every source (ids match
                                the source: nodes inside the hypergraph)
layers/                         one canonical hypergraph per source
snapshots/                      append-only raw fetches (gitignored)
dead-detained-deported.hypergraph.topothink.json    merged canonical
dead-detained-deported.normalized-dyadic.json       viewer projection (Exoskeleton/JVV)
```

## Update model — how it stays current without losing anything

1. **One source = one layer.** Each source in `sources.registry.json` owns a
   layer file under `layers/`. Refreshing a source rewrites only its layer.
2. **Merge-by-ID federation** (`adapters/merge_hypergraphs.py`). Deterministic
   slugs (`ddd_lib`) mean the ICE page's "Wei, Lianyong / August 23, 2026" lands
   on the same `event:death/wei-lianyong-2026-08-23` node every extraction, so
   layers dedupe on merge. When two sources disagree about an attribute, the
   conflict is **recorded** (`i2t:conflicts` on the merged entity), never
   silently resolved.
3. **Snapshots before parsing.** Every fetch saves raw bytes to `snapshots/`
   first. A parser bug costs nothing; re-extraction is always possible.
4. **Nothing is deleted on update.** A record that vanishes from a source stays
   in the graph with its extraction timestamp. Disappearance from a source is
   itself a signal (that is exactly what the September 2026 ODLS purge was).
5. **Links survive.** Every source URL is a `source:` node; every edge carries
   `dcterms:source` (list of source-node ids) and `i2t:evidence` (the quote that
   justifies the edge, per the editorial discipline). Zero edges in the current
   build lack provenance.

```bash
cd ~/Projects/information2topology/data/examples/dead-detained-deported
python3 update_pipeline.py status     # staleness report
python3 update_pipeline.py rebuild    # regenerate + merge + validate + project (offline)
python3 update_pipeline.py fetch source:ice-death-reporting --network   # explicit opt-in
```

The ICE death-reporting fetcher is implemented (snapshot → tolerant parse →
layer). The other sources are registered with access mechanism, cadence, and
notes on what a fetcher should emit; TRAC and the Deportation Data Project are
the next two worth automating (metrics and trajectories respectively).
CourtListener is the only real-time API and the de-anonymization bridge: unsealed
habeas filings carry real names and named facilities.

## Schema mapping (research doc's Neo4j design → TopoThink)

The research document proposed a labeled property graph (Person, EnforcementAction,
Facility, CourtDocket, Country). The hypergraph subsumes it without intermediate
nodes:

- A death is **one reified state-change hyperedge** — person (`deceased`),
  facility (`custodial_site`), country (`country_of_death`) — not a Person→DIED_IN→CustodialDeath
  chain. N-ary edges carry what property graphs force into join nodes.
- Registry membership is **one containment hyperedge** with 89 incidences, not
  88 separate rows. The registry encloses deaths; enclosure is the relation.
- The locator purge, the WGEID petition, the Salvadoran pipeline, and the
  Abrego Garcia removal are **reified events** — other edges make assertions
  about them (the petition's subject *is* the purge event).
- Detention metrics are **dated unary measurement edges** on
  `system:ice-detention-network`. Refreshes append new measurements instead of
  overwriting — which is what gives the time axis for free.

Every edge is classified into the four-category typology
(`docs/edge-categories.md`): current distribution is 102 state_change /
28 reference / 7 containment / 5 interactivity.

## The infographic thesis — COVID dashboards, but people's lives

COVID dashboards worked because they rendered one relation per panel: a curve
(state change over time), a map (containment in regions), a table (reference).
Per the whitepaper's single-layer-legibility finding (v1.4.0, Addition 5),
legibility arrives exactly when one edge category gets one honest visual channel.
This graph is already split along those seams, so each layer projects to an
infographic the way `split_by_predicate.py` projects a layer:

- **State-change layer** → the mortality curve and individual trajectories
  (arrest → facility → transfer → removal → death). Not case counts — named
  people, each with their evidence quote one click away.
- **Containment layer** → the registry as a drawn region: 88 deaths inside the
  boundary, and the excluded deaths rendered *outside it, adjacent to it* — the
  visual argument of the entire project in one frame. Same idiom for 208 listed
  facilities inside ICE's public directory and 260+ obscured ones outside it,
  and for the ~16,000 concealed inside the detention system but outside ODLS.
- **Interactivity layer** → who acts on whom: petitions, injunctions,
  obstructions, circumventions. The accountability channel map.
- **Reference layer** → the provenance mesh: which source can see which part of
  the system, and — rendered as negative space — which parts nothing can see.

What no COVID dashboard had: **the concealment is in the data model.** A
dashboard of counts can only show what the state publishes. A hypergraph whose
registry-sets and exclusion edges are explicit can render the boundary of the
official record itself — the people the count contains, standing next to the
people it was built not to contain.

## Cautions

- Every fact here traces to published public sources (official ICE ledger,
  court records, HRW/PHR/press reporting) via its evidence quote. Keep it that
  way: no edge without `i2t:evidence` or `dcterms:source`.
- Names of the deceased are public record and memorialization is the point.
  Living individuals appear only as named in public litigation (e.g., Abrego
  Garcia). No PII beyond the sources' own published content; the Fellegi-Sunter
  entity-resolution pipeline sketched in the research doc would need its own
  ethics pass before linking anonymized microdata to names.
- ODLS is CAPTCHA-gated and anti-automation by design; it is registered as a
  source but deliberately has no fetcher.
