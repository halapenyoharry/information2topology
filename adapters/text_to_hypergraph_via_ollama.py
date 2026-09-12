#!/usr/bin/env python3
"""Adapter: arbitrary source text → InstaGraph-with-i2t-extensions JSON via local Ollama model.

This is the local-AI variant of text_to_hypergraph_via_llm.py. Instead of
calling the Anthropic API, it talks to a local Ollama instance using the
OpenAI-compatible chat/completions endpoint. No API key needed — just a
running Ollama with a model pulled.

The same system prompt (prompts/text_to_topothink_hypergraph.md) is used.
Output chains through instagraph_to_hypergraph.py and hypergraph_to_dyadic.py
just like the cloud version.

Usage:
    # Start ollama if not running:
    ollama serve &

    # Pull a model (one-time):
    ollama pull mistral-nemo    # 12B, good balance
    ollama pull llama3.1:70b    # best quality, needs ~40GB VRAM

    # Run extraction:
    python3 adapters/text_to_hypergraph_via_ollama.py source.txt -o out.instagraph.json
    python3 adapters/instagraph_to_hypergraph.py out.instagraph.json
    python3 adapters/hypergraph_to_dyadic.py out.hypergraph.topothink.json

Defaults:
    Model:       mistral-nemo (override with --model)
    Ollama URL:  http://localhost:11434 (override with --ollama-url or OLLAMA_HOST)
    Temperature: 0
    Max output:  16000 tokens
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import os
from pathlib import Path
from urllib import request, error

# Import shared utilities (no external dependencies)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from extraction_common import (
    load_prompt,
    strip_code_fences,
    validate_instagraph,
    anchor_to_source,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_MODEL = "mistral-nemo"
DEFAULT_OLLAMA_URL = "http://localhost:11434"
MAX_OUTPUT_TOKENS = 16000


def get_ollama_url() -> str:
    """Resolve Ollama base URL from env or default."""
    return os.environ.get("OLLAMA_HOST", DEFAULT_OLLAMA_URL).rstrip("/")


def check_ollama_available(base_url: str) -> bool:
    """Quick check that Ollama is reachable."""
    try:
        req = request.Request(f"{base_url}/api/tags", method="GET")
        with request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except (error.URLError, OSError):
        return False


def check_model_available(base_url: str, model: str) -> bool:
    """Check if the requested model is pulled in Ollama."""
    try:
        req = request.Request(f"{base_url}/api/tags", method="GET")
        with request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            names = [m.get("name", "") for m in data.get("models", [])]
            # Match with or without tag suffix
            return any(
                n == model or n.startswith(f"{model}:") or n == f"{model}:latest"
                for n in names
            )
    except (error.URLError, OSError, json.JSONDecodeError):
        return False



def chunk_text(text: str, max_chunk_len: int = 1500) -> list[str]:
    """Split text into chunks by double newline, up to ~max_chunk_len."""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_len = 0
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if current_len + len(p) > max_chunk_len and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [p]
            current_len = len(p)
        else:
            current_chunk.append(p)
            current_len += len(p)
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    return chunks

def extract(base_url: str, source_text: str,
            model: str = DEFAULT_MODEL, graph_context: dict | None = None) -> tuple[dict, dict]:
    """Call Ollama via OpenAI-compatible endpoint. Return (parsed_json, usage_metadata)."""
    system_prompt = load_prompt()

    if graph_context:
        # Inject existing nodes into prompt to allow ID reuse
        nodes_json = json.dumps(graph_context.get("nodes", []), indent=2)
        system_prompt += f"\n\n--- CURRENT GRAPH STATE ---\nThe following nodes have already been extracted from previous chunks. You MAY reuse their `id`s if the text refers to them, but DO NOT output them again unless you are modifying them.\n{nodes_json}\n---------------------------\n"
        system_prompt += "\n\nExtract ONLY the NEW nodes and edges for the following text chunk:"

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": source_text},
        ],
        "stream": False,
        "options": {
            "temperature": 0,
            "num_predict": MAX_OUTPUT_TOKENS,
        },
        "format": "json",  # request JSON mode if the model supports it
    }).encode("utf-8")

    req = request.Request(
        f"{base_url}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=3600) as resp:  # 60 min timeout for large texts
            response = json.loads(resp.read())
    except error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"error: Ollama HTTP {e.code}: {body[:500]}", file=sys.stderr)
        sys.exit(1)
    except error.URLError as e:
        print(f"error: cannot reach Ollama at {base_url}: {e}", file=sys.stderr)
        sys.exit(1)

    raw = response.get("message", {}).get("content", "")
    cleaned = strip_code_fences(raw)

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as e:
        # Try to recover by finding the outermost { ... }
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(0))
            except json.JSONDecodeError:
                raise e
        else:
            raise

    metadata = {
        "model": model,
        "total_duration_ns": response.get("total_duration", 0),
        "eval_count": response.get("eval_count", 0),
        "prompt_eval_count": response.get("prompt_eval_count", 0),
    }
    return parsed, metadata


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Extract a TopoThink hypergraph from source text using a local Ollama model."
    )
    ap.add_argument("input", help="Source text file")
    ap.add_argument("-o", "--output", required=True,
                    help="Output InstaGraph-with-i2t-extensions JSON file")
    ap.add_argument("--model", default=DEFAULT_MODEL,
                    help=f"Ollama model name (default: {DEFAULT_MODEL}). "
                         "Use 'ollama list' to see available models.")
    ap.add_argument("--ollama-url", default=None,
                    help=f"Ollama base URL (default: {DEFAULT_OLLAMA_URL} or OLLAMA_HOST env)")
    ap.add_argument("--no-validate", action="store_true",
                    help="Skip output validation")
    ap.add_argument("--chunked", action="store_true",
                    help="Extract in chunks to save context window (recommended for local models)")
    args = ap.parse_args()

    base_url = args.ollama_url or get_ollama_url()

    # Pre-flight checks
    if not check_ollama_available(base_url):
        print(f"error: Ollama not reachable at {base_url}", file=sys.stderr)
        print(f"  start it with: ollama serve", file=sys.stderr)
        return 1

    if not check_model_available(base_url, args.model):
        print(f"error: model '{args.model}' not found in Ollama", file=sys.stderr)
        print(f"  pull it with: ollama pull {args.model}", file=sys.stderr)
        print(f"  or list available: ollama list", file=sys.stderr)
        return 1

    inpath = Path(args.input)
    if not inpath.exists():
        print(f"error: input file not found: {inpath}", file=sys.stderr)
        return 1

    source_text = inpath.read_text(encoding="utf-8")
    char_count = len(source_text)
    print(f"reading {inpath} ({char_count:,} chars)", file=sys.stderr)

    # Local models have smaller context windows — warn at lower threshold
    if char_count > 50_000:
        print(f"warning: source is {char_count:,} chars; local models typically have",
              file=sys.stderr)
        print("         8K-32K context windows. Consider splitting the source.",
              file=sys.stderr)

    print(f"calling {args.model} at {base_url}...", file=sys.stderr)

    if args.chunked:
        chunks = chunk_text(source_text)
        print(f"split source into {len(chunks)} chunks.", file=sys.stderr)
        master_graph = {"nodes": [], "edges": []}
        total_meta = {"model": args.model, "total_duration_ns": 0, "eval_count": 0, "prompt_eval_count": 0}
        
        for i, chunk in enumerate(chunks):
            print(f"processing chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...", file=sys.stderr)
            try:
                parsed, metadata = extract(base_url, chunk, model=args.model, graph_context=master_graph)
                master_graph["nodes"].extend(parsed.get("nodes", []))
                master_graph["edges"].extend(parsed.get("edges", []))
                total_meta["total_duration_ns"] += metadata["total_duration_ns"]
                total_meta["eval_count"] += metadata["eval_count"]
                total_meta["prompt_eval_count"] += metadata["prompt_eval_count"]
            except Exception as e:
                print(f"error on chunk {i+1}: {e}", file=sys.stderr)
                
        # Deduplicate nodes by ID
        unique_nodes = {}
        for n in master_graph["nodes"]:
            if "id" in n:
                unique_nodes[n["id"]] = n
        master_graph["nodes"] = list(unique_nodes.values())
        parsed = master_graph
        metadata = total_meta
    else:
        try:
            parsed, metadata = extract(base_url, source_text, model=args.model)
        except json.JSONDecodeError as e:
            print(f"error: model output was not parseable as JSON ({e})", file=sys.stderr)
            print("       try a larger model or re-run", file=sys.stderr)
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

    # Add provenance
    parsed.setdefault("metadata", {})
    parsed["metadata"]["extractor_model"] = metadata["model"]
    parsed["metadata"]["extracted_via"] = "text_to_hypergraph_via_ollama.py"
    parsed["metadata"]["local_ai"] = True

    # Anchor labels back to source positions
    total_items = len(parsed.get("edges", [])) + len(parsed.get("nodes", []))
    anchored = anchor_to_source(parsed, source_text)
    print(f"  source anchoring: {anchored} of {total_items} items anchored",
          file=sys.stderr)

    outpath = Path(args.output)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    outpath.write_text(json.dumps(parsed, indent=2), encoding="utf-8")

    print(f"wrote {outpath}", file=sys.stderr)
    print(f"  nodes: {len(parsed.get('nodes', [])):>4}", file=sys.stderr)
    print(f"  edges: {len(parsed.get('edges', [])):>4}", file=sys.stderr)

    duration_s = metadata["total_duration_ns"] / 1_000_000_000
    print(f"  tokens: prompt_eval={metadata['prompt_eval_count']:,}  "
          f"eval={metadata['eval_count']:,}", file=sys.stderr)
    print(f"  duration: {duration_s:.1f}s", file=sys.stderr)
    print(f"  cost: $0.00 (local)", file=sys.stderr)

    print(f"\nnext steps:", file=sys.stderr)
    print(f"  python3 adapters/instagraph_to_hypergraph.py {outpath}", file=sys.stderr)
    hg_path = outpath.with_name(
        outpath.stem.replace(".instagraph", "") + ".hypergraph.topothink.json"
    )
    print(f"  python3 adapters/hypergraph_to_dyadic.py {hg_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
