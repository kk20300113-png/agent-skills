#!/usr/bin/env python3
"""
API Executor for Advanced Agent Orchestrator v3

Programmatically calls AI provider APIs for each workflow phase.
Uses only Python stdlib (urllib) — no pip installs required.

USAGE:
    python api_executor.py --provider moonshot --phase planner --task "Build a REST API"
    python api_executor.py --provider anthropic --phase executor --blueprint blueprint.md
    python api_executor.py --provider google --phase reviewer --task "..." --output review.md
    python api_executor.py --list-providers

ENVIRONMENT VARIABLES (set one per provider you use — never hardcode keys):
    ANTHROPIC_API_KEY   — Claude Opus (Anthropic)
    GOOGLE_API_KEY      — Gemini Pro  (Google)
    MOONSHOT_API_KEY    — Kimi K2     (Moonshot AI)
    OPENAI_API_KEY      — GPT / Codex (OpenAI)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
PROVIDER_DEFAULTS = ROOT / "references" / "provider-defaults.json"
PROMPTS_DIR = ROOT / "prompts"

# Maps phase names → prompt files
PHASE_TO_PROMPT: dict[str, str] = {
    "planner":       "planner-create-plan.md",
    "plan_reviewer": "plan-reviewer-critique.md",
    "executor":      "executor-implement-plan.md",
    "reviewer":      "reviewer-primary-critique.md",
    "reviewer2":     "reviewer-secondary-critique.md",
    "state_export":  "state-export-blueprint.md",
}

# Maps provider name → environment variable holding the API key
ENV_KEYS: dict[str, str] = {
    "anthropic": "ANTHROPIC_API_KEY",
    "google":    "GOOGLE_API_KEY",
    "moonshot":  "MOONSHOT_API_KEY",
    "openai":    "OPENAI_API_KEY",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_provider_defaults() -> dict:
    with open(PROVIDER_DEFAULTS, encoding="utf-8") as fh:
        return json.load(fh)


def _load_prompt(phase: str) -> str:
    prompt_file = PROMPTS_DIR / PHASE_TO_PROMPT[phase]
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    return prompt_file.read_text(encoding="utf-8")


def _http_post(url: str, payload: dict, headers: dict) -> dict:
    """Send a JSON POST request and return the parsed response dict."""
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {err_body}") from exc


# ---------------------------------------------------------------------------
# Provider call implementations
# ---------------------------------------------------------------------------

def _call_openai_compatible(
    base_url: str,
    api_key: str,
    model_id: str,
    system_prompt: str,
    user_message: str,
) -> str:
    """Reused for any OpenAI-compatible endpoint (OpenAI, Moonshot/Kimi, etc.)."""
    url = base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        "temperature": 0.7,
    }
    data = _http_post(url, payload, headers)
    return data["choices"][0]["message"]["content"]


def _call_anthropic(model_id: str, api_key: str, system_prompt: str, user_message: str) -> str:
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    payload = {
        "model": model_id,
        "max_tokens": 8192,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_message}],
    }
    data = _http_post(url, payload, headers)
    return data["content"][0]["text"]


def _call_google(model_id: str, api_key: str, system_prompt: str, user_message: str) -> str:
    # Google's REST endpoint does not use Bearer auth — key goes in the URL query param
    url = (
        f"https://generativelanguage.googleapis.com/v1beta"
        f"/models/{model_id}:generateContent?key={api_key}"
    )
    headers = {"Content-Type": "application/json"}
    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"parts": [{"text": user_message}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 8192,
        },
    }
    data = _http_post(url, payload, headers)
    return data["candidates"][0]["content"]["parts"][0]["text"]


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

def execute_phase(provider: str, phase: str, content: str) -> str:
    """
    Calls the specified provider's API for the given workflow phase.

    Args:
        provider: One of 'anthropic', 'google', 'moonshot', 'openai'.
        phase:    One of the keys in PHASE_TO_PROMPT.
        content:  Task description (planner) or blueprint/code (later phases).

    Returns:
        The model's full text response.
    """
    if provider not in ENV_KEYS:
        raise ValueError(
            f"Unknown provider '{provider}'. "
            f"Valid options: {list(ENV_KEYS.keys())}"
        )
    if phase not in PHASE_TO_PROMPT:
        raise ValueError(
            f"Unknown phase '{phase}'. "
            f"Valid options: {list(PHASE_TO_PROMPT.keys())}"
        )

    defaults = _load_provider_defaults()
    prov_cfg = defaults["providers"].get(provider)
    if prov_cfg is None:
        raise KeyError(f"Provider '{provider}' not found in provider-defaults.json")

    model_id = prov_cfg["approved_model_id"]
    api_key_env = ENV_KEYS[provider]
    api_key = os.environ.get(api_key_env, "")
    if not api_key:
        raise EnvironmentError(
            f"No API key found. Set the {api_key_env} environment variable.\n"
            f"Example (Windows PowerShell):  $env:{api_key_env} = 'sk-...'"
        )

    system_prompt = _load_prompt(phase)

    print(f"\n[api_executor] Provider : {provider} ({prov_cfg['approved_label']})")
    print(f"[api_executor] Model    : {model_id}")
    print(f"[api_executor] Phase    : {phase}")
    print(f"[api_executor] Input    : {len(content)} chars")
    print("[api_executor] Calling API...\n")

    if provider == "anthropic":
        return _call_anthropic(model_id, api_key, system_prompt, content)
    elif provider == "google":
        return _call_google(model_id, api_key, system_prompt, content)
    elif provider == "moonshot":
        base_url = prov_cfg.get("base_url", "https://api.moonshot.ai/v1")
        return _call_openai_compatible(base_url, api_key, model_id, system_prompt, content)
    elif provider == "openai":
        return _call_openai_compatible("https://api.openai.com/v1", api_key, model_id, system_prompt, content)

    raise AssertionError("Unreachable")  # all branches above are exhaustive


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Programmatic API executor for Advanced Agent Orchestrator phases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Plan a task using Kimi
  python api_executor.py --provider moonshot --phase planner --task "Build a REST API"

  # Execute using Kimi with a saved blueprint
  python api_executor.py --provider moonshot --phase executor --blueprint blueprint.md

  # Review output and save to file
  python api_executor.py --provider anthropic --phase reviewer --blueprint output.md --output review.md

  # Check which API keys are configured
  python api_executor.py --list-providers
""",
    )
    parser.add_argument(
        "--provider",
        choices=list(ENV_KEYS.keys()),
        help="AI provider to use",
    )
    parser.add_argument(
        "--phase",
        choices=list(PHASE_TO_PROMPT.keys()),
        help="Workflow phase to execute",
    )
    parser.add_argument(
        "--task",
        type=str,
        default="",
        help="Task description string (used for planner / state_export phase)",
    )
    parser.add_argument(
        "--blueprint",
        type=Path,
        default=None,
        help="Path to a .md blueprint/output file to pass as input",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Write the model response to this file (default: print to stdout)",
    )
    parser.add_argument(
        "--list-providers",
        action="store_true",
        help="Show all configured providers and whether their API keys are set, then exit",
    )
    return parser


