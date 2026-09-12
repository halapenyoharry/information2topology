#!/usr/bin/env python3
"""Information to Topology (i2t) Engine CLI.

Full Pipeline Command:
    python3 i2t_cli.py extract <input_file> --out <canonical_output.json> [--project]

Features:
- Reads unstructured prose or source input.
- Connects to BYO-AI (OpenRouter / Gemini / OpenAI-compatible / Local CLI).
- Applies TopoThink structural joint tests and categorizes every relation
  into: containment, state_change, interactivity, reference.
- Validates the resulting document against hypergraph.topothink.schema.json.
- Persists canonical ground truth (*.hypergraph.topothink.json).
- Optionally emits the normalized-dyadic projection for Exoskeleton cockpit.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Local engine imports
from engine.classifier import classify_relation
from engine.validator import assert_valid_topothink
from engine.byo_client import ByoAiClient

# Projection adapter
import adapters.hypergraph_to_dyadic as dyadic_adapter


def load_system_prompt() -> str:
    prompt_path = Path(__file__).parent / "prompts" / "text_to_topothink_hypergraph.md"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Missing prompt template at {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def run_extraction(
    input_path: Path,
    output_path: Path,
    client: ByoAiClient,
    emit_projection: bool = True
) -> None:
    print(f"[*] Reading source from: {input_path}")
    raw_text = input_path.read_text(encoding="utf-8")
    source_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()

    prompt = load_system_prompt()
    print(f"[*] Dispatching to AI Engine ({client.model})...")
    raw_response = client.call_ai(prompt, raw_text)

    try:
        extracted = json.loads(raw_response)
    except json.JSONDecodeError as e:
        print(f"[!] Model did not return valid JSON: {e}", file=sys.stderr)
        print(f"Raw output:\n{raw_response[:500]}...", file=sys.stderr)
        sys.exit(1)

    # 1. Transform raw extraction to Canonical TopoThink Format
    print("[*] Normalizing to Canonical TopoThink Hypergraph & classifying joints...")
    nodes: list[dict] = []
    edges: list[dict] = []
    incidences: list[dict] = []

    # Map nodes
    for idx, n in enumerate(extracted.get("nodes", [])):
        nid = n.get("id") or f"node:{idx}"
        attrs = dict(n.get("properties", {}))
        if "label" in n:
            attrs["label"] = n["label"]
        if "type" in n:
            attrs["type"] = n["type"]
        nodes.append({"id": nid, "attrs": attrs})

    # Map edges and adjudicate 4-category classification
    for idx, e in enumerate(extracted.get("edges", [])):
        eid = e.get("id") or f"edge:{idx}"
        pred = e.get("relationship") or e.get("predicate") or "references"
        category = classify_relation(pred)

        attrs = dict(e.get("properties", {}))
        attrs["i2t:predicate"] = pred
        attrs["i2t:category"] = category
        if "label" in e:
            attrs["i2t:evidence"] = e["label"]

        directed = e.get("direction", "directed") == "directed"
        edges.append({"id": eid, "directed": directed, "attrs": attrs})

        # Incidences
        if "members" in e:
            for m in e["members"]:
                if isinstance(m, str):
                    incidences.append({"edge": eid, "node": m, "role": "member"})
                elif isinstance(m, dict):
                    inc = {"edge": eid, "node": m["node"], "role": m.get("role", "member")}
                    if "attrs" in m:
                        inc["attrs"] = m["attrs"]
                    incidences.append(inc)
        elif "from" in e and "to" in e:
            incidences.append({"edge": eid, "node": e["from"], "role": "source"})
            incidences.append({"edge": eid, "node": e["to"], "role": "target"})

    canonical_doc = {
        "metadata": {
            "topothink-version": "0.1",
            "title": input_path.stem,
            "source_file": str(input_path),
            "source_sha256": source_hash,
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "model_used": client.model
        },
        "nodes": nodes,
        "edges": edges,
        "incidences": incidences
    }

    # 2. Validate against schema
    print("[*] Validating structural commitments against hypergraph.topothink.schema.json...")
    assert_valid_topothink(canonical_doc)
    print("    [✓] Schema validation passed.")

    # 3. Save Canonical Ground Truth
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(canonical_doc, f, indent=2)
    print(f"    [✓] Saved Canon to: {output_path} ({len(nodes)} nodes, {len(edges)} edges, {len(incidences)} incidences)")

    # 4. Optional: Emit Projection
    if emit_projection:
        proj_stem = output_path.name.replace(".hypergraph.topothink.json", "")
        if proj_stem == output_path.name:
            proj_stem = output_path.stem
        proj_path = output_path.parent / f"{proj_stem}.normalized-dyadic.json"

        print(f"[*] Emitting Dyadic Projection for Exoskeleton cockpit...")
        proj_doc = dyadic_adapter.normalize(canonical_doc)
        with open(proj_path, "w", encoding="utf-8") as f:
            json.dump(proj_doc, f, indent=2)
        print(f"    [✓] Saved Projection to: {proj_path}")


def main():
    parser = argparse.ArgumentParser(description="Information to Topology (i2t) Engine CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_p = subparsers.add_parser("extract", help="Extract topology from source document")
    extract_p.add_argument("input", type=Path, help="Path to raw source text file")
    extract_p.add_argument("-o", "--out", type=Path, required=True, help="Path for canonical output (.hypergraph.topothink.json)")
    extract_p.add_argument("--project", action="store_true", default=True, help="Also emit .normalized-dyadic.json projection")
    extract_p.add_argument("--api-key", help="BYO API Key (OpenRouter or Gemini)")
    extract_p.add_argument("--base-url", help="BYO API base URL (default: OpenRouter)")
    extract_p.add_argument("--model", help="AI Model to run (default: google/gemini-2.5-flash)")
    extract_p.add_argument("--cli-command", help="BYO Commandline AI (pipes prompt + text to stdin of a shell command)")

    args = parser.parse_args()

    if args.command == "extract":
        client = ByoAiClient(
            api_key=args.api_key,
            base_url=args.base_url,
            model=args.model,
            cli_command=args.cli_command
        )
        run_extraction(
            input_path=args.input,
            output_path=args.out,
            client=client,
            emit_projection=args.project
        )


if __name__ == "__main__":
    main()
