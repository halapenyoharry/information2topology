# Personal Droids

*Memory graphs and functional specialization as the foundation for AI that runs on your own hardware, remembers what it has done, and stays itself across conversations.*

The shape of current AI assistance is general capability without persistent memory. You can ask anything. The system answers. The next conversation, it does not remember the last one, does not know what you decided, does not carry forward the texture of how you work. Some products glue on a "memory" feature, usually a flat list of facts the system has been told to retain. The gluing is not the mechanism. The mechanism is structural, and the structure is graph-shaped.

R2D2 is specialized and remembered. He repairs starfighters, slices Imperial systems, plays back recorded messages, and across the films he carries the same memories of the same people doing the same work. He is not a generalist who occasionally retrieves a fact. He is a *specific droid* with a specific role and a specific accumulated history, and that combination is what makes him a character rather than a tool. Current AI gives you generality without the second half. The gap is the topology.

This whitepaper sketches what a memory graph for personal AI would look like, how it would be served, and why the droid framing is the right organizing image for the next generation of personal-hardware agents.

## The shape of memory

Most AI memory implementations are a flat list of facts the user has told the system, dumped into context at the start of every conversation. The flat list is convenient for the implementer. It is wrong for the user. Memory is not a list. Memory is a graph that grows, supersedes itself, contradicts itself, points to its own sources, and gets reshaped every time you learn something that recontextualizes what you thought you knew.

A flat list cannot represent: this fact replaces an earlier fact (supersession), these two beliefs are in tension and the user has not resolved them (contradiction), this principle elaborates that one (containment), this memory came from that conversation on that date and was last verified two months ago (provenance and decay), these memories all concern the writing-craft project rather than the network-topology project (scoping). The graph can. The graph is not optional rigor; it is the minimum structure that lets memory be honest.

The implication for the droid: a droid with a memory graph can answer not just "what do I know" but "what did I used to think, when did I update, why, and where is the source." That is the difference between a system that remembers and a system that has a history.

## The schema, briefly

**Node types.** `Memory` is the atomic unit, carrying body text, name, description, a confidence flag (`fact`, `synthesis`, `hypothesis`, `ephemeral`), a status (`active`, `archived`, `superseded`), and time fields (`created_at`, `updated_at`, `last_verified_at`). `Tag` for retrieval handles, the `#writingcraft #commas` style, first-class so tags can have their own properties. `Topic` for broader semantic groupings built from embeddings or curated by hand. `Source` for provenance, the conversation id or file path or person the memory came from. `Person`, `Project`, `Decision` as the cross-cuts that scope everything else.

**Edge types,** reified as hyperedges in the canonical i2t pattern: `derived_from` connects a memory to its source with a role marker for whether it cites, paraphrases, or quotes; `tagged_with` connects a memory to a tag; `supersedes` produces a directed acyclic graph over time, like the prose-craft v2 file superseding v1; `elaborates`, `contradicts`, and `depends_on` produce the present-tense graph among active memories; `decision_made` is n-ary, binding a Decision to the Person who made it, the Project it concerns, the supporting Memories, and the prose excerpt that captured the reasoning. Every edge carries a prose-excerpt label as its honesty anchor, the same editorial discipline already in the i2t hypergraph format.

**The shape this gives you.** A DAG over time. A graph in the present. Two retrieval indexes (tag and topic) sitting on top. Per-predicate layers as the loadable unit, so you can pull "everything tagged #writingcraft that supersedes a v1" as a single sub-hypergraph rather than the whole store. The schema does not invent new infrastructure; it applies the i2t pattern to a domain (your own cognition) where the topology has been hidden under flat-file conventions for years.

## Files stay the source of truth

There is a temptation, when designing a memory system, to put the database in charge. Don't. The database goes down, gets corrupted, schema-migrates badly, and your memories go with it. The current pattern Claude Code uses, markdown files with frontmatter living in a directory you can `ls`, is the right substrate. Files survive infrastructure failures. Files sync across machines via Syncthing without database-replication ceremony. Files can be read by `cat` in an emergency. The constraint going forward: **the database and the embeddings are derived caches that rebuild from the files. They are never the primary store.**

This is not a small constraint. It rules out a class of database-first designs that would be easier to build but would couple your cognition to your uptime. The droid metaphor depends on the droid retaining its memories when its servers are off. R2D2 does not phone home for his recordings. Neither should yours.

## Serving the graph

Three layers, mapped onto infrastructure that already exists in this household.

**1. Store.** SQLite or DuckDB on lumen for the structured side: nodes, edges, incidences, time fields. Markdown-with-frontmatter files at the existing memory paths for the body content. An embeddings table (sqlite-vss or local Chroma) for semantic recall. The DB is the index, the files are the source of truth, the embeddings are an auxiliary cache.

**2. Query.** A small Python service exposing three query modes: tag lookup (cheap), graph traversal (SQL CTEs or short-lived in-memory loads via HypergraphX for serious topology), and semantic recall (vector similarity over the embeddings). Output adapters hand the same memories back in different shapes: hypergraph view for Claude, dyadic view for Gemma, plain markdown for a human reader. Same store, three readers, the [`docs/ai-collaborator-format-guide.md`](../docs/ai-collaborator-format-guide.md) pattern applied to cognition.

