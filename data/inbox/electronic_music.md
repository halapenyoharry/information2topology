# Hypergraph Representation of Electronic Music Evolution (2000–2026): A Network Analysis

The evolution of electronic music from the turn of the millennium to the present day represents a period of unprecedented structural and aesthetic acceleration, marked by the transition from physical, geographically isolated club scenes to decentralized, algorithmically mediated digital platforms that have fundamentally rewritten the relational topology of musical culture. Traditional network analysis, relying on bipartite graphs and pairwise relationships, fails to capture this ecosystem because musical development occurs through group participation, shared demographic audiences, and collective aesthetic commitments. This complex domain is best understood through hypergraph representation learning, wherein high-order, multi-dimensional relationships, such as genres, record labels, geographic hubs, and cultural movements, function as hyperedges connecting heterogeneous node types across artists, tracks, labels, platforms, and technological tools.

By analyzing electronic music through advanced topological frameworks, including Hypergraph Neural Networks (HNNs) and Kolmogorov-Arnold Networks (HyperKAN), computational musicology can quantify the flow of sonic influence, trace the emergence of microgenres, and identify bridge nodes connecting disparate sound communities. This analysis incorporates the five edge categories defined in the Information-to-Topology (i2t) v1.4.0 framework: Containment (spatial and organizational hubs), Reference (citations, sampling, and aesthetic homage), State Change (remixes, pitch-shifting, and genre mutations), Interactivity (constitutive collaborations conferring complementary roles), and Instantiation (typing relations linking specific tracks to abstract microgenres).

---

## 1. Topological Foundations & Pre-2000 Lineages

Musical evolution functions as a dynamic topological system where static relational snapshots conceal the underlying velocity of stylistic transformation. In classical graph models, an edge connects exactly two vertices, representing a single dyadic link such as a direct remix between two producers. Electronic music production operates as an n-ary hypergraph where a single aesthetic movement encapsulates dozens of artists, tracks, distribution tools, and performance spaces simultaneously.

```
+-----------------------------------------------------------------------------------+
|                              HYPEREDGE: BLOG HOUSE                                |
|                                                                                   |
|  [Artist: Justice] <--(pioneer)--+                     +--(hub)--> [Label: Ed Banger]
|                                  |                     |                          |
|  [Track: We Are Your Friends] <--+-- (hyperedge: blog_house) --+                  |
|                                                                |                  |
|  [Platform: Hype Machine] <--(infrastructure)------------------+                  |
+-----------------------------------------------------------------------------------+
```

### Pre-2000 Root Nodes and Structural Precursors

The 2000–2026 hypergraph inherits its structural baseline from three foundational nodes established in the late 20th century:

1. **Detroit Techno (The Motor City Axis)**: Grounded by Underground Resistance, Metroplex, and Transmat, pioneered by Jeff Mills, Robert Hood, and Mad Mike Banks. Detroit Techno established stripped-down machine rhythms and speculative futurism, functioning as the primary parent node for European Minimal Techno.
2. **Chicago House & Garage**: Emerging from the Warehouse under Frankie Knuckles and the Music Box under Ron Hardy, Chicago House established the physical club as a sacred space for marginalized Black and queer communities, providing the rhythmic template for all subsequent 4/4 dance music.
3. **UK Jungle & 2-Step Garage**: Developed in London during the mid-1990s through sound system culture, syncopated breakbeats, and pitch-shifted basslines, creating the structural lineage that directly spawned Dubstep and Grime.

---

## 2. 2000–2009: Physical Archives, European Minimal, and Blog House

The first decade of the 2000s marked the transition from physical, location-bound club scenes to digital distribution networks.

```
       [Detroit Techno Lineage]
                  |
                  v (State Change: stripped-down aesthetic)
        [Minimal Techno Hyperedge] <==== (Hub: Kompakt / Perlon)
                  |
     +------------+------------+
     |                         |
[Move D]               [Benjamin Brunn]
     \                         /
      +--> [Track: Velvet Paws]
```

