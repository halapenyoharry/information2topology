"""Shared utilities for text-to-hypergraph adapters.

Functions here are used by both the cloud (Anthropic) and local (Ollama)
extraction adapters. They have no external dependencies beyond the stdlib.
"""
from __future__ import annotations
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATH  = PROJECT_ROOT / "prompts" / "text_to_topothink_hypergraph.md"


def load_prompt() -> str:
    """Load the extraction system prompt."""
    import sys
    if not PROMPT_PATH.exists():
        sys.exit(f"error: prompt template not found at {PROMPT_PATH}")
    return PROMPT_PATH.read_text(encoding="utf-8")


def strip_code_fences(text: str) -> str:
    """Remove markdown code fences if the model wrapped JSON in ```json ... ```."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].rstrip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    return text.strip()


def validate_instagraph(doc: dict) -> list[str]:
    """Structural validation enforcing the editorial-discipline rule that every
    edge MUST carry a text-evidence `label`. Returns list of error messages.
    """
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["top-level output is not a JSON object"]
    for required_key in ("nodes", "edges"):
        if required_key not in doc:
            errors.append(f"missing top-level '{required_key}' array")
        elif not isinstance(doc[required_key], list):
            errors.append(f"'{required_key}' is not a list")

    nodes = doc.get("nodes", [])
    edges = doc.get("edges", [])

    node_ids: set[str] = set()
    for i, n in enumerate(nodes):
        if not isinstance(n, dict):
            errors.append(f"nodes[{i}] is not an object")
            continue
        nid = n.get("id")
        if not nid:
            errors.append(f"nodes[{i}] missing 'id'")
            continue
        if nid in node_ids:
            errors.append(f"nodes[{i}] duplicate id: {nid}")
        node_ids.add(nid)

    for i, e in enumerate(edges):
        if not isinstance(e, dict):
            errors.append(f"edges[{i}] is not an object")
            continue
        if not e.get("label"):
            errors.append(f"edges[{i}] missing 'label' — every edge must carry text evidence (editorial discipline)")
        # Check from/to OR members
        has_from_to = "from" in e and "to" in e
        has_members = "members" in e
        if not (has_from_to or has_members):
            errors.append(f"edges[{i}] needs either from/to or members")
        if has_members and not isinstance(e["members"], list):
            errors.append(f"edges[{i}] 'members' is not a list")

    return errors


def _build_line_index(text: str) -> list[int]:
    """Return a list mapping character offset → 1-indexed line number.

    line_index[i] gives the line number for character position i.
    Built once per source text, then used for O(1) lookups.
    """
    index = []
    line = 1
    for ch in text:
        index.append(line)
        if ch == '\n':
            line += 1
    return index


def anchor_to_source(doc: dict, source_text: str) -> int:
    """Post-process LLM output to anchor labels back to source positions.

    Searches primarily for `properties.exact_quote`, falling back to `label` or `text`.
    Uses an ASCII-normalized index to robustly match despite diacritics or punctuation differences.

    Returns the number of items successfully anchored.
    """
    import unicodedata

    line_index = _build_line_index(source_text)
    
    # Build normalized mapping
    orig_indices = []
    norm_chars = []
    
    for i, ch in enumerate(source_text):
        nfkd = unicodedata.normalize('NFKD', ch)
        ascii_ch = nfkd.encode('ASCII', 'ignore').decode('ASCII').lower()
        if not ascii_ch.isalnum():
            ascii_ch = ' '
            
        for c in ascii_ch:
            if c == ' ':
                if not norm_chars or norm_chars[-1] != ' ':
                    norm_chars.append(' ')
                    orig_indices.append(i)
            else:
                norm_chars.append(c)
                orig_indices.append(i)
                
    norm_source = "".join(norm_chars)
    anchored = 0

    def find_offset(needle: str) -> tuple[int, int] | None:
        """Find needle in source_text, return (line, char_offset) or None."""
        if not needle.strip():
            return None
            
        # Try exact first
        idx = source_text.find(needle.strip())
        if idx >= 0 and idx < len(line_index):
            return (line_index[idx], idx)
            
        # Try normalized
        nfkd = unicodedata.normalize('NFKD', needle)
        ascii_n = nfkd.encode('ASCII', 'ignore').decode('ASCII').lower()
        import re
        ascii_n = re.sub(r'[^a-z0-9]', ' ', ascii_n)
        norm_needle = re.sub(r'\s+', ' ', ascii_n).strip()
        
        if not norm_needle:
            return None
            
        norm_idx = norm_source.find(norm_needle)
        if norm_idx >= 0 and norm_idx < len(orig_indices):
            orig_pos = orig_indices[norm_idx]
            return (line_index[orig_pos], orig_pos)
            
        return None

    # Try exact_quote first, then label for edges
    for edge in doc.get("edges", []):
        props = edge.get("properties", {})
        needle = props.get("exact_quote", "") or edge.get("label", "")
        if needle:
            pos = find_offset(needle)
            if pos:
                edge.setdefault("properties", {})
                edge["properties"]["source_line"] = pos[0]
                edge["properties"]["source_char_offset"] = pos[1]
                anchored += 1

    # Try exact_quote first, then text for nodes
    for node in doc.get("nodes", []):
        props = node.get("properties", {})
        needle = props.get("exact_quote", "") or props.get("text", "") or node.get("label", "")
        if needle:
            pos = find_offset(needle)
            if pos:
                props["source_line"] = pos[0]
                props["source_char_offset"] = pos[1]
                anchored += 1

    return anchored