**3. Expose.** Local HTTP on lumen, alongside ollama and the rest of the home services. Pick a unique port from the registry. An MCP server bridge so Claude Code and Gemma-via-ollama can both query the memory graph during a conversation, replacing the "load every markdown file at session start" approach with on-demand recall. The droid gets its memory not by having every fact stuffed into context, but by being able to ask its own memory store what it needs to know, when it needs to know it, and to receive back a sub-hypergraph scoped to the question.

## Cultivating droids

Memory modules are the substrate. Droids are what you build on top. A droid is a specialized AI configuration plus a scoped memory module plus a stable identity that survives the conversation it was instantiated for.

Specialization comes from the system prompt and the toolset. A repair droid has hardware-debug tools, a slicer droid has filesystem and process tools, a translator droid has language tools. None of them needs to be a general assistant. None of them should be. The mistake of the current AI moment is treating every model as a generalist; the more useful unit is the specialized agent that does one thing exceptionally and knows what it has done.

Scoped memory comes from the graph. A repair droid needs the memories tagged `#hardware #repair #incident-history`. A writing droid needs the memories tagged `#writingcraft #voice #reader-feedback`. The same underlying memory store serves both, scoped by tag or project or person, so two droids can share the memories of the events they both touched and diverge on the events they did not. R2D2 and C-3PO have overlapping but distinct memories. So should yours.

Stable identity comes from the persistence of the memory plus the persistence of the configuration. A droid that can be invoked tomorrow with the same name, the same memory scope, and the same toolset is a droid that has continuity. A droid whose every invocation is fresh has no identity to speak of, just a costume worn briefly.

The composition pattern: a household of droids, each specialized, each carrying its own scoped memory, all running on personal hardware, all queryable from any conversation through MCP. Some droids are persistent processes that you can stream events to. Some are spawned per-conversation but pull from the same store. The store outlives any individual droid.

## Why this should run on your laptop

Three reasons that compound.

**Privacy.** Your memories are yours. The model that reads them is yours. The disk they live on is yours. The minute any of those three move into someone else's infrastructure, the relationship between you and the droid changes. You become a tenant. The droid becomes a service. The "your memories" framing becomes a marketing line rather than a structural fact.

**Latency.** Local recall is fast. A memory query that goes to a remote store and back is a query you will not bother to issue. The droid that asks its own memory ten times a conversation is functionally different from the droid that asks once because each round-trip costs you. Local makes the asking cheap, which makes the droid actually use what it knows.

**Ownership of failure modes.** When the network goes down, a local droid still works. When the cloud provider deprecates its API, a local droid still works. When the company pivots its product, a local droid still works. None of this is hypothetical; all of it has happened to people in the last twelve months. The droid that depends on someone else's continued business model is a droid you do not own.

## What this might be wrong about

The droid metaphor could mislead. R2D2 is a fictional character with a writer's room behind him. A real droid in this sense is a memory graph plus a config plus a tool set, not a personality. If the framing seduces people into expecting the persona, the substance, will disappoint.

The memory-graph topology has not been demonstrated to scale to a million memories. The schema is right for thousands, possibly tens of thousands. Beyond that, the indexes will need work, the embeddings will need real attention, and the per-predicate-layer pattern may need to chunk further. None of this is research-grade hard. None of it is solved either.

The "files stay authoritative" constraint is a bet. It is the bet I would make. It might turn out, at sufficient scale, that the database has to be authoritative because rebuilding from files becomes prohibitive. If that day comes, the way to find out is to push the constraint until it breaks rather than to abandon it preemptively.

The MCP exposure is the easiest part to get wrong. An MCP server that lets a model write to the memory graph is dangerous in the way that any agent with persistent state is dangerous. The droid that updates its own memories without supervision can drift in ways the user does not see. Read access without supervision is fine. Write access needs an editorial pass.

## What this is

A schema sketch and a service architecture for AI that remembers. The mechanism is a hypergraph of memories with reified edges and incidence roles, the same i2t pattern already proven on novels and political theory and conversational tics, applied to the substrate (your own cognition) it has been waiting for. The serving architecture is three layers, all local, all built from infrastructure that already exists, with the constraint that markdown files remain the source of truth.

The framing is the droid: specialized function, scoped memory, stable identity, local hardware. Not a generalist that pretends to remember. A specific tool that does. The R2D2 line is not a metaphor; it is a target. Build a droid with persistent memory, repeat the pattern for each function, watch a household of droids accumulate competence and history that survives any individual conversation.

The hard work is not the code. The hard work is the schema, the editorial discipline on what gets remembered and what gets archived, the per-droid scoping decisions, the human judgment about what a droid should be authorized to remember on its own and what should require explicit save. That work is done at the desk where the droid is being cultivated. It is not done by a vendor. The vendor cannot do it for you, because the memories are yours and only you know which ones still carry weight in the work in front of you.

The mechanism is here. The schema is sketched. The serving plan fits on the hardware that is already running. The remaining work is taste, and taste is what you have been refining all along.