### The Visual Archive and Physical Club Isolation

Before MP3 blogs dematerialized music distribution, networks were physically mapped through localized club promotions. Archival collections, including over 12,000 rave flyers and 17,000 club flyers spanning 25 years, document the geographic hubs and subgenres, such as hard dance, trance, drum 'n' bass, and cosmic house, that defined early 2000s night culture. Tracks like Scott Brown's 170 BPM anthem "Taking Drugs?" (2004) and Tony de Vit's high-NRG contributions to London's trade afterhours scene illustrate the spatial isolation and acoustic intensity of physical club nodes.

### European Minimal Techno and Label Hubs

In contrast to 1990s rave maximalism, Minimal Techno experienced a resurgence across European club circuits. Rooted in Detroit minimalism, the genre was refined by German labels like Kompakt in Cologne, Perlon in Frankfurt, and M_nus in Berlin. Defined by syncopated percussion, subtle dub delays, and atmospheric sound design at 120–130 BPM, Minimal Techno provided a deeply immersive club environment. Move D and Benjamin Brunn's 2008 track "Velvet Paws" exemplifies the intricate headtrip aesthetic produced by this hyperedge.

### French Touch 2.0, Blog House, and MP3 Aggregators

Simultaneously, European electronic music mutated into "French Touch 2.0" or "Blog House", an aggressive, rock-influenced aesthetic driven by heavy compression and distorted synthesizers. Ed Banger Records, founded in 2003 by Pedro Winter, acted as a central hub node connecting Justice, SebastiAn, and Mr. Oizo. Justice's 2007 album *Cross* and their 2006 collaboration with Simian Mobile Disco, "We Are Your Friends", codified the movement's acoustic signature. Kitsuné Musique provided a parallel platform for indie-dance crossover acts including Digitalism, Hot Chip, and Bloc Party.

```
     [Ed Banger Records] <--- (Hub)
              |
    +---------+---------+
    |                   |
[Justice]         [SebastiAn]
    |                   |
    +-----> [Blog House Hyperedge] <----- [Hype Machine Platform]
```

Blog House was uniquely driven by MP3 blogs (Hype Machine, Discobelle) and Myspace, bypassing traditional vinyl distribution through digital bootlegs, high-volume remixes, and peer-to-peer file sharing. The 2008 remix of Kid Cudi's "Day 'n' Nite" by Italian duo Crookers sold over one million copies in the UK, demonstrating how internet blog networks could propel underground club tracks directly onto mainstream pop charts.

### The UK Bass Music Schism: Dubstep, Grime, and Electro House

In the United Kingdom, Dubstep emerged from UK Garage and 2-step around Croydon and South London. Pioneers like Skream, whose 2006 album *Skream!* became a genre blueprint, and Burial, whose 2007 album *Untrue* defined future garage through crackling vinyl textures and pitch-shifted vocal samples, established the sonic parameters of the movement. Concurrently, Grime developed in East London through Wiley, Dizzee Rascal, and the Roll Deep collective, combining 140 BPM instrumental riddims with rapid vocal delivery.

```
[UK Garage / 2-Step]
        |
        +---> [Dubstep Hyperedge] ===> (Pioneers: Skream, Burial, Hatcha)
        |
        +---> [Grime Hyperedge]   ===> (Pioneers: Wiley, Dizzee Rascal)
```

In North America and mainland Europe, Electro House evolved into a heavy, festival-oriented hyperedge led by deadmau5, Feed Me, and Wolfgang Gartner, setting the stage for the mid-tempo and "brostep" explosions led by Skrillex in the next decade.

---

## 3. 2010–2019: Internet Microgenres, Hauntology, and Deconstructed Club

The 2010s brought digital saturation, cloud-based hosting on SoundCloud, and the collapse of the boundary between pop music and avant-garde sound design.

```
                      [SoundCloud / Digital Platforms]
                                     |
    +--------------------------------+--------------------------------+
    |                                |                                |
[Vaporwave Hyperedge]      [Hyperpop Hyperedge]           [Deconstructed Club]
(Macintosh Plus, OPN)      (PC Music, SOPHIE, Charli)     (Arca, Lotic, PAN, Tri Angle)
```

