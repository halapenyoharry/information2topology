import sys
import json
import os
from pathlib import Path
sys.path.insert(0, '/Users/harold/Projects/information2topology/adapters')
from text_to_hypergraph_via_ollama import extract as ollama_extract, get_ollama_url
from extraction_common import validate_instagraph, anchor_to_source
from instagraph_to_hypergraph import adapt
from hypergraph_to_dyadic import normalize

os.chdir('/Users/harold/Projects/information2topology')

# 1. extract text
with open('/Users/harold/Knowledge/full_texts/Valmikis_Ramayana.txt', 'r') as f:
    lines = f.readlines()
canto1 = "".join(lines[664:1036]).strip()

print(f"Extracted {len(canto1)} characters.")

out_dir = Path("test_output/ramayana_v3")
out_dir.mkdir(parents=True, exist_ok=True)
source_file = out_dir / "canto1.canonical.txt"
with open(source_file, "w") as f:
    f.write(canto1)

# 2. Extract with Ollama via CLI (using --chunked)
import subprocess

print("Running chunked extraction via Ollama...")
cmd = [
    sys.executable,
    "adapters/text_to_hypergraph_via_ollama.py",
    str(source_file),
    "-o", str(out_dir / "canto1.instagraph.json"),
    "--model", "qwen2.5-coder:32b-instruct-q4_K_M",
    "--chunked"
]
subprocess.run(cmd, check=True)

# 3. Convert to Hypergraph
print("Converting to TopoThink hypergraph...")
cmd = [
    sys.executable,
    "adapters/instagraph_to_hypergraph.py",
    str(out_dir / "canto1.instagraph.json")
]
subprocess.run(cmd, check=True)

# 4. Convert to Dyadic (JSON projection for viewing)
print("Converting to Dyadic format...")
cmd = [
    sys.executable,
    "adapters/hypergraph_to_dyadic.py",
    str(out_dir / "canto1.hypergraph.topothink.json")
]
subprocess.run(cmd, check=True)

print("Done. All artifacts generated in test_output/ramayana_v3/")
