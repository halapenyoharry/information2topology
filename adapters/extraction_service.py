#!/usr/bin/env python3
"""Extraction service: HTTP API for the text-to-hypergraph pipeline.

Provides a simple REST endpoint that exoskeleton (or any client) can POST
source text to and receive a hypergraph JSON back.

Usage:
    # Install dependencies (one-time):
    pip install fastapi uvicorn

    # Run the server:
    python3 adapters/extraction_service.py

    # Or with uvicorn directly:
    uvicorn adapters.extraction_service:app --port 8420

    # Test:
    curl -X POST http://localhost:8420/extract \\
         -H 'Content-Type: application/json' \\
         -d '{"text": "Sisyphus pushes the boulder up the hill.", "backend": "algorithmic"}'

Endpoints:
    POST /extract          - Extract a hypergraph from text
    GET  /health           - Health check
    GET  /backends         - List available extraction backends
"""
from __future__ import annotations
import json
import sys
import os
from pathlib import Path

# Ensure adapters directory is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field
    import uvicorn
except ImportError:
    print("error: FastAPI and uvicorn required", file=sys.stderr)
    print("  install: pip install fastapi uvicorn", file=sys.stderr)
    sys.exit(1)

from extraction_common import (
    load_prompt,
    strip_code_fences,
    validate_instagraph,
    anchor_to_source,
)

# Check which backends are available
BACKENDS_AVAILABLE: dict[str, bool] = {
    "algorithmic": True,  # always available — pure Python
    "ollama": False,
    "anthropic": False,
}

# Check Ollama availability
try:
    from text_to_hypergraph_via_ollama import check_ollama_available, get_ollama_url
    if check_ollama_available(get_ollama_url()):
        BACKENDS_AVAILABLE["ollama"] = True
except ImportError:
    pass

# Check Anthropic availability
try:
    import anthropic
    if os.environ.get("ANTHROPIC_API_KEY"):
        BACKENDS_AVAILABLE["anthropic"] = True
except ImportError:
    pass


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="i2t Extraction Service",
    description="Text → TopoThink Hypergraph extraction API",
    version="0.1.0",
)

# Allow exoskeleton (localhost, any port) to call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExtractionRequest(BaseModel):
    text: str = Field(..., description="Source text to extract a hypergraph from")
    backend: str = Field(
        default="algorithmic",
        description="Extraction backend: 'algorithmic' (structural only, instant), "
                    "'ollama' (local AI), or 'anthropic' (cloud AI)"
    )
    model: str | None = Field(
        default=None,
        description="Model name override for AI backends (e.g. 'mistral-nemo', 'claude-sonnet-4-6')"
    )
    source_filename: str | None = Field(
        default=None,
        description="Optional filename for provenance metadata"
    )


class ExtractionResponse(BaseModel):
    hypergraph: dict = Field(..., description="The extracted TopoThink hypergraph JSON")
    backend_used: str
    anchored_count: int = Field(0, description="Number of items successfully source-anchored")
    validation_errors: list[str] = Field(default_factory=list)


@app.get("/health")
async def health():
    return {"status": "ok", "backends": BACKENDS_AVAILABLE}


@app.get("/backends")
async def backends():
    return {
        "backends": BACKENDS_AVAILABLE,
        "default": "algorithmic",
        "description": {
            "algorithmic": "Structural extraction only (paragraphs, sections, sequence). Instant, free, no AI.",
            "ollama": "Full semantic extraction via local Ollama model. Requires ollama serve.",
            "anthropic": "Full semantic extraction via Claude API. Requires ANTHROPIC_API_KEY.",
        }
    }