### Commercial EDM vs. Underground Counter-Culture

The decade began with the commercialization of Electronic Dance Music (EDM) in North America, catalyzed by Skrillex's 2010 EP *Scary Monsters and Nice Sprites*. Massive festival brands like Ultra and Electric Daisy Carnival, alongside multi-million-dollar Las Vegas DJ residencies, converted festival mainstages into financialized pop platforms. This commercialization triggered an immediate counter-reaction in the underground, accelerating the creation of internet-native microgenres designed to evade corporate curation.

### Hauntology and Nostalgia: Vaporwave, Synthwave, and Chillwave

Vaporwave, Synthwave, and Chillwave emerged as aesthetic responses to late-capitalist digital saturation. Synthwave (Outrun) relied on analog synthesizer emulation and gated snares, championed by Kavinsky and Com Truise. Chillwave offered a warmer, lo-fi indie-pop fusion popularized by Toro y Moi and Washed Out.

Vaporwave operated as a more abstract, hauntological movement, spearheaded by Oneohtrix Point Never (as Chuck Person on *Eccojams Vol. 1*, 2010) and Macintosh Plus (*Floral Shoppe*, 2011). Utilizing chopped-and-screwed elevator music, corporate training audio, time-stretching, and smooth jazz samples, Vaporwave expressed digital decay, organizing into a recognized subgenre entirely through online forum consensus.

```
[Smooth Jazz / Muzak Samples] ===(State Change: pitch-shift & slow)===> [Vaporwave Hyperedge]
                                                                                ||
                                                                      [Floral Shoppe (2011)]
```

### Hyperpop, PC Music, and the Deconstruction of Pop

Hyperpop emerged from London art collective PC Music, founded by A.G. Cook in 2013. PC Music pioneered "bubblegum bass", an exaggerated take on 1990s pop, Eurodance, and J-pop featuring pitch-shifted vocals and metallic synthesizer design. A.G. Cook's 2014 track "Beautiful" established the acoustic template for the movement.

```
[A.G. Cook / PC Music] ---> [Track: Beautiful] ---> (Proto-Hyperpop)
          |
          +---> [SOPHIE] ---> [Album: Oil of Every Pearl's Un-Insides]
                   |
                   +---> [Charli XCX] ---> [EP: Vroom Vroom] ---> (Mainstream Crossover Bridge)
```

Producer SOPHIE expanded the hyperpop framework through physics-defying synthesizer sound design. Her 2018 album *Oil of Every Pearl's Un-Insides* and collaborations with Charli XCX (*Vroom Vroom* EP, *Pop 2* mixtape) positioned hyperpop at the intersection of experimental electronic music and global pop. Charli XCX acted as a crucial bridge node, bringing underground sound design to mainstream audiences. In 2019, 100 gecs released *1000 gecs*, introducing trap beats, ska, and metalcore into hyperpop, prompting Spotify to codify "Hyperpop" as an official metadata tag and playlist in August 2019.

### Deconstructed Club: Dancefloor Disruption

Operating alongside Hyperpop, Deconstructed Club (Post-Club) dismantled traditional dance music structures, replacing 4/4 beats with dramatic dynamic shifts, metallic textures, and abrasive soundscapes.

```
[Transnational Collectives: GHE20G0TH1K, Fade to Mind, Janus]
                           |
                           v
            [Deconstructed Club Hyperedge]
                           |
       +-------------------+-------------------+
       |                   |                   |
    [Arca]              [Lotic]         [Total Freedom]
       |                   |                   |
 [Label: PAN]     [Label: Tri Angle]   [Label: NAAFI]
```

Emerging from collectives like GHE20G0TH1K in New York, Fade to Mind in Los Angeles, and Janus in Berlin, producers Arca, Lotic, and Total Freedom rejected rigid genre boundaries. Record labels like PAN, Tri Angle, and NAAFI served as infrastructural hubs connecting artists across Mexico City, London, Berlin, and Los Angeles. Deconstructed Club incorporated elements of Jersey club, reggaeton, grime, and dancehall, turning the club into a venue for sound theory and performance art.

