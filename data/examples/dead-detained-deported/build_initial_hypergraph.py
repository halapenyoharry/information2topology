#!/usr/bin/env python3
"""Initial extraction: the DeadDetainedDeported research document -> canonical
TopoThink hypergraph.

Source document:
  ~/Projects/DeadDetainedDeported.website/_research/ICE Detention Data and APIs.md

This script IS the extraction — the records below were transcribed from that
document by hand (every edge carries its i2t:evidence quote and dcterms:source
pointing at the source nodes). Run it to regenerate the base layer:

  python3 build_initial_hypergraph.py

Output: layers/ddd.base-research-doc.hypergraph.topothink.json
Then `python3 update_pipeline.py rebuild` merges all layers into the
canonical file and emits the dyadic projection.
"""
from __future__ import annotations

from pathlib import Path

from ddd_lib import GraphBuilder, LAYERS_DIR, add_death, sha256_file, utcnow_iso

RESEARCH_DOC = Path.home() / "Projects/DeadDetainedDeported.website/_research/ICE Detention Data and APIs.md"

# ---------------------------------------------------------------------------
# Source nodes. These double as the provenance targets of dcterms:source and
# as the subjects of sources.registry.json (same ids). Reified by use: edges
# point AT them, so they are first-class nodes, not just strings.
# ---------------------------------------------------------------------------
SOURCES = [
    ("source:ddd-research-doc", "DeadDetainedDeported research compilation", None,
     "Local research document synthesizing the cited public sources."),
    ("source:ice-death-reporting", "ICE Detainee Death Reporting index",
     "https://www.ice.gov/detain/detainee-death-reporting",
     "Official ledger of deaths in physical ICE custody; statutory 90-day reporting."),
    ("source:trac", "Transactional Records Access Clearinghouse (TRAC)",
     "https://trac.syr.edu",
     "Monthly detention census, ADP, facility profiles, court backlogs; 30-60 day lag."),
    ("source:deportation-data-project", "Deportation Data Project (UC Berkeley & UCLA)",
     "https://deportationdata.org",
     "Raw ICE arrest logs, book-in microdata, transfers, flight manifests; CSV/Parquet."),
    ("source:courtlistener-recap", "CourtListener / RECAP (Free Law Project)",
     "https://www.courtlistener.com",
     "Federal dockets, TRO filings, habeas petitions; REST API and webhooks; real-time."),
    ("source:freedom-for-immigrants", "Freedom for Immigrants Detention Database",
     "https://www.freedomforimmigrants.org/map",
     "Facility conditions, solitary abuse, geocoded detention sites; crowdsourced."),
    ("source:third-country-deportation-watch", "Third Country Deportation Watch",
     "https://www.thirdcountrydeportationwatch.org/el-salvador",
     "Transferred noncitizens, third-country facilities, post-removal deaths."),
    ("source:uscri-tcd-tracker", "USCRI Third Country Deportations Tracker",
     "https://refugees.org/tcdtracker/", None),
    ("source:hrw-deported-to-danger", "HRW, Deported to Danger (2020)",
     "https://www.hrw.org/report/2020/02/05/deported-danger/united-states-deportation-policies-expose-salvadorans-death-and",
     "Verified 138 killings of deported Salvadorans; 70+ torture/assault/disappearance cases."),
    ("source:mother-jones-uncounted", "Mother Jones, The Deaths ICE Doesn't Count (2026-08)",
     "https://www.motherjones.com/politics/2026/08/the-deaths-ice-doesnt-count/", None),
    ("source:ap-locator-purge", "AP Exclusive: ICE hides locations of detainees with final removal orders",
     "https://apnews.com/article/ice-detainee-locator-disappear-removal-orders-c3329a70bce424879bc5880b286c019c", None),
    ("source:ccr-wgeid-petition", "CCR press release: coalition petition to UN WGEID",
     "https://ccrjustice.org/home/press-center/press-releases/immigrant-rights-coalition-urges-united-nations-intervene-after-ice", None),
    ("source:vera-detention-data", "Vera Institute, Ten Things We Know from the Latest ICE Detention Data (2026-08)",
     "https://www.vera.org/publications/ten-things-we-know-from-the-latest-ice-detention-data-august-2026", None),
    ("source:phr-aclu-audits", "PHR / ACLU clinical oversight evaluations; American Oversight, Deadly Failures",
     "https://americanoversight.org/reports-and-features/deadly-failures-preventable-deaths-in-u-s-immigration-detention/", None),
    ("source:guardian-invisibilized", "Guardian interactive: Gone in 90 seconds (2026-09-28)",
     "https://www.theguardian.com/us-news/ng-interactive/2026/sep/28/ice-us-immigration-new-tactics", None),
    ("source:amnesty-whistles-guns", "Amnesty International, We Had Whistles They Had Guns (2026-09)",
     "https://www.amnestyusa.org/wp-content/uploads/2026/09/We-Had-Whistles-They-Had-Guns-Human-Rights-Violations-in-U.S.-Immigration-Enforcement-Operations-and-the-Case-to-Abolish-ICE_Amnesty-International-report.pdf", None),
    ("source:odls", "ICE Online Detainee Locator System (ODLS)",
     "https://locator.ice.gov",
     "Manual search only (A-Number+country, or name+DOB+country); CAPTCHA; no API."),
    ("source:ice-directives", "ICE Policy Directives 11003.6 / 11003.7",
     "https://www.ice.gov/doclib/foia/policy/11003.7.pdf", None),
]