def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    if args.list_providers:
        defaults = _load_provider_defaults()
        print("\nConfigured providers (from provider-defaults.json):\n")
        for name, cfg in defaults["providers"].items():
            key_var = ENV_KEYS.get(name, "UNKNOWN_API_KEY")
            key_status = "✓ set" if os.environ.get(key_var) else "✗ not set"
            print(
                f"  {name:<12}  {cfg['approved_label']:<30}  "
                f"[{key_var}: {key_status}]"
            )
        print()
        return

    if not args.provider or not args.phase:
        parser.print_help()
        sys.exit(1)

    # Determine input content
    if args.blueprint:
        bp = Path(args.blueprint)
        if not bp.exists():
            print(f"[api_executor] ERROR: Blueprint file not found: {bp}", file=sys.stderr)
            sys.exit(1)
        content = bp.read_text(encoding="utf-8")
    elif args.task:
        content = args.task
    else:
        print(
            "[api_executor] No --task or --blueprint provided. "
            "Reading from stdin (Ctrl+Z then Enter on Windows to finish)..."
        )
        content = sys.stdin.read()

    try:
        response = execute_phase(args.provider, args.phase, content)
    except (EnvironmentError, ValueError, KeyError, RuntimeError) as exc:
        print(f"[api_executor] ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        out = Path(args.output)
        out.write_text(response, encoding="utf-8")
        print(f"[api_executor] Response written to: {out}")
    else:
        print("=" * 70)
        print(response)
        print("=" * 70)


if __name__ == "__main__":
    main()