---

## 4. 2020–2026: Global Polyrhythms, Post-Genre Acceleration, and Algorithmic Topology

The 2020s mark a post-geographic era where electronic music's center of gravity shifted toward the Global South, driven by high-speed internet adoption and short-form video algorithms.

```
     [Global South Rhythmic Hubs]
                  |
     +------------+------------+
     |                         |
[Amapiano Hyperedge]    [Afro House / 3BIT]
(Log Drum Basslines)    (Black Coffee, Keinemusik)
     |                         |
[Kabza De Small]       [Grammy: Subconsciously]
```

### The Global Hegemony of Amapiano and Afro House

Afro House and Amapiano achieved global prominence during the 2020s, rewriting mainstream dance music's rhythmic foundation. Emerging from South African townships as an evolution of Kwaito, Afro House blends deep house chords with intricate percussive patterns. South African producer Black Coffee championed this sound, winning a Grammy for his 2022 album *Subconsciously*, while Berlin collective Keinemusik (&ME, Rampa, Adam Port) acted as a European bridge node, driving track virality with releases like 2022's "Move".

Concurrently, Amapiano—characterized by melodic log drum synthesis, lounge piano chords, and 110–115 BPM house rhythms—grew from Pretoria and Johannesburg into an international movement led by Kabza De Small, DJ Maphorisa, and Focalistic.

### Dariacore, Drift Phonk, and Microgenre Acceleration

In digital underground spaces, microgenres iterated at high velocity. Coined by Jane Remover in 2021, Dariacore (Hyperflip) uses sample-heavy collages, fast BPMs, Jersey club rhythms, pop-punk samples, and internet memes. The style spread rapidly, merging with Japanese "otoMAD" remix cultures on Niconico and entering arcade games like *Beatmania IIDX*.

```
[Jane Remover] ---> [Dariacore / Hyperflip] ---> [Niconico / Japanese otoMAD] ---> [Beatmania IIDX]
```

Simultaneously, Drift Phonk—characterized by distorted cowbell melodies, heavy bass, and Memphis rap samples—spread across TikTok and YouTube shorts, demonstrating how short-form video recommendation algorithms can rapidly commercialize niche aesthetics.

### Topological Recommender Systems and Algorithmic Feedback Loops

Modern electronic music evolution is deeply intertwined with streaming recommender algorithms. Systems based on Diversified Weighted Hypergraph Recommendation (DWHRec) navigate user, track, label, and tag nodes using random walks to balance recommendation precision with music discovery.

```
[Streaming Platform Algorithm] ===(Reification: Playlist/Tag)===> [Hyperedge Codified]
                                                                        |
                                                                        v
[Underground Producers Evade Tag] <===(Aesthetic Drift / Mutation)------+
```