# --- ICE official death ledger, FY2024-FY2026, as tabulated in the doc -----
# (name_as_listed, iso_date, fiscal_year, context_or_None, facility_or_None)
LEDGER = [
    ("Wei, Lianyong", "2026-08-23", "FY2026", None, None),
    ("Lopez Cornejo, Edwin", "2026-08-01", "FY2026", None, None),
    ("Arenas Silva, Jesus Manuel", "2026-07-13", "FY2026", None, None),
    ("Florian, Adrian", "2026-06-24", "FY2026", None, None),
    ("Alcorta-Rodriguez, Felix", "2026-06-19", "FY2026", None, None),
    ("Artmeladze, Mamuka", "2026-06-04", "FY2026",
     "Hospitalized in Louisiana; official cause pending autopsy", None),
    ("Adan Gonzalez, Denny", "2026-04-28", "FY2026", None, None),
    ("Carbonell Betancourt, Aled", "2026-04-12", "FY2026", None, None),
    ("Cabrera Clemente, Alejandro", "2026-04-11", "FY2026", None, None),
    ("Bui, Tuan Van", "2026-04-01", "FY2026", None, None),
    ("Ramos Solano, Jose Guadalupe", "2026-03-25", "FY2026", None, None),
    ("Perez Jimenez, Royer", "2026-03-16", "FY2026", None, None),
    ("Paktiawal, Mohammad Nazeer", "2026-03-14", "FY2026", None, None),
    ("Damas, Emmanuel", "2026-03-02", "FY2026", None, None),
    ("Najafabadi, Pejman Karshenas", "2026-03-01", "FY2026", None, None),
    ("Gutierrez Reyes, Alberto", "2026-02-27", "FY2026", None, None),
    ("Garcia Hernandez, Jairo", "2026-02-16", "FY2026", None, None),
    ("Sim, Lorth", "2026-02-16", "FY2026", None, None),
    ("Diaz, Victor Manuel", "2026-01-14", "FY2026",
     "Found unconscious at Camp East Montana, El Paso, TX", "facility:camp-east-montana"),
    ("Sanchez Dominguez, Heber", "2026-01-14", "FY2026", None, None),
    ("La, Parady", "2026-01-09", "FY2026", None, None),
    ("Yanez Cruz, Luis", "2026-01-06", "FY2026", None, None),
    ("Nunez Caceres, Luis", "2026-01-05", "FY2026", None, None),
    ("Lunas Campos, Geraldo", "2026-01-03", "FY2026", None, None),
    ("Gantchev, Nenko Stanev", "2025-12-15", "FY2026", None, None),
    ("Francisco Rodriguez, Delvin", "2025-12-14", "FY2026",
     "Pronounced brain dead at Merit Health Natchez, MS", "facility:merit-health-natchez"),
    ("Abdulkadir, Fouad Saeed", "2025-12-14", "FY2026", None, None),
    ("Brutus, Jean Wilson", "2025-12-12", "FY2026", None, None),
    ("Sachiwani, Shiraz Fateh Ali", "2025-12-06", "FY2026", None, None),
    ("Montejo, Pete Sumalo", "2025-12-05", "FY2026", None, None),
    ("Gaspar-Andres, Francisco", "2025-12-03", "FY2026", None, None),
    ("Wong, Kai Yin", "2025-10-25", "FY2026", None, None),
    ("Garcia-Aviles, Gabriel", "2025-10-23", "FY2026", None, None),
    ("Castro Rivera, Jose", "2025-10-23", "FY2026", None, None),
    ("Saleh, Hasan Ali Moh'd", "2025-10-11", "FY2026", None, None),
    ("Cruz-Silva, Leo", "2025-10-04", "FY2026", None, None),
    ("Garcia Hernandez, Miguel Angel", "2025-09-30", "FY2025", None, None),
    ("Xie, Huabing", "2025-09-29", "FY2025", None, None),
    ("Guzman Fuentes, Norlan", "2025-09-24", "FY2025", None, None),
    ("Ayala Uribe, Ismael", "2025-09-22", "FY2025", None, None),
    ("Reyes, Banegas", "2025-09-18", "FY2025", None, None),
    ("Villegas Gonzalez, Silverio", "2025-09-12", "FY2025", None, None),
    ("Duarte Rascon, Oscar", "2025-09-08", "FY2025", None, None),
    ("Batrez Vargas, Lorenzo Antonio", "2025-08-31", "FY2025", None, None),
    ("Ge, Chaofeng", "2025-08-05", "FY2025", None, None),
    ("Phan, Tien Xuan", "2025-07-19", "FY2025", None, None),
    ("Perez, Isidro", "2025-06-26", "FY2025", None, None),
    ("Noviello, Johnny", "2025-06-23", "FY2025", None, None),
    ("Molina-Veya, Jesus", "2025-06-07", "FY2025", None, None),
    ("Avelleneda-Delgado, Abelardo", "2025-05-05", "FY2025", None, None),
    ("Blaise, Marie Ange", "2025-04-25", "FY2025", None, None),
    ("Nguyen, Nhon Ngoc", "2025-04-16", "FY2025", None, None),
    ("Rayo-Garzon, Brayan", "2025-04-08", "FY2025", None, None),
    ("Tineo Martinez, Juan Alexis", "2025-02-23", "FY2025", None, None),
    ("Chernyak, Maksym", "2025-02-20", "FY2025", None, None),
    ("Dejene, Serawit Gezahegn", "2025-01-29", "FY2025", None, None),
    ("Ruiz Guillen, Genry", "2025-01-23", "FY2025", None, None),
    ("Amechand, Ramesh", "2024-12-16", "FY2025", None, None),
    ("Kataria, Pankaj Karan Singh", "2024-11-01", "FY2025", None, None),
    ("Sanchez-Castro, Jose Manuel", "2024-10-27", "FY2025", None, None),
    ("Bamaca-Zacarias, Brendy Yohana", "2024-09-07", "FY2024", None, None),
    ("Quintana, Jhon Benavides", "2024-06-15", "FY2024", None, None),
    ("Boror-Urla, Hugo Roberto", "2024-05-22", "FY2024", None, None),
    ("Dennis, Cambric", "2024-05-22", "FY2024", None, None),
    ("Farias-Farias, Edixon Del Jesus", "2024-04-18", "FY2024", None, None),
    ("Singh, Jaspal", "2024-04-15", "FY2024", None, None),
    ("Daniel, Charles Leo", "2024-03-07", "FY2024", None, None),
    ("Ba, Ousmane", "2024-02-23", "FY2024", None, None),
    ("Okpu, Frankline", "2023-12-06", "FY2024", None, None),
    ("Juan Francisco, Carlos", "2023-12-04", "FY2024", None, None),
    ("Shrestha, Subash", "2023-11-13", "FY2024", None, None),
    ("Chirino Peralta, Julio Cesar", "2023-10-08", "FY2024", None, None),
]

