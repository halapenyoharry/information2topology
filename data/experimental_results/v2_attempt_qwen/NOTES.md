# V2 Attempt: Qwen2.5-Coder 32B on Ramayana Canto 1

**Date:** 2026-08-02
**Model:** `qwen2.5-coder:32b-instruct-q4_K_M` (running via Ollama)
**Source Text:** Valmiki's Ramayana (Canto I excerpt, ~12,400 chars)

## Results
- **Extraction success:** Yes, valid InstaGraph JSON was generated.
- **Node Count:** 74 items extracted (nodes + edges).
- **Anchoring success:** FAILED (5 out of 74 items anchored).
- **Execution Time:** ~18 minutes (timed out first attempt, required increasing Ollama timeout to 60 mins).

## Notes & Analysis
Qwen2.5-Coder did a phenomenal job at generating a highly structured, valid JSON schema containing 74 nodes and edges that beautifully mapped the mythological cosmology.

**The Anchoring Problem Persists:**
Despite being an instruction-following powerhouse, Qwen 2.5 suffered from the exact same "exact quote" failure as Gemma 4. In fact, it was slightly worse in a specific way: **Pre-training bleed**.

When reading the Ramayana, Qwen correctly identified the characters (Rama, Sita, Lakshman, Dasaratha, Ravana, etc.). However, instead of quoting the text verbatim, it leaned on its internal pre-training knowledge of the Ramayana to provide canonically correct spellings (e.g., `Daśaratha`, `Śúrpaṇakhá`, `Lakshmaṇ`) that did not precisely match the ASCII/unicode spelling in the provided 1870 Project Gutenberg text. 

Because of this, the `anchor_to_source` post-processor could not find these strings in the raw text, resulting in a 5/74 anchoring success rate.

**Conclusion:**
Local AI models, even highly capable 32B instruction-tuned models, naturally want to be helpful by normalizing data (fixing spelling, standardizing names) rather than acting as a dumb string-copying machine. 

To resolve this, we must:
1. **Fuzzy Match the Anchors**: Modify `adapters/extraction_common.py` to use a fuzzy string matching algorithm (like Levenshtein distance or SequenceMatcher) rather than strict `str.find()`. This will allow `Daśaratha` to anchor to `Dasaratha`.
2. **Implement Node-to-Anchor Separation**: In the prompt, we should instruct the model to provide both a normalized `label` (for the graph UI) AND an `exact_quote` attribute (for the OSC bus), giving the model an outlet to normalize data without breaking our UI pointer.
