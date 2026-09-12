# Requirements for Local AI Extraction Model (Information to Topology)

To successfully extract TopoThink hypergraphs that can anchor to Exoskeleton's text panes via the OSC bus, a local LLM must meet several strict requirements. 

If running on a single RTX 3090 (24GB VRAM), we need a model that maximizes instruction-following and JSON adherence while fitting within memory (typically meaning an 8B to 30B parameter model, heavily quantized if on the larger end).

## Core Requirements

### 1. Verbatim Quoting (Critical for OSC Anchoring)
**Requirement:** The model must be able to strictly follow instructions like `"Extract the EXACT string, DO NOT modify the text even a single character."`
**Why it matters:** Our `anchor_to_source` post-processor relies on exact substring matching. If the model summarizes (e.g., outputs "King Daśaratha" when the text reads "Daśaratha") or normalizes punctuation, the string cannot be found in the source text. If it cannot be found, it cannot be assigned a `source_line` and `source_char_offset`, which means clicking the node in the Exoskeleton graph viewer will not scroll the text editor.
**Common failures:** Smaller models tend to paraphrase, summarize, or resolve pronouns (e.g., changing "he" to the character's name) instead of quoting exactly.

### 2. Strict JSON Schema Adherence
**Requirement:** The model must reliably output well-formed JSON matching the `InstaGraph` schema without Markdown code fences, trailing commas, or missing brackets.
**Why it matters:** The pipeline expects a machine-readable format. While `extraction_common.py` can strip ```json fences, it cannot fix structural JSON errors.
**Mitigation:** We can use Ollama's `format: "json"` flag, but the model still needs to understand the specific schema we prompt it with.

### 3. Context Window Size
**Requirement:** The model needs a context window of at least 8K to 16K tokens.
**Why it matters:** Users will paste large chunks of text (entire scenes or chapters) into Exoskeleton. The prompt itself is also quite long, detailing the topological categories (State Change, Containment, etc.).
**Common failures:** If the context window is too small, the model will "forget" the JSON schema instructions placed at the beginning of the prompt.

### 4. Relational/Topological Reasoning
**Requirement:** The model must be capable of understanding the four TopoThink relational categories (Interactivity, Containment, State Change, Reference) and correctly categorizing the edges it extracts.
**Why it matters:** This is the core philosophical aim of the Information to Topology project.

---

## Benchmarking / Selection Criteria for RTX 3090 (24GB VRAM)

When evaluating models for the V2 test, look for these traits:

1. **High "Needle in a Haystack" (NIAH) performance:** Models that score well on retrieving exact text from a large context tend to be better at verbatim quoting.
2. **Coding / Structured Output bias:** Models fine-tuned on code (like `Qwen2.5-Coder-32B` quantized, or `Command R`) are generally much better at strict JSON adherence and following structural rules than general-purpose chat models.
3. **Parameter Size:** 
   - **8B - 14B models** (e.g., Llama 3 8B, Qwen 2.5 14B) run extremely fast and leave plenty of VRAM for massive context windows (up to 128k).
   - **27B - 34B models** (e.g., Gemma 2 27B, Command R 35B) can fit on a 24GB 3090 if quantized (e.g., Q4_K_M GGUF format). They offer much better reasoning and instruction-following, but you may need to limit the context window to ~8K-16K tokens to avoid Out of Memory (OOM) errors.

## Suggested Models to Research
*   **Qwen2.5-Coder (14B or 32B-Q4):** Exceptionally strong at following complex JSON schemas and formatting instructions.
*   **Command R (35B-Q4):** Specifically trained for Retrieval Augmented Generation (RAG), meaning it is heavily biased toward quoting source text exactly rather than hallucinating.
*   **Llama 3.1 (8B):** Very fast, massive context window, decent instruction following.