def _extract_algorithmic(text: str, source_filename: str | None) -> dict:
    """Pure-algorithmic structural extraction: paragraphs, sequence edges, containment."""
    import re

    nodes = []
    edges = []
    paragraphs = []

    # Split on blank lines
    pos = 0
    lines_consumed = 0
    while pos < len(text):
        while pos < len(text) and text[pos] in ' \t\n\r':
            if text[pos] == '\n':
                lines_consumed += 1
            pos += 1
        if pos >= len(text):
            break
        para_line = 1 + lines_consumed
        para_char = pos
        end = text.find('\n\n', pos)
        if end == -1:
            end = len(text)
        p = text[pos:end].strip()
        lines_consumed += text[pos:end].count('\n')
        pos = end
        if not p:
            continue
        paragraphs.append((p, para_line, para_char))

    # Build nodes
    doc_id = "doc:1"
    nodes.append({
        "id": doc_id,
        "attrs": {
            "label": source_filename or "Document",
            "instagraph:type": "Document",
            "instagraph:color": "#C8E0F8",
        }
    })

    para_ids = []
    for i, (p_text, p_line, p_char) in enumerate(paragraphs):
        pid = f"p:{i+1:03d}"
        # Compute a slug from first few words
        slug_words = re.sub(r'[^\w\s]', ' ', p_text).split()[:6]
        slug = '-'.join(w.lower() for w in slug_words)[:60] or "paragraph"

        nodes.append({
            "id": pid,
            "attrs": {
                "label": slug,
                "instagraph:type": "Paragraph",
                "instagraph:color": "#F8F8E8",
                "text": p_text,
                "paragraph_index": i,
                "word_count": len(re.findall(r'\b\w[\w\'-]*\b', p_text)),
                "source_line": p_line,
                "source_char_offset": p_char,
                **({"source_file": source_filename} if source_filename else {}),
            }
        })
        para_ids.append(pid)

    # Containment edge: document contains all paragraphs
    if para_ids:
        contains_id = "contains:doc"
        edges.append({
            "id": contains_id,
            "directed": True,
            "attrs": {
                "i2t:predicate": "document_contains_paragraphs",
                "i2t:edge_category": "containment",
                "label": f"Document contains {len(para_ids)} paragraphs",
            }
        })

    # Sequence edges
    for i in range(len(para_ids) - 1):
        edges.append({
            "id": f"precedes:{para_ids[i]}__{para_ids[i+1]}",
            "directed": True,
            "attrs": {
                "i2t:predicate": "precedes",
                "i2t:edge_category": "state_change",
            }
        })

    # Build incidences
    incidences = []
    if para_ids:
        incidences.append({"edge": "contains:doc", "node": doc_id, "role": "container"})
        for pid in para_ids:
            incidences.append({"edge": "contains:doc", "node": pid, "role": "member"})

    for i in range(len(para_ids) - 1):
        eid = f"precedes:{para_ids[i]}__{para_ids[i+1]}"
        incidences.append({"edge": eid, "node": para_ids[i], "role": "source"})
        incidences.append({"edge": eid, "node": para_ids[i+1], "role": "target"})

    return {
        "metadata": {
            "description": "Structural extraction (algorithmic, no AI)",
            "extractor": "extraction_service.py / algorithmic",
            **({"source_file": source_filename} if source_filename else {}),
        },
        "nodes": nodes,
        "edges": edges,
        "incidences": incidences,
    }


@app.post("/extract", response_model=ExtractionResponse)
async def extract(req: ExtractionRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Empty text provided")

    if req.backend not in ("algorithmic", "ollama", "anthropic"):
        raise HTTPException(status_code=400, detail=f"Unknown backend: {req.backend}")

    if req.backend != "algorithmic" and not BACKENDS_AVAILABLE.get(req.backend):
        raise HTTPException(
            status_code=503,
            detail=f"Backend '{req.backend}' not available. "
                   f"Available: {[k for k, v in BACKENDS_AVAILABLE.items() if v]}"
        )

    validation_errors: list[str] = []

    if req.backend == "algorithmic":
        hypergraph = _extract_algorithmic(req.text, req.source_filename)
        anchored = len([n for n in hypergraph["nodes"]
                       if "source_line" in n.get("attrs", {})])

    elif req.backend == "ollama":
        from text_to_hypergraph_via_ollama import extract as ollama_extract, get_ollama_url
        model = req.model or "mistral-nemo"
        try:
            parsed, _meta = ollama_extract(get_ollama_url(), req.text, model=model)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ollama extraction failed: {e}")
        validation_errors = validate_instagraph(parsed)
        anchored = anchor_to_source(parsed, req.text)
        # Convert instagraph → hypergraph format inline
        # (For now return instagraph; full pipeline conversion can be added)
        hypergraph = parsed

    elif req.backend == "anthropic":
        from text_to_hypergraph_via_llm import extract as claude_extract
        model = req.model or "claude-sonnet-4-6"
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        try:
            parsed, _meta = claude_extract(client, req.text, model=model)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Anthropic extraction failed: {e}")
        validation_errors = validate_instagraph(parsed)
        anchored = anchor_to_source(parsed, req.text)
        hypergraph = parsed

    return ExtractionResponse(
        hypergraph=hypergraph,
        backend_used=req.backend,
        anchored_count=anchored,
        validation_errors=validation_errors[:20],
    )


if __name__ == "__main__":
    print("Starting i2t extraction service on http://localhost:8420")
    print(f"Available backends: {[k for k, v in BACKENDS_AVAILABLE.items() if v]}")
    uvicorn.run(app, host="0.0.0.0", port=8420)
