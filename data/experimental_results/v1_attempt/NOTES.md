# V1 Attempt: Gemma 4 on Ramayana Canto 1

**Date:** 2026-08-02
**Model:** `gemma4:latest` (running via Ollama)
**Source Text:** Valmiki's Ramayana (Canto I excerpt, ~12,400 chars)

## Results
- **Extraction success:** Yes, valid InstaGraph JSON was generated.
- **Node Count:** 59 items extracted (nodes + edges).
- **Anchoring success:** FAILED (4 out of 59 items anchored).
- **Graph Validity:** FAILED (4 dangling endpoints generated).

## Notes & Analysis
The extraction pipeline successfully completed from raw text -> InstaGraph -> TopoThink Hypergraph -> Dyadic JSON. However, the semantic content extracted by the model failed our strict anchoring requirements.

**The Anchoring Problem:**
Our pipeline relies on the model quoting the exact source text verbatim for its labels, so that the `anchor_to_source` post-processor can find the string offset and map the graph node back to the exact UI coordinate in the Exoskeleton text editor.
Gemma 4 failed to follow the exact-quote instruction. It summarized (e.g., extracting "King Daśaratha" instead of "Daśaratha") and normalized punctuation. Because the strings didn't exactly match the source text, the anchoring step couldn't find them, meaning clicking these nodes in Exoskeleton would *not* scroll the camera to the right text.

**Next Steps for V2:**
Before running a V2 attempt, we need to either:
1. Find a local AI model more suited to strict instruction following and verbatim quoting.
2. Update the prompt to use Few-Shot examples specifically tailored for local LLMs (the current prompt is optimized for Claude).
3. Relax the anchoring script to use fuzzy string matching.