# --- Historical cohort FY2018-FY2023 (month precision in the doc) ----------
HISTORICAL = [
    ("Melvin Ariel Calero Mendoza", "2022-10"),
    ("Salvador Rosales-Vargas", "2023-04"),
    ("Cristian Dumitrascu", "2023-03"),
    ("Kesley Vial", "2022-08"),
    ("Benjamin Gonzalez-Soto", "2022-07"),
    ("Pablo Sanchez-Gotopo", "2021-10"),
    ("Elba Maria Centeno-Briones", "2021-08"),
    ("Diego Fernando Gallego-Agudelo", "2021-03"),
    ("Jesse Dean", "2021-02"),
    ("Felipe Montes", "2021-01"),
    ("Anthony Jones", "2020-12"),
    ("James Tomas Hill", "2020-08"),
    ("Luis Sanchez-Perez", "2020-07"),
    ("Carlos Ernesto Escobar-Mejia", "2020-05"),
    ("Efrain Romero De La Rosa", "2018-07"),
    ("Roxana Hernandez", "2018-05"),
]

# --- Post-removal deaths documented by HRW "Deported to Danger" ------------
# (name, age, iso_date_or_None, circumstances)
POST_REMOVAL = [
    ("Carlos Alberto Garay", "43", None,
     "Intercepted in Usulutan while driving his vehicle; shot multiple times by gang members several months after deportation following unheeded extortion threats."),
    ("Mario Enrique Sandoval Gomez", "~30", "2017-06-29",
     "Assassinated inside his residence on June 29, 2017, by attackers posing as law enforcement; had lived in the U.S. and possessed no gang ties."),
    ("Tommy Eduardo Paiz", "41", "2018-08-04",
     "Employed in a San Salvador call center post-removal; abducted while visiting family in La Libertad on August 4, 2018; beaten, handcuffed, and shot."),
    ("Nicolas P.", "25", None,
     "Fled to the U.S. after surviving a shooting in 2015; deported in 2017 and executed inside his family home at 9:30 p.m. on the day of his return."),
    ("Javier (surname withheld)", None, None,
     "Targeted and executed four months after deportation at his family's residence after gang members identified his non-gang artistic tattoos."),
]


