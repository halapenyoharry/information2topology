"""BYO-AI Client Contract:
Supports:
1. OpenRouter (https://openrouter.ai/api/v1)
2. Gemini (OpenAI-compatible endpoint or native)
3. Local OpenAI-compatible (vLLM / Ollama)
4. BYO-Commandline-AI: executes arbitrary shell command (e.g., local script or custom binary) via stdin/stdout
"""
from __future__ import annotations
import json
import os
import subprocess
import urllib.request
import urllib.error
from typing import Any


class ByoAiClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        cli_command: str | None = None,
    ):
        self.api_key = (
            api_key
            or os.environ.get("OPENROUTER_KEY_INFO2TOPO")
            or os.environ.get("OPENROUTER_API_KEY")
            or os.environ.get("GEMINI_API_KEY")
        )
        self.base_url = base_url or os.environ.get("AI_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = model or os.environ.get("AI_MODEL", "google/gemini-2.5-flash")
        self.cli_command = cli_command or os.environ.get("AI_CLI_COMMAND")

    def call_ai(self, system_prompt: str, user_text: str) -> str:
        """Dispatches to either a BYO-Commandline tool or an HTTP endpoint."""
        # 1. BYO-Commandline path (pipes prompt + text into stdin)
        if self.cli_command:
            return self._call_cli(system_prompt, user_text)

        # 2. HTTP API path (OpenRouter / Gemini / OpenAI-compatible)
        return self._call_http(system_prompt, user_text)

    def _call_cli(self, system_prompt: str, user_text: str) -> str:
        payload = {
            "system_prompt": system_prompt,
            "user_text": user_text,
            "model": self.model
        }
        process = subprocess.Popen(
            self.cli_command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=json.dumps(payload))
        if process.returncode != 0:
            raise RuntimeError(f"BYO-Commandline error (exit {process.returncode}): {stderr.strip()}")
        return stdout.strip()

    def _call_http(self, system_prompt: str, user_text: str) -> str:
        if not self.api_key:
            raise ValueError(
                "No API Key provided. Set OPENROUTER_API_KEY, GEMINI_API_KEY, or pass --api-key / --cli-command"
            )

        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/halapenyoharry/information2topology",
            "X-Title": "i2t-topology-engine"
        }

        # Request schema
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.0
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                resp_json = json.loads(resp.read().decode("utf-8"))
                choices = resp_json.get("choices", [])
                if not choices:
                    raise RuntimeError(f"No choices returned from model API: {resp_json}")
                return choices[0]["message"]["content"]
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP Error {e.code} from {url}: {err_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Network Connection Error to {url}: {e.reason}")
