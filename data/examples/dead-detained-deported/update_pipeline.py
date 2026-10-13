#!/usr/bin/env python3
"""Update system for the dead-detained-deported hypergraph.

Commands:
  status                 show every registered source and its staleness
  fetch <source-id>      refresh one source's layer file. REQUIRES --network:
                         this script never touches the internet unless you
                         pass the flag explicitly.
  rebuild                regenerate the base layer, merge all layers into the
                         canonical file, validate, and emit the dyadic
                         projection. No network involved.

Update model (why information is never lost):
  snapshots/<source>/<timestamp>.<ext>   append-only raw bytes, saved before parsing
  layers/ddd.source-*.json               one canonical hypergraph per source
  layers/ddd.base-research-doc.json      the hand-extracted research-document layer
  dead-detained-deported.hypergraph.topothink.json   merge of all layers (by node ID)

A refresh rewrites ONE layer and re-merges. Deterministic IDs (ddd_lib) make
the same fact land on the same node every time, so merges dedupe; genuine
disagreements between sources are preserved as i2t:conflicts entries on the
merged entity rather than silently resolved.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

from ddd_lib import (
    CANONICAL_PATH,
    EXAMPLE_DIR,
    LAYERS_DIR,
    REGISTRY_PATH,
    REPO_ROOT,
    SNAPSHOTS_DIR,
    GraphBuilder,
    add_death,
    utcnow_iso,
)

USER_AGENT = "ddd-hypergraph-updater/0.1 (research/transparency; halapenyoharry@gmail.com)"


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text())


def save_registry(reg: dict) -> None:
    REGISTRY_PATH.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n")


def cmd_status() -> None:
    reg = load_registry()
    now = datetime.datetime.now(datetime.timezone.utc)
    print(f"{'source':46} {'fetcher':22} {'cadence':9} {'last_checked':26} state")
    for s in reg["sources"]:
        cadence = s.get("cadence_days")
        last = s.get("last_checked")
        if s.get("fetcher") is None:
            state = "manual (no fetcher yet)"
        elif last is None:
            state = "NEVER FETCHED"
        else:
            age = (now - datetime.datetime.fromisoformat(last)).days
            state = f"stale ({age}d old)" if cadence and age > cadence else f"fresh ({age}d old)"
        print(f"{s['id']:46} {str(s.get('fetcher')):22} {str(cadence):9} {str(last):26} {state}")


def snapshot(source_id: str, content: bytes, ext: str) -> Path:
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = SNAPSHOTS_DIR / source_id.split(":", 1)[1] / f"{stamp}.{ext}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    print(f"snapshot saved: {path.relative_to(EXAMPLE_DIR)} ({len(content)} bytes)")
    return path


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


# ---------------------------------------------------------------------------
# Fetchers. Each takes the registry entry, returns the layer path it wrote.
# Snapshot FIRST, parse second; a parser failure still leaves the raw bytes.
# ---------------------------------------------------------------------------

def fetch_ice_death_reporting(entry: dict) -> Path:
    """Scrape the ICE Detainee Death Reporting index into a source layer.

    The page's exact markup is not guaranteed; this parser is deliberately
    tolerant (looks for name-like strings adjacent to parseable dates in
    table rows or list items) and is expected to be tightened against a real
    snapshot on first run. Everything it cannot parse remains available in
    the snapshot for a better parser later.
    """
    raw = http_get(entry["url"])
    snap = snapshot(entry["id"], raw, "html")
    html = raw.decode("utf-8", errors="replace")

    # strip tags to text lines, keeping table-cell boundaries as separators
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    text = re.sub(r"</(td|th|tr|li|p|div)>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]

    date_pat = re.compile(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)"
        r"\s+(\d{1,2}),\s+(\d{4})"
    )
    months = {m: i + 1 for i, m in enumerate(
        ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"])}
    # "Last, First" or "Last, First Middle" immediately before/on a dated line
    name_pat = re.compile(r"^([A-Z][\w'\-]+(?: [A-Z][\w'\-]+)*), ([A-Z][\w'\-]+(?: [A-Z][\w'\-.]+)*)$")

    records: list[tuple[str, str]] = []
    prev = ""
    for ln in lines:
        m = date_pat.search(ln)
        if m:
            date_iso = f"{int(m.group(3)):04d}-{months[m.group(1)]:02d}-{int(m.group(2)):02d}"
            candidate = ln[: m.start()].strip(" -–—,") or prev
            nm = name_pat.match(candidate)
            if nm:
                records.append((candidate, date_iso))
        prev = ln

    g = GraphBuilder(
        "DDD source layer: ICE Detainee Death Reporting",
        {
            "i2t:relation_to_canonical": "predicate-layer",
            "source_url": entry["url"],
            "snapshot": str(snap.relative_to(EXAMPLE_DIR)),
            "extracted_at": utcnow_iso(),
            "extraction_method": "tolerant html scrape (update_pipeline.fetch_ice_death_reporting)",
            "records_parsed": len(records),
        },
    )
    g.node("source:ice-death-reporting",
           **{"schema:name": "ICE Detainee Death Reporting index", "schema:url": entry["url"],
              "ddd:node_type": "source", "ddd:last_fetched": utcnow_iso()})
    g.node("registry:ice-death-ledger",
           **{"schema:name": "ICE Detainee Death Reporting ledger", "ddd:node_type": "registry"})
    events = []
    for name, date_iso in records:
        events.append(add_death(
            g, name, date_iso,
            ledger_status="official",
            sources=["source:ice-death-reporting"],
            evidence=f"Listed on ICE Detainee Death Reporting index as of {utcnow_iso()[:10]}: {name}, {date_iso}.",
        ))
    if events:
        g.edge("edge:ledger-membership", predicate="documents_death", category="containment",
               members=[("registry:ice-death-ledger", "registry")] + [(e, "documented_death") for e in events],
               sources=["source:ice-death-reporting"])

    layer = EXAMPLE_DIR / entry["layer"]
    g.write(layer)
    if not records:
        print("WARNING: 0 records parsed — page markup likely changed; "
              "inspect the snapshot and tighten the parser. Raw data is preserved.")
    return layer


FETCHERS = {
    "ice_death_reporting": fetch_ice_death_reporting,
}


def cmd_fetch(source_id: str, network: bool) -> None:
    if not network:
        raise SystemExit(
            "fetch requires --network. This pipeline never calls the internet "
            "unless explicitly told to (house rule)."
        )
    reg = load_registry()
    entry = next((s for s in reg["sources"] if s["id"] == source_id), None)
    if entry is None:
        raise SystemExit(f"unknown source id: {source_id}")
    fetcher = FETCHERS.get(entry.get("fetcher") or "")
    if fetcher is None:
        raise SystemExit(
            f"{source_id} has no implemented fetcher yet "
            f"(access: {entry.get('access')}). See its registry notes for what a fetcher should emit."
        )
    fetcher(entry)
    entry["last_checked"] = utcnow_iso()
    save_registry(reg)
    print(f"{source_id} refreshed; run `python3 update_pipeline.py rebuild` to re-merge.")


def cmd_rebuild() -> None:
    py = sys.executable
    # 1. regenerate the base layer from the research document
    subprocess.run([py, str(EXAMPLE_DIR / "build_initial_hypergraph.py")], check=True, cwd=EXAMPLE_DIR)
    # 2. merge every layer into the canonical file (base first = priority on conflicts)
    layers = sorted(LAYERS_DIR.glob("ddd.*.hypergraph.topothink.json"))
    base = LAYERS_DIR / "ddd.base-research-doc.hypergraph.topothink.json"
    ordered = [base] + [p for p in layers if p != base]
    subprocess.run(
        [py, str(REPO_ROOT / "adapters/merge_hypergraphs.py"),
         *map(str, ordered), "-o", str(CANONICAL_PATH),
         "--title", "Dead, Detained, Deported — canonical hypergraph"],
        check=True,
    )
    # 3. dyadic projection for viewers (Exoskeleton / JVV / post-pipe)
    subprocess.run(
        [py, str(REPO_ROOT / "adapters/hypergraph_to_dyadic.py"), str(CANONICAL_PATH)],
        check=True,
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    f = sub.add_parser("fetch")
    f.add_argument("source_id")
    f.add_argument("--network", action="store_true",
                   help="explicit opt-in to internet access for this fetch")
    sub.add_parser("rebuild")
    args = ap.parse_args()

    if args.cmd == "status":
        cmd_status()
    elif args.cmd == "fetch":
        cmd_fetch(args.source_id, args.network)
    elif args.cmd == "rebuild":
        cmd_rebuild()


if __name__ == "__main__":
    main()