def build() -> None:
    meta = {
        "i2t:relation_to_canonical": "predicate-layer",  # base layer of the DDD merge set
        "source_file": str(RESEARCH_DOC),
        "extracted_at": utcnow_iso(),
        "extraction_method": "manual transcription (Claude-assisted), editorial-discipline evidence quotes",
    }
    if RESEARCH_DOC.exists():
        meta["source_sha256"] = sha256_file(RESEARCH_DOC)
    g = GraphBuilder("Dead, Detained, Deported — base layer (research document)", meta)

    # -- sources ------------------------------------------------------------
    for sid, name, url, note in SOURCES:
        g.node(sid, **{"schema:name": name, "schema:url": url, "ddd:note": note, "ddd:node_type": "source"})

    # -- institutions, systems, places --------------------------------------
    org = lambda i, n, **kw: g.node(i, **{"schema:name": n, "ddd:node_type": "organization", **kw})
    org("org:ice", "U.S. Immigration and Customs Enforcement (ICE)")
    org("org:ero", "Enforcement and Removal Operations (ERO)")
    org("org:opr", "Office of Professional Responsibility (OPR)")
    org("org:ihsc", "ICE Health Service Corps (IHSC)")
    org("org:hsi", "Homeland Security Investigations (HSI)")
    org("org:dhs", "Department of Homeland Security (DHS)")
    org("org:geo-group", "GEO Group", **{"ddd:sector": "private corrections"})
    org("org:corecivic", "CoreCivic", **{"ddd:sector": "private corrections"})
    org("org:usms", "U.S. Marshals Service (USMS)")
    org("org:ccr", "Center for Constitutional Rights (CCR)")
    org("org:aclu", "American Civil Liberties Union (ACLU)")
    org("org:amnesty", "Amnesty International")
    org("org:rfk-human-rights", "Robert F. Kennedy Human Rights")
    org("org:raices", "RAICES")
    org("org:hrw", "Human Rights Watch (HRW)")
    org("org:phr", "Physicians for Human Rights (PHR)")
    org("org:un-wgeid", "UN Working Group on Enforced or Involuntary Disappearances (WGEID)",
        **{"ddd:chair": "Grazyna Baranowska"})
    org("org:scotus", "Supreme Court of the United States")

    g.node("system:ice-detention-network",
           **{"schema:name": "U.S. immigration detention network",
              "ddd:node_type": "system",
              "ddd:description": "Distributed network of federal processing centers, privately managed facilities, and county jails."})
    g.node("system:odls",
           **{"schema:name": "Online Detainee Locator System (ODLS)",
              "ddd:node_type": "system", "schema:url": "https://locator.ice.gov"})
    g.node("registry:ice-death-ledger",
           **{"schema:name": "ICE Detainee Death Reporting ledger",
              "ddd:node_type": "registry",
              "schema:url": "https://www.ice.gov/detain/detainee-death-reporting"})

    fac = lambda i, n, **kw: g.node(i, **{"schema:name": n, "ddd:node_type": "facility", **kw})
    fac("facility:camp-east-montana", "Camp East Montana", **{"ddd:location": "El Paso, TX"})
    fac("facility:merit-health-natchez", "Merit Health Natchez", **{"ddd:location": "Natchez, MS", "ddd:kind": "hospital"})
    fac("facility:aurora-detention-center", "Aurora Detention Center", **{"ddd:location": "Aurora, CO"})
    fac("facility:stewart-detention-center", "Stewart Detention Center", **{"ddd:location": "Lumpkin, GA"})
    fac("facility:cecot", "Center for the Confinement of Terrorism (CECOT)",
        **{"ddd:location": "El Salvador", "ddd:kind": "third-country mega-prison"})

    country = lambda i, n: g.node(i, **{"schema:name": n, "ddd:node_type": "country"})
    country("country:united-states", "United States")
    country("country:el-salvador", "El Salvador")
    country("country:uzbekistan", "Uzbekistan")
    country("country:venezuela", "Venezuela")
    country("country:haiti", "Haiti")
    country("country:cuba", "Cuba")

    law = lambda i, n, **kw: g.node(i, **{"schema:name": n, "ddd:node_type": "legal_instrument", **kw})
    law("law:dhs-appropriations-2018", "DHS Appropriations Act of 2018")
    law("law:ice-directive-11003", "ICE Policy Directives 11003.6 / 11003.7")
    law("law:8usc1231b3", "8 U.S.C. § 1231(b)(3) (withholding of removal)")
    law("law:cat-8cfr1208-16c", "Convention Against Torture, 8 C.F.R. § 1208.16(c)")
    law("law:28usc2241", "28 U.S.C. § 2241 (habeas corpus)")
    law("law:privacy-act-foia-exemptions", "Privacy Act of 1974; FOIA exemptions 5 U.S.C. § 552(b)(6), (b)(7)(C)")
    law("law:icppced", "International Convention for the Protection of All Persons from Enforced Disappearance")

    case = lambda i, n: g.node(i, **{"schema:name": n, "ddd:node_type": "court_case"})
    case("case:jgg-v-trump", "J.G.G. v. Trump")
    case("case:dvd-v-dhs", "D.V.D. v. DHS")
    case("case:abrego-garcia", "Abrego Garcia litigation (USCA4 25-1345)")

    g.node("cohort:final-order-concealed",
           **{"schema:name": "Detainees with final removal orders concealed from ODLS",
              "ddd:node_type": "cohort", "ddd:approx_size": 16000,
              "ddd:share_of_detained_population": "~30%"})
    g.node("cohort:cecot-venezuelans",
           **{"schema:name": "Venezuelan nationals transferred to CECOT",
              "ddd:node_type": "cohort", "ddd:approx_size": 252})

    DOC = ["source:ddd-research-doc"]

    # -- deaths: official ledger ---------------------------------------------
    ledger_death_events: list[str] = []
    for name, date_iso, fy, context, facility in LEDGER:
        eid = add_death(
            g, name, date_iso,
            ledger_status="official",
            fiscal_year=fy,
            facility=facility,
            circumstances=context,
            sources=["source:ice-death-reporting"] + DOC,
            evidence=context or "Documented on official ICE custodial death ledger.",
        )
        ledger_death_events.append(eid)

    for name, month in HISTORICAL:
        eid = add_death(
            g, name, month,
            ledger_status="official",
            circumstances="Confirmed custodial fatality, FY2018–FY2023 historical cohort.",
            sources=["source:ice-death-reporting"] + DOC,
            evidence="Between FY 2018 and FY 2023, confirmed custodial fatalities included "
                     f"{name} ({month}).",
        )
        ledger_death_events.append(eid)

    # Ledger membership: one containment hyperedge; the registry encloses the
    # documented death events (set membership, docs/edge-categories.md).
    g.edge(
        "edge:ledger-membership",
        predicate="documents_death",
        category="containment",
        members=[("registry:ice-death-ledger", "registry")]
                + [(eid, "documented_death") for eid in ledger_death_events],
        evidence="The following register details deceased individuals documented on ICE's official Detainee Death Reporting ledger from Fiscal Year 2024 through late Fiscal Year 2026.",
        sources=["source:ice-death-reporting"] + DOC,
    )

    # -- deaths ICE does not count -------------------------------------------
    excluded = [
        add_death(g, "Prisciliano Trejo Ricano", None,
                  ledger_status="excluded-post-release",
                  circumstances="Died in a medical facility days after custodial release.",
                  sources=["source:mother-jones-uncounted"] + DOC,
                  evidence="Documented instances include Prisciliano Trejo Ricano, who died in a medical facility days after custodial release."),
        add_death(g, "Randall Gamboa Esquivel", None,
                  ledger_status="excluded-post-release",
                  circumstances="Removed from the United States; died immediately upon landing in country of origin.",
                  sources=["source:mother-jones-uncounted"] + DOC,
                  evidence="...individuals removed from the United States who died immediately upon landing in their country of origin, such as Randall Gamboa Esquivel."),
    ]
    g.edge(
        "edge:registry-exclusion-post-release",
        predicate="excludes_death",
        category="reference",
        members=[("registry:ice-death-ledger", "registry")] + [(e, "excluded_death") for e in excluded],
        evidence="Because these individuals are technically classified as released from physical custody at the time death is pronounced, ICE systematically excludes them from its public Detainee Death Reporting registry.",
        sources=["source:mother-jones-uncounted"] + DOC,
        **{"ddd:exclusion_mechanism": "humanitarian parole / bond release shortly before death"},
    )

    good = add_death(g, "Renee Nicole Good", None,
                     ledger_status="excluded-enforcement-op",
                     circumstances="Fatal shooting during an enforcement operation in Minneapolis.",
                     sources=["source:amnesty-whistles-guns"] + DOC,
                     evidence="Incidents such as the fatal shooting of Renee Nicole Good during an enforcement operation in Minneapolis fall outside custodial registries entirely.")
    g.edge(
        "edge:registry-exclusion-enforcement-ops",
        predicate="excludes_death",
        category="reference",
        members=[("registry:ice-death-ledger", "registry"), (good, "excluded_death")],
        evidence="Official mortality metrics exclude lethal force encounters occurring during community arrest operations, street sweeps, and residential entries executed by ERO and HSI personnel.",
        sources=["source:amnesty-whistles-guns"] + DOC,
        **{"ddd:exclusion_mechanism": "lethal force outside custody; handled as police shooting investigations"},
    )

    # -- clinical audit cases (PHR / ACLU) -----------------------------------
    samimi = add_death(g, "Kamyar Samimi", None,
                       ledger_status="audit-documented",
                       facility="facility:aurora-detention-center",
                       circumstances="Died after medical personnel halted prescribed opioid agonist treatment.",
                       sources=["source:phr-aclu-audits"] + DOC,
                       evidence="Clinical audits reveal patterns of abrupt medication discontinuation, such as the case of Kamyar Samimi, who died after medical personnel at the Aurora Detention Center halted prescribed opioid agonist treatment.")
    jimenez = add_death(g, "Jean Jimenez", None,
                        ledger_status="audit-documented",
                        facility="facility:stewart-detention-center",
                        circumstances="Suicide following prolonged solitary isolation.",
                        sources=["source:phr-aclu-audits"] + DOC,
                        evidence="...severe psychiatric neglect resulting in suicide, as in the death of Jean Jimenez at Stewart Detention Center following prolonged solitary isolation.")
    g.edge(
        "edge:phr-aclu-mortality-finding",
        predicate="attributes_deaths_to",
        category="reference",
        members=[("org:phr", "evaluator"), ("org:aclu", "evaluator"),
                 (samimi, "case_study"), (jimenez, "case_study"),
                 ("system:ice-detention-network", "evaluated_system")],
        evidence="Clinical oversight evaluations coordinated by Physicians for Human Rights (PHR) and the ACLU indicate that these deaths are frequently attributable to chronic failures in correctional healthcare administration.",
        sources=["source:phr-aclu-audits"] + DOC,
    )

    # -- post-removal deaths (El Salvador, HRW) -------------------------------
    post_removal_events = []
    for name, age, date_iso, circ in POST_REMOVAL:
        post_removal_events.append(add_death(
            g, name, date_iso,
            ledger_status="post-removal",
            age=age,
            country_of_death="country:el-salvador",
            circumstances=circ,
            sources=["source:hrw-deported-to-danger"] + DOC,
            evidence=circ,
        ))
    g.edge(
        "edge:hrw-deported-to-danger-findings",
        predicate="verified_post_removal_harm",
        category="reference",
        members=[("org:hrw", "investigator"), ("country:el-salvador", "destination_country")]
                + [(e, "verified_killing") for e in post_removal_events],
        evidence="Investigations conducted by Human Rights Watch under the 'Deported to Danger' project verified 138 killings of Salvadorans deported from the United States, along with more than 70 cases of torture, sexual assault, and enforced disappearance occurring shortly after arrival.",
        sources=["source:hrw-deported-to-danger"] + DOC,
        **{"ddd:verified_killings": 138, "ddd:torture_assault_disappearance_cases": "70+"},
    )
    g.edge(
        "edge:monitoring-ceases-at-border",
        predicate="monitoring_ceases_upon",
        category="reference",
        members=[("country:united-states", "monitoring_state"), ("system:ice-detention-network", "monitored_system")],
        evidence="When noncitizens are removed from the United States, official domestic monitoring ceases at the border.",
        sources=DOC,
    )

    # -- governance of the death ledger ---------------------------------------
    g.edge("edge:ledger-mandated-by", predicate="mandates", category="reference", directed=True,
           members=[("law:dhs-appropriations-2018", "source"), ("registry:ice-death-ledger", "target")],
           evidence="Federal tracking of deaths in immigration custody is formally regulated under the DHS Appropriations Act of 2018, which requires ICE to publish reports regarding in-custody deaths within 90 days of occurrence.",
           sources=["source:ice-directives"] + DOC,
           **{"ddd:reporting_deadline_days": 90})
    g.edge("edge:directive-escalation-timeline", predicate="defines_protocol_for", category="reference", directed=True,
           members=[("law:ice-directive-11003", "source"), ("registry:ice-death-ledger", "target")],
           evidence="The relevant Field Office Director must issue notifications within 12 hours to senior leadership in ERO and OPR; an interim notice must be published within two business days, followed by Mortality Review Reports by IHSC and OPR Detainee Death Reviews, with toxicology and autopsy records finalized within 60 to 180 days.",
           sources=["source:ice-directives"] + DOC)
    g.edge("edge:ledger-maintained-by", predicate="maintained_by", category="reference", directed=True,
           members=[("registry:ice-death-ledger", "source"), ("org:ice", "target")], sources=DOC)
    g.edge("edge:odls-operated-by", predicate="operated_by", category="reference", directed=True,
           members=[("system:odls", "source"), ("org:ice", "target")], sources=DOC)
    for sub in ("org:ero", "org:opr", "org:ihsc", "org:hsi"):
        g.edge(f"edge:{sub.split(':')[1]}-part-of-ice", predicate="component_of", category="containment", directed=True,
               members=[(sub, "source"), ("org:ice", "target")], sources=DOC)
    g.edge("edge:ice-part-of-dhs", predicate="component_of", category="containment", directed=True,
           members=[("org:ice", "source"), ("org:dhs", "target")], sources=DOC)

    # -- facility network structure -------------------------------------------
    g.edge("edge:facility-count-discrepancy", predicate="obscures_facilities", category="reference",
           members=[("org:ice", "publisher"), ("system:ice-detention-network", "described_system")],
           evidence="Physical custody is distributed across 469 facilities nationwide... Crucially, ICE's public directory lists only 208 centers, obscuring more than 260 municipal lockups, county jails, and transit staging facilities from standard visibility.",
           sources=["source:vera-detention-data"] + DOC,
           **{"ddd:active_facilities": 469, "ddd:publicly_listed": 208, "ddd:obscured": "260+"})
    g.edge("edge:network-operators", predicate="operated_through", category="interactivity",
           members=[("system:ice-detention-network", "network"),
                    ("org:geo-group", "contract_operator"), ("org:corecivic", "contract_operator"),
                    ("org:usms", "interagency_operator")],
           evidence="...dedicated Contract Detention Facilities (CDFs) operated by private corrections entities like GEO Group and CoreCivic, Intergovernmental Service Agreements (IGSAs) with local sheriffs, and U.S. Marshals Service (USMS) inter-agency arrangements.",
           sources=DOC,
           **{"ddd:contract_types": ["CDF", "IGSA", "USMS"]})
    g.edge("edge:cecot-in-el-salvador", predicate="located_in", category="containment", directed=True,
           members=[("facility:cecot", "source"), ("country:el-salvador", "target")], sources=DOC)
    g.edge("edge:aurora-operated-by-geo", predicate="operated_by", category="reference", directed=True,
           members=[("facility:aurora-detention-center", "source"), ("org:geo-group", "target")], sources=DOC)
    g.edge("edge:stewart-operated-by-corecivic", predicate="operated_by", category="reference", directed=True,
           members=[("facility:stewart-detention-center", "source"), ("org:corecivic", "target")], sources=DOC)

    # -- the September 2026 locator purge (reified state-change event) --------
    g.edge(
        "event:odls-purge-2026-09-15",
        predicate="concealed_from_locator",
        category="state_change",
        members=[("org:ice", "acting_agency"), ("system:odls", "modified_system"),
                 ("cohort:final-order-concealed", "concealed_population")],
        evidence="On September 15, 2026, ICE modified the public search protocol of its Online Detainee Locator System. Without public notice or formal administrative rulemaking, the agency removed from ODLS search returns all individuals who have received a final order of removal from an immigration judge. This automated filter affected approximately 16,000 currently incarcerated individuals—nearly 30% of the entire national detained population.",
        sources=["source:ap-locator-purge"] + DOC,
        reify=True,
        **{"ddd:date": "2026-09-15", "ddd:affected_population": 16000},
    )
    g.edge(
        "edge:purge-undermines-due-process",
        predicate="obstructs",
        category="interactivity",
        directed=True,
        members=[("event:odls-purge-2026-09-15", "source"), ("law:28usc2241", "target")],
        evidence="Even after an immigration judge issues a final removal order, noncitizens retain constitutional and statutory rights to file emergency motions to reopen, seek judicial stays of removal, or petition federal district courts for writs of habeas corpus under 28 U.S.C. § 2241. By concealing the physical location of detainees... ICE effectively prevents legal counsel and families from serving legal papers, obtaining signatures, or filing emergency pleadings before expulsion.",
        sources=["source:ap-locator-purge"] + DOC,
    )
    g.edge(
        "event:wgeid-petition-2026-09",
        predicate="petitioned",
        category="interactivity",
        members=[("org:ccr", "petitioner"), ("org:aclu", "petitioner"), ("org:amnesty", "petitioner"),
                 ("org:rfk-human-rights", "petitioner"), ("org:raices", "petitioner"),
                 ("org:un-wgeid", "petitioned_body"),
                 ("event:odls-purge-2026-09-15", "subject_of_petition"),
                 ("law:icppced", "legal_basis")],
        evidence="In late September 2026, a legal coalition of more than 30 organizations filed an emergency petition with the UN Working Group on Enforced or Involuntary Disappearances... asserting that detaining noncitizens while refusing to disclose their physical location constitutes an enforced disappearance under the International Convention for the Protection of All Persons from Enforced Disappearance.",
        sources=["source:ccr-wgeid-petition"] + DOC,
        reify=True,
        **{"ddd:date": "2026-09", "ddd:coalition_size": "30+ organizations"},
    )
    g.edge(
        "edge:redaction-authorized-by",
        predicate="authorizes_redaction",
        category="reference",
        directed=True,
        members=[("law:privacy-act-foia-exemptions", "source"), ("org:ice", "target")],
        evidence="Under the Privacy Act of 1974 and federal FOIA exemptions (specifically 5 U.S.C. § 552(b)(6) and (b)(7)(C)), ICE routinely redacts names and Alien Numbers from public microdata releases.",
        sources=DOC,
    )

    # -- third-country expulsion corridors ------------------------------------
    g.edge(
        "event:salvadoran-pipeline",
        predicate="transferred_to_third_country_custody",
        category="state_change",
        members=[("org:ice", "removing_agency"), ("cohort:cecot-venezuelans", "transferred_cohort"),
                 ("facility:cecot", "receiving_facility"), ("country:el-salvador", "receiving_state")],
        evidence="Commencing under diplomatic arrangements in March 2025, noncitizens—including roughly 252 Venezuelan nationals and dozens of others—were transferred directly into the custodial authority of El Salvador and incarcerated within high-security facilities, including CECOT.",
        sources=["source:third-country-deportation-watch", "source:uscri-tcd-tracker"] + DOC,
        reify=True,
        **{"ddd:start_date": "2025-03", "ddd:documented_conditions": "23.5-hour solitary confinement in unlit cells"},
    )
    g.edge(
        "edge:cecot-litigation-documents-conditions",
        predicate="documents_conditions_at",
        category="reference",
        members=[("case:jgg-v-trump", "litigation"), ("case:dvd-v-dhs", "litigation"),
                 ("facility:cecot", "documented_facility")],
        evidence="Federal litigation, including J.G.G. v. Trump and D.V.D. v. DHS, demonstrated that detainees were subjected to 23.5-hour solitary confinement in unlit cells.",
        sources=["source:third-country-deportation-watch"] + DOC,
    )
    g.node(person_id := "person:kilmar-armando-abrego-garcia",
           **{"schema:name": "Kilmar Armando Abrego Garcia", "ddd:node_type": "person"})
    g.edge(
        "event:abrego-garcia-removal",
        predicate="deported_in_violation_of_order",
        category="state_change",
        members=[(person_id, "deported_person"), ("org:ice", "removing_agency"),
                 ("country:el-salvador", "destination"), ("case:abrego-garcia", "adjudicating_case"),
                 ("law:8usc1231b3", "violated_protection")],
        evidence="In the case of Kilmar Armando Abrego Garcia, federal courts documented that ICE deported the individual to Salvadoran imprisonment in direct violation of a federal judge's withholding order.",
        sources=["source:third-country-deportation-watch"] + DOC,
        reify=True,
    )
    g.edge(
        "edge:third-country-circumvents-protections",
        predicate="circumvents",
        category="interactivity",
        directed=True,
        members=[("event:salvadoran-pipeline", "source"), ("law:8usc1231b3", "target"),
                 ("law:cat-8cfr1208-16c", "target")],
        evidence="To circumvent these legal bars, federal enforcement agencies executed third-country agreements that allow noncitizens to be expelled to foreign partner jurisdictions with which they have no ties.",
        sources=DOC,
    )
    g.edge(
        "edge:third-country-volume",
        predicate="expelled_under_third_country_instruments",
        category="state_change",
        members=[("org:ice", "removing_agency"), ("country:el-salvador", "destination"),
                 ("country:uzbekistan", "destination")],
        evidence="Over a twelve-month period through late 2026, more than 23,000 noncitizens were expelled under these third-country instruments... including expulsions of third-country nationals to Uzbekistan and multiple African jurisdictions.",
        sources=["source:uscri-tcd-tracker"] + DOC,
        **{"ddd:expelled_12mo_through_late_2026": "23,000+"},
    )
    g.edge(
        "edge:scotus-permits-removals",
        predicate="permitted_continuation_of",
        category="interactivity",
        directed=True,
        members=[("org:scotus", "source"), ("edge:third-country-volume", "target")],
        evidence="While federal courts issued injunctions halting transfers to specific third countries, the Supreme Court permitted removals to continue in late September 2026 while litigation proceeds on the merits.",
        sources=DOC,
        **{"ddd:date": "2026-09"},
    )
    # the volume edge is referenced by the SCOTUS edge, so reify it
    g.node("edge:third-country-volume", **{"i2t:reified": True})

    # -- detention-scale measurements (unary metric edges on the system node) --
    # Each measurement is a dated claim; refreshes append new measurement edges
    # rather than overwriting, which is what gives the dashboard a time axis.
    def metric(mid: str, evidence: str, srcs: list[str], **attrs):
        g.edge(f"edge:metric/{mid}", predicate="measured_at", category="reference",
               members=[("system:ice-detention-network", "measured_system")],
               evidence=evidence, sources=srcs, **attrs)

    metric("adp-2026-mid",
           "The daily detained population climbed past 65,000 individuals by mid-2026, surpassing the previous historical record of approximately 50,000 to 55,000 set in August 2019.",
           ["source:vera-detention-data", "source:trac"] + DOC,
           **{"ddd:metric": "average_daily_population", "ddd:value": 65000, "ddd:as_of": "2026-06",
              "ddd:baseline": "~20,000 (late 2021); ~50,000-55,000 (2019-08)", "ddd:beds_target": 110000})
    metric("bookins-cumulative",
           "Cumulative book-ins across the expanded enforcement apparatus reached 591,385, with July 2026 logging more than 46,000 admissions in a single month.",
           ["source:deportation-data-project"] + DOC,
           **{"ddd:metric": "cumulative_book_ins", "ddd:value": 591385, "ddd:monthly_peak": "46,000+ (2026-07)",
              "ddd:baseline": "~23,000/month (2025-05)"})
    metric("noncriminal-share",
           "Microdata analyzed by TRAC and the Deportation Data Project confirms that nearly three-quarters of all detained noncitizens have no criminal record (73.6% non-criminal, 48,377 of 65,735).",
           ["source:trac", "source:deportation-data-project"] + DOC,
           **{"ddd:metric": "noncriminal_share", "ddd:value": "73.6%", "ddd:numerator": 48377, "ddd:denominator": 65735})
    metric("sixty-day-release-collapse",
           "Under intensified detention policies, 60-day release rates plummeted from 35% to less than 7%.",
           ["source:trac"] + DOC,
           **{"ddd:metric": "released_within_60_days", "ddd:value": "<7%", "ddd:baseline": "~35%"})
    metric("interior-arrests-multiplier",
           "Interior arrests multiplied by a factor of 11 as agents targeted individuals outside courthouses, at mandatory check-in appointments, and in public settings.",
           ["source:guardian-invisibilized", "source:deportation-data-project"] + DOC,
           **{"ddd:metric": "interior_arrest_multiplier", "ddd:value": "11x"})
    metric("mortality-2025",
           "While the agency recorded over 170 deaths across the combined period between 2003 and 2025, custodial deaths exceeded 32 individuals in 2025 alone.",
           ["source:ice-death-reporting"] + DOC,
           **{"ddd:metric": "custodial_deaths", "ddd:value_2025": "32+", "ddd:value_2003_2025": "170+"})
    metric("demographic-targeting",
           "Recent enforcement has disproportionately targeted Haitian immigrants—following the administrative termination of Temporary Protected Status—alongside Venezuelan, Cuban, and African nationals.",
           ["source:vera-detention-data"] + DOC,
           **{"ddd:metric": "disproportionately_targeted_nationalities",
              "ddd:value": ["Haiti", "Venezuela", "Cuba", "African nations"]})

    # -- what each source tracks (the update topology itself) ------------------
    tracks = [
        ("source:ice-death-reporting", "registry:ice-death-ledger",
         "Detainees who die while in official physical ICE detention; excludes deaths post-release or during street-level operations."),
        ("source:trac", "system:ice-detention-network",
         "Monthly detention census, average daily population, facility criminal profiles, court backlogs; 30-60 day lag."),
        ("source:deportation-data-project", "system:ice-detention-network",
         "Raw ICE arrest logs, detention book-in microdata, facility transfers, deportation flight manifests; quarterly to semi-annual releases following court orders."),
        ("source:courtlistener-recap", "law:28usc2241",
         "Federal district court dockets, emergency TRO filings, habeas petitions; real-time indexing, limited to detainees who secure representation."),
        ("source:freedom-for-immigrants", "system:ice-detention-network",
         "Facility conditions, solitary confinement abuse, geographic coordinates of detention sites; crowdsourced and visitation-dependent."),
        ("source:third-country-deportation-watch", "facility:cecot",
         "Transferred noncitizens, third-country facilities, post-removal violent deaths; investigative cadence, no continuous census."),
        ("source:odls", "cohort:final-order-concealed",
         "Manual locator; post-2026-09-15 deliberately returns empty records for final-order detainees."),
    ]
    for src, target, note in tracks:
        g.edge(f"edge:tracks/{src.split(':')[1]}", predicate="tracks", category="reference", directed=True,
               members=[(src, "source"), (target, "target")],
               sources=DOC, **{"ddd:coverage_note": note})

    g.write(LAYERS_DIR / "ddd.base-research-doc.hypergraph.topothink.json")


if __name__ == "__main__":
    build()
