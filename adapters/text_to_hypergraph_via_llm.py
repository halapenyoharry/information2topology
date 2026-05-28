#!/usr/bin/env python3
"""Adapter: arbitrary source text → InstaGraph-with-i2t-extensions JSON via Claude API.

This is the LLM-based ingestion path: instead of writing a per-source-format
heuristic adapter (regex, alias tables, pattern matching), feed the source text
to Claude with the editorial-discipline prompt template (prompts/text_to_topothink_hypergraph.md)
and let it produce the graph. Output then chains through instagraph_to_hypergraph.py
and hypergraph_to_dyadic.py for canonical-format and JVV-loadable forms.

Usage:
    export ANTHROPIC_API_KEY=...
    python3 adapters/text_to_hypergraph_via_llm.py source.txt -o out.instagraph.json
    python3 adapters/instagraph_to_hypergraph.py out.instagraph.json
    python3 adapters/hypergraph_to_dyadic.py out.hypergraph.topothink.json

The system prompt is sent with prompt_caching enabled; re-running on different
sources within ~5 minutes pays only the cache-read cost for the prompt portion
(~10x cheaper than re-uploading).

Defaults:
    Model:       claude-opus-4-7 (override with --model)
    Temperature: 0 (deterministic within a run)
    Max output:  16000 tokens (large enough for ~100-node graphs)
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("error: 'anthropic' package not installed", file=sys.stderr)
    print("  install: pip install anthropic", file=sys.stderr)
    print("  or in a venv: python3 -m venv .venv && source .venv/bin/activate && pip install anthropic", file=sys.stderr)
    sys.exit(1)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPT_PATH  = PROJECT_ROOT / "prompts" / "text_to_topothink_hypergraph.md"

DEFAULT_MODEL = "claude-opus-4-7"
MAX_OUTPUT_TOKENS = 16000

# Per-million-tokens pricing for cost estimate (claude-opus-4-7 as of 2026).
# Approximate; check the API console for exact current pricing.
PRICING = {
    "claude-opus-4-7":          {"input": 15.0, "cached_read": 1.50, "output": 75.0},
    "claude-sonnet-4-6":        {"input":  3.0, "cached_read": 0.30, "output": 15.0},
    "claude-haiku-4-5-20251001":{"input":  0.8, "cached_read": 0.08, "output":  4.0},
}


def load_prompt() -> str:
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


def extract(client: "anthropic.Anthropic", source_text: str,
            model: str = DEFAULT_MODEL) -> tuple[dict, dict]:
    """Call Claude. Return (parsed_json, usage_metadata)."""
    system_prompt = load_prompt()

    response = client.messages.create(
        model=model,
        max_tokens=MAX_OUTPUT_TOKENS,
        temperature=0,
        system=[{
            "type": "text",
            "text": system_prompt,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": source_text}],
    )

    # Concatenate all text blocks (usually one)
    raw = "".join(block.text for block in response.content if block.type == "text")
    cleaned = strip_code_fences(raw)

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as e:
        # Try to recover by finding the outermost { ... } in the response
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(0))
            except json.JSONDecodeError:
                raise e
        else:
            raise

    usage = response.usage
    metadata = {
        "model": model,
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", 0) or 0,
        "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0) or 0,
        "stop_reason": response.stop_reason,
    }
    return parsed, metadata


def estimate_cost_usd(metadata: dict) -> float:
    """Rough cost estimate based on per-million-tokens pricing table."""
    p = PRICING.get(metadata["model"])
    if not p:
        return 0.0
    return (
        metadata["input_tokens"]               * p["input"]       / 1_000_000
        + metadata["cache_read_input_tokens"]    * p["cached_read"] / 1_000_000
        + metadata["cache_creation_input_tokens"] * p["input"]      / 1_000_000  # cache create costs the same as fresh input
        + metadata["output_tokens"]              * p["output"]      / 1_000_000
    )


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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("input", help="Source text file (any encoding-safe text format)")
    ap.add_argument("-o", "--output", required=True,
                    help="Output InstaGraph-with-i2t-extensions JSON file. "
                         "Run instagraph_to_hypergraph.py on it next for canonical form.")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"Anthropic model ID (default: {DEFAULT_MODEL}). "
                         "Sonnet/Haiku cost less but produce simpler graphs.")
    ap.add_argument("--no-validate", action="store_true",
                    help="Skip output validation (write whatever the model returned)")
    args = ap.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        print("  set it with: export ANTHROPIC_API_KEY=sk-ant-...", file=sys.stderr)
        return 1

    inpath = Path(args.input)
    if not inpath.exists():
        print(f"error: input file not found: {inpath}", file=sys.stderr)
        return 1

    source_text = inpath.read_text(encoding="utf-8")
    char_count = len(source_text)
    print(f"reading {inpath} ({char_count:,} chars)", file=sys.stderr)
    if char_count > 150_000:
        print(f"warning: source is {char_count:,} chars; single-pass extraction may", file=sys.stderr)
        print("         hit context-window or output-token limits. Chunking is", file=sys.stderr)
        print("         a planned follow-up; for now consider splitting the source", file=sys.stderr)
        print("         (e.g., by chapter) and merging the resulting graphs.", file=sys.stderr)

    print(f"calling {args.model} (system prompt cached)...", file=sys.stderr)

    client = anthropic.Anthropic(api_key=api_key)

    try:
        parsed, metadata = extract(client, source_text, model=args.model)
    except json.JSONDecodeError as e:
        print(f"error: model output was not parseable as JSON ({e})", file=sys.stderr)
        print("       try re-running, or use --model claude-opus-4-7 for higher reliability",
              file=sys.stderr)
        return 1
    except anthropic.APIError as e:
        print(f"error: Anthropic API error: {e}", file=sys.stderr)
        return 1

    # Validate
    if not args.no_validate:
        errors = validate_instagraph(parsed)
        if errors:
            print(f"warning: output has {len(errors)} validation issues:", file=sys.stderr)
            for err in errors[:10]:
                print(f"    - {err}", file=sys.stderr)
            if len(errors) > 10:
                print(f"    ... and {len(errors) - 10} more", file=sys.stderr)
            print("(writing anyway; inspect manually)", file=sys.stderr)

    # Add provenance to metadata
    parsed.setdefault("metadata", {})
    parsed["metadata"]["extractor_model"] = metadata["model"]
    parsed["metadata"]["extracted_via"] = "text_to_hypergraph_via_llm.py"

    outpath = Path(args.output)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text(json.dumps(parsed, indent=2), encoding="utf-8")

    print(f"wrote {outpath}", file=sys.stderr)
    print(f"  nodes: {len(parsed.get('nodes', [])):>4}", file=sys.stderr)
    print(f"  edges: {len(parsed.get('edges', [])):>4}", file=sys.stderr)
    print(f"  tokens: input={metadata['input_tokens']:,}  "
          f"cache_create={metadata['cache_creation_input_tokens']:,}  "
          f"cache_read={metadata['cache_read_input_tokens']:,}  "
          f"output={metadata['output_tokens']:,}", file=sys.stderr)
    print(f"  estimated cost: ${estimate_cost_usd(metadata):.4f}", file=sys.stderr)
    print(f"  stop_reason: {metadata['stop_reason']}", file=sys.stderr)
    if metadata["stop_reason"] == "max_tokens":
        print("  ⚠ output may be truncated — increase MAX_OUTPUT_TOKENS or chunk the source",
              file=sys.stderr)
    print(f"\nnext steps:", file=sys.stderr)
    print(f"  python3 adapters/instagraph_to_hypergraph.py {outpath}", file=sys.stderr)
    hg_path = outpath.with_name(outpath.stem.replace(".instagraph", "") + ".hypergraph.topothink.json")
    print(f"  python3 adapters/hypergraph_to_dyadic.py {hg_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