When an algorithm formalizes a hyperedge (such as Spotify's Hyperpop tag), it creates a feedback loop. The tag shifts from a descriptive community marker into a prescriptive commercial category, prompting original artists to abandon the label and establish new unmapped niches, driving a continuous cycle of topological evasion between producers and machine learning classifiers.

---

## 5. Topological Matrix of Electronic Music (2000–2026)

| Landmark Release / Entity | Primary Artist(s) | Associated Hyperedge | i2t Edge Category | Structural Centrality & Role |
| :--- | :--- | :--- | :--- | :--- |
| *Skream!* (2006) | Skream | Dubstep | Instantiation | High Weighted In-Degree; foundational UK bass node. |
| *Untrue* (2007) | Burial | Future Garage | Reference / State Change | High Betweenness Centrality; bridges bass music with ambient hauntology. |
| *Cross* (2007) | Justice | Blog House | Interactivity (Constitutive) | High Hyperedge Density; anchor node for French Touch 2.0. |
| "Day 'n' Nite" (Crookers Remix) | Kid Cudi / Crookers | Blog House | State Change (Remix) | Crossover Bridge Node; connected blog culture to pop radio charts. |
| *Floral Shoppe* (2011) | Macintosh Plus | Vaporwave | Instantiation / Reference | High Betweenness Centrality; codified internet hauntology. |
| "Beautiful" (2014) | A.G. Cook | Bubblegum Bass / PC Music | Instantiation | Foundational Hub Node; established the PC Music aesthetic. |
| *Oil of Every Pearl's Un-Insides* | SOPHIE | Hyperpop / Deconstructed Club | Interactivity / State Change | High Betweenness Centrality; bridged experimental synthesis with pop. |
| *1000 gecs* (2019) | 100 gecs | Hyperpop | Instantiation | Algorithmic Reification Catalyst; prompted Spotify tag formalization. |
| *Subconsciously* (2022) | Black Coffee | Afro House | Interactivity | Global Hub Node; brought South African electronic music to global awards. |
| "Move" (2022) | Keinemusik | Afro House | Interactivity / Reference | Crossover Bridge Node; European festival distributor for Afro house. |
| *Frailty* (2021) | Jane Remover | Dariacore / Hyperflip | State Change | Microgenre Founder Node; accelerated internet collage music. |

---

## 6. Synthesis and Architectural Conclusion

The history of electronic music from 2000 to 2026 documents a transition from localized physical club hubs to decentralized, high-dimensional digital networks. From Blog House and Minimal Techno to Dubstep, Vaporwave, Hyperpop, Deconstructed Club, Amapiano, and Dariacore, the genre's structural topology has evolved through continuous aesthetic mutation.

Applying the TopoThink hypergraph framework and i2t v1.4.0 edge typology allows computational models to represent these relationships accurately. The appended JSON payload provides a machine-readable hypergraph dataset mapping the nodes, hyperedges, and participation incidences that define modern electronic music.

---

## Appendix: TopoThink Hypergraph Data Payload

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://halapenyoharry.github.io/i2t/hypergraph.topothink.schema.json",
  "metadata": {
    "title": "Comprehensive Topology of Electronic Music Evolution (2000-2026)",
    "description": "An exhaustive hypergraph mapping artists, tracks, labels, platforms, geographic hubs, and genre movements across three decades.",
    "author": "Information to Topology Architecture",
    "timestamp": "2026-08-03T15:00:00Z"
  },
  "nodes": [
    { "id": "artist:jeff_mills", "attrs": { "name": "Jeff Mills", "type": "Artist", "origin": "Detroit, USA", "active_since": 1988 } },
    { "id": "artist:robert_hood", "attrs": { "name": "Robert Hood", "type": "Artist", "origin": "Detroit, USA", "active_since": 1989 } },
    { "id": "artist:move_d", "attrs": { "name": "Move D", "type": "Artist", "origin": "Heidelberg, Germany", "active_since": 1990 } },
    { "id": "artist:benjamin_brunn", "attrs": { "name": "Benjamin Brunn", "type": "Artist", "origin": "Hamburg, Germany", "active_since": 2000 } },
    { "id": "artist:justice", "attrs": { "name": "Justice", "type": "Artist", "origin": "Paris, France", "active_since": 2003 } },
    { "id": "artist:sebastian", "attrs": { "name": "SebastiAn", "type": "Artist", "origin": "Paris, France", "active_since": 2005 } },
    { "id": "artist:crookers", "attrs": { "name": "Crookers", "type": "Artist", "origin": "Milan, Italy", "active_since": 2003 } },
    { "id": "artist:skream", "attrs": { "name": "Skream", "type": "Artist", "origin": "Croydon, UK", "active_since": 2001 } },
    { "id": "artist:burial", "attrs": { "name": "Burial", "type": "Artist", "origin": "London, UK", "active_since": 2005 } },
    { "id": "artist:wiley", "attrs": { "name": "Wiley", "type": "Artist", "origin": "London, UK", "active_since": 1997 } },
    { "id": "artist:deadmau5", "attrs": { "name": "deadmau5", "type": "Artist", "origin": "Toronto, Canada", "active_since": 1998 } },
    { "id": "artist:skrillex", "attrs": { "name": "Skrillex", "type": "Artist", "origin": "Los Angeles, USA", "active_since": 2004 } },
    { "id": "artist:kavinsky", "attrs": { "name": "Kavinsky", "type": "Artist", "origin": "Paris, France", "active_since": 2005 } },
    { "id": "artist:toro_y_moi", "attrs": { "name": "Toro y Moi", "type": "Artist", "origin": "Columbia, USA", "active_since": 2008 } },
    { "id": "artist:oneohtrix_point_never", "attrs": { "name": "Oneohtrix Point Never", "type": "Artist", "origin": "Boston, USA", "active_since": 2007 } },
    { "id": "artist:macintosh_plus", "attrs": { "name": "Macintosh Plus", "type": "Artist", "origin": "Seattle, USA", "active_since": 2011 } },
    { "id": "artist:ag_cook", "attrs": { "name": "A.G. Cook", "type": "Artist", "origin": "London, UK", "active_since": 2013 } },
    { "id": "artist:sophie", "attrs": { "name": "SOPHIE", "type": "Artist", "origin": "Glasgow, UK", "active_since": 2013 } },
    { "id": "artist:charli_xcx", "attrs": { "name": "Charli XCX", "type": "Artist", "origin": "Cambridge, UK", "active_since": 2008 } },
    { "id": "artist:100_gecs", "attrs": { "name": "100 gecs", "type": "Artist", "origin": "St. Louis, USA", "active_since": 2015 } },
    { "id": "artist:arca", "attrs": { "name": "Arca", "type": "Artist", "origin": "Caracas, Venezuela", "active_since": 2011 } },
    { "id": "artist:lotic", "attrs": { "name": "Lotic", "type": "Artist", "origin": "Houston, USA", "active_since": 2011 } },
    { "id": "artist:dj_rashad", "attrs": { "name": "DJ Rashad", "type": "Artist", "origin": "Chicago, USA", "active_since": 1998 } },
    { "id": "artist:black_coffee", "attrs": { "name": "Black Coffee", "type": "Artist", "origin": "Durban, South Africa", "active_since": 1994 } },
    { "id": "artist:keinemusik", "attrs": { "name": "Keinemusik", "type": "Artist", "origin": "Berlin, Germany", "active_since": 2009 } },
    { "id": "artist:kabza_de_small", "attrs": { "name": "Kabza De Small", "type": "Artist", "origin": "eMalahleni, South Africa", "active_since": 2009 } },
    { "id": "artist:jane_remover", "attrs": { "name": "Jane Remover", "type": "Artist", "origin": "Northern New Jersey, USA", "active_since": 2020 } },

    { "id": "track:taking_drugs", "attrs": { "name": "Taking Drugs?", "type": "Track", "release_year": 2004 } },
    { "id": "track:velvet_paws", "attrs": { "name": "Velvet Paws", "type": "Track", "release_year": 2008 } },
    { "id": "track:we_are_your_friends", "attrs": { "name": "We Are Your Friends", "type": "Track", "release_year": 2006 } },
    { "id": "track:day_n_nite_remix", "attrs": { "name": "Day 'n' Nite (Crookers Remix)", "type": "Track", "release_year": 2008 } },
    { "id": "track:floral_shoppe", "attrs": { "name": "Floral Shoppe", "type": "Track", "release_year": 2011 } },
    { "id": "track:beautiful", "attrs": { "name": "Beautiful", "type": "Track", "release_year": 2014 } },
    { "id": "track:vroom_vroom", "attrs": { "name": "Vroom Vroom", "type": "Track", "release_year": 2016 } },
    { "id": "track:money_machine", "attrs": { "name": "Money Machine", "type": "Track", "release_year": 2019 } },
    { "id": "track:drive", "attrs": { "name": "Drive", "type": "Track", "release_year": 2018 } },
    { "id": "track:move", "attrs": { "name": "Move", "type": "Track", "release_year": 2022 } },

    { "id": "label:ed_banger", "attrs": { "name": "Ed Banger Records", "type": "Label", "origin": "Paris, France", "founded": 2003 } },
    { "id": "label:kompakt", "attrs": { "name": "Kompakt", "type": "Label", "origin": "Cologne, Germany", "founded": 1998 } },
    { "id": "label:hyperdub", "attrs": { "name": "Hyperdub", "type": "Label", "origin": "London, UK", "founded": 2004 } },
    { "id": "label:pc_music", "attrs": { "name": "PC Music", "type": "Label", "origin": "London, UK", "founded": 2013 } },
    { "id": "label:pan", "attrs": { "name": "PAN", "type": "Label", "origin": "Berlin, Germany", "founded": 2008 } },
    { "id": "label:soulistic", "attrs": { "name": "Soulistic Music", "type": "Label", "origin": "Johannesburg, South Africa", "founded": 2005 } },

    { "id": "platform:hypemachine", "attrs": { "name": "Hype Machine", "type": "Platform", "detail": "MP3 Blog Aggregator" } },
    { "id": "platform:soundcloud", "attrs": { "name": "SoundCloud", "type": "Platform", "detail": "Decentralized Hosting" } },
    { "id": "platform:spotify", "attrs": { "name": "Spotify", "type": "Platform", "detail": "Algorithmic Recommender" } },
    { "id": "platform:tiktok", "attrs": { "name": "TikTok", "type": "Platform", "detail": "Short-Form Video & Algorithmic Virality" } }
  ],
  "edges": [
    { "id": "genre:detroit_techno", "directed": false, "attrs": { "name": "Detroit Techno", "type": "Genre", "era": "1980s-present", "i2t:category": "Containment" } },
    { "id": "genre:minimal_techno", "directed": false, "attrs": { "name": "Minimal Techno", "type": "Genre", "era": "2000-2010", "i2t:category": "Containment" } },
    { "id": "genre:blog_house", "directed": false, "attrs": { "name": "Blog House", "type": "Genre", "era": "2005-2010", "i2t:category": "Containment" } },
    { "id": "genre:dubstep", "directed": false, "attrs": { "name": "Dubstep", "type": "Genre", "era": "2000-2012", "i2t:category": "Containment" } },
    { "id": "genre:vaporwave", "directed": false, "attrs": { "name": "Vaporwave", "type": "Genre", "era": "2010-2016", "i2t:category": "Reference" } },
    { "id": "genre:hyperpop", "directed": false, "attrs": { "name": "Hyperpop", "type": "Genre", "era": "2013-present", "i2t:category": "State Change" } },
    { "id": "genre:deconstructed_club", "directed": false, "attrs": { "name": "Deconstructed Club", "type": "Genre", "era": "2013-present", "i2t:category": "Interactivity" } },
    { "id": "genre:afro_house", "directed": false, "attrs": { "name": "Afro House", "type": "Genre", "era": "2010-present", "i2t:category": "Containment" } },
    { "id": "genre:amapiano", "directed": false, "attrs": { "name": "Amapiano", "type": "Genre", "era": "2018-present", "i2t:category": "Containment" } },
    { "id": "genre:dariacore", "directed": false, "attrs": { "name": "Dariacore / Hyperflip", "type": "Genre", "era": "2021-present", "i2t:category": "State Change" } },
    { "id": "network:algorithmic_gatekeeping", "directed": true, "attrs": { "name": "Algorithmic Reification", "type": "Structural_Influence", "i2t:category": "Reference" } }
  ],
  "incidences": [
    { "edge": "genre:detroit_techno", "node": "artist:jeff_mills", "role": "pioneer" },
    { "edge": "genre:detroit_techno", "node": "artist:robert_hood", "role": "pioneer" },

    { "edge": "genre:minimal_techno", "node": "artist:move_d", "role": "innovator" },
    { "edge": "genre:minimal_techno", "node": "artist:benjamin_brunn", "role": "collaborator" },
    { "edge": "genre:minimal_techno", "node": "label:kompakt", "role": "hub" },
    { "edge": "genre:minimal_techno", "node": "track:velvet_paws", "role": "canonical_artifact" },

    { "edge": "genre:blog_house", "node": "artist:justice", "role": "pioneer" },
    { "edge": "genre:blog_house", "node": "artist:sebastian", "role": "innovator" },
    { "edge": "genre:blog_house", "node": "artist:crookers", "role": "crossover_bridge" },
    { "edge": "genre:blog_house", "node": "label:ed_banger", "role": "hub" },
    { "edge": "genre:blog_house", "node": "platform:hypemachine", "role": "distribution_infrastructure" },
    { "edge": "genre:blog_house", "node": "track:we_are_your_friends", "role": "defining_artifact" },
    { "edge": "genre:blog_house", "node": "track:day_n_nite_remix", "role": "crossover_artifact" },

    { "edge": "genre:dubstep", "node": "artist:skream", "role": "pioneer" },
    { "edge": "genre:dubstep", "node": "artist:burial", "role": "innovator" },
    { "edge": "genre:dubstep", "node": "label:hyperdub", "role": "hub" },

    { "edge": "genre:vaporwave", "node": "artist:oneohtrix_point_never", "role": "pioneer" },
    { "edge": "genre:vaporwave", "node": "artist:macintosh_plus", "role": "codifier" },
    { "edge": "genre:vaporwave", "node": "platform:soundcloud", "role": "distribution_infrastructure" },
    { "edge": "genre:vaporwave", "node": "track:floral_shoppe", "role": "canonical_artifact" },

    { "edge": "genre:hyperpop", "node": "artist:ag_cook", "role": "pioneer" },
    { "edge": "genre:hyperpop", "node": "artist:sophie", "role": "innovator" },
    { "edge": "genre:hyperpop", "node": "artist:charli_xcx", "role": "crossover_bridge" },
    { "edge": "genre:hyperpop", "node": "artist:100_gecs", "role": "accelerator" },
    { "edge": "genre:hyperpop", "node": "label:pc_music", "role": "hub" },
    { "edge": "genre:hyperpop", "node": "track:beautiful", "role": "proto_artifact" },
    { "edge": "genre:hyperpop", "node": "track:vroom_vroom", "role": "crossover_artifact" },
    { "edge": "genre:hyperpop", "node": "track:money_machine", "role": "viral_artifact" },

    { "edge": "genre:deconstructed_club", "node": "artist:arca", "role": "pioneer" },
    { "edge": "genre:deconstructed_club", "node": "artist:lotic", "role": "innovator" },
    { "edge": "genre:deconstructed_club", "node": "artist:sophie", "role": "crossover_bridge" },
    { "edge": "genre:deconstructed_club", "node": "label:pan", "role": "hub" },

    { "edge": "genre:afro_house", "node": "artist:black_coffee", "role": "pioneer" },
    { "edge": "genre:afro_house", "node": "artist:keinemusik", "role": "global_distributor" },
    { "edge": "genre:afro_house", "node": "label:soulistic", "role": "hub" },
    { "edge": "genre:afro_house", "node": "track:drive", "role": "crossover_artifact" },
    { "edge": "genre:afro_house", "node": "track:move", "role": "viral_artifact" },

    { "edge": "genre:amapiano", "node": "artist:kabza_de_small", "role": "pioneer" },

    { "edge": "genre:dariacore", "node": "artist:jane_remover", "role": "founder" },
    { "edge": "genre:dariacore", "node": "platform:soundcloud", "role": "distribution_infrastructure" },
    { "edge": "genre:dariacore", "node": "platform:tiktok", "role": "viral_catalyst" },

    { "edge": "network:algorithmic_gatekeeping", "node": "platform:spotify", "role": "source" },
    { "edge": "network:algorithmic_gatekeeping", "node": "genre:hyperpop", "role": "target" }
  ]
}
```
