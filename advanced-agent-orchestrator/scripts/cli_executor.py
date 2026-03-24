#!/usr/bin/env python3
"""
CLI Executor for Advanced Agent Orchestrator v3

Invokes AI providers that are accessible via local CLI tools rather than
direct HTTP API calls.  Currently supports:

  gemini_cli  — Google's Gemini CLI  (npm: @google/gemini-cli)

USAGE:
    python cli_executor.py --provider gemini_cli --phase planner --task "Build a REST API"
    python cli_executor.py --provider gemini_cli --phase executor --blueprint blueprint.md
    python cli_executor.py --provider gemini_cli --phase reviewer --blueprint output.md --output review.md
    python cli_executor.py --check                     # verify CLI tools are installed

SETUP (Gemini CLI - one-time):
    npm install -g @google/gemini-cli
    gemini auth login          # browser OAuth — no API key file required
    gemini --version           # confirms install
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
PROVIDER_DEFAULTS = ROOT / "references" / "provider-defaults.json"
PROMPTS_DIR = ROOT / "prompts"

PHASE_TO_PROMPT: dict[str, str] = {
    "planner":       "planner-create-plan.md",
    "plan_reviewer": "plan-reviewer-critique.md",
    "executor":      "executor-implement-plan.md",
    "reviewer":      "reviewer-primary-critique.md",
    "reviewer2":     "reviewer-secondary-critique.md",
    "state_export":  "state-export-blueprint.md",
}

# Supported CLI providers and their executable names
CLI_PROVIDERS: dict[str, str] = {
    "gemini_cli": "gemini",
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


def _check_cli(executable: str) -> bool:
    return shutil.which(executable) is not None


# ---------------------------------------------------------------------------
# Gemini CLI invocation
# ---------------------------------------------------------------------------

def _call_gemini_cli(model_id: str, system_prompt: str, user_message: str) -> str:
    """
    Invokes the Gemini CLI tool with a combined system + user prompt via stdin.

    The Gemini CLI reads the prompt text from stdin when you pass '-' or pipe into it.
    We write a temp file to avoid shell quoting issues with long prompts.
    """
    if not _check_cli("gemini"):
        raise EnvironmentError(
            "Gemini CLI not found on PATH.\n"
            "Install: npm install -g @google/gemini-cli\n"
            "Auth:    gemini auth login"
        )

    # Combine system prompt + user message into one input block
    combined = (
        "=== SYSTEM / ROLE INSTRUCTIONS ===\n"
        f"{system_prompt}\n\n"
        "=== USER INPUT ===\n"
        f"{user_message}"
    )

    # Write to a temp file so the CLI can read it cleanly
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(combined)
        tmp_path = tmp.name

    try:
        cmd = ["gemini", "--model", model_id, "--file", tmp_path]
        print(f"[cli_executor] Running: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5-minute hard limit
        )

        if result.returncode != 0:
            err = result.stderr.strip() or "(no stderr)"
            raise RuntimeError(
                f"Gemini CLI exited with code {result.returncode}.\n"
                f"stderr: {err}"
            )

        output = result.stdout.strip()
        if not output:
            raise RuntimeError("Gemini CLI returned empty output.")

        return output

    finally:
        os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------

def execute_phase(provider: str, phase: str, content: str) -> str:
    """
    Invokes the specified CLI-based provider for the given workflow phase.

    Args:
        provider: One of the keys in CLI_PROVIDERS (e.g. 'gemini_cli').
        phase:    One of the keys in PHASE_TO_PROMPT.
        content:  Task description (planner) or blueprint / code (later phases).

    Returns:
        The model's full text response.
    """
    if provider not in CLI_PROVIDERS:
        raise ValueError(
            f"Unknown CLI provider '{provider}'. "
            f"Supported: {list(CLI_PROVIDERS.keys())}"
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
    system_prompt = _load_prompt(phase)

    print(f"\n[cli_executor] Provider : {provider} ({prov_cfg['approved_label']})")
    print(f"[cli_executor] Model    : {model_id}")
    print(f"[cli_executor] Phase    : {phase}")
    print(f"[cli_executor] Input    : {len(content)} chars\n")

    if provider == "gemini_cli":
        return _call_gemini_cli(model_id, system_prompt, content)

    raise AssertionError(f"Unhandled provider: {provider}")  # exhaustive check


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI-based phase executor for Advanced Agent Orchestrator (Gemini CLI, etc.)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Plan a task with Gemini CLI
  python cli_executor.py --provider gemini_cli --phase planner --task "Build a REST API"

  # Execute using a saved blueprint file
  python cli_executor.py --provider gemini_cli --phase executor --blueprint blueprint.md

  # Review and save output
  python cli_executor.py --provider gemini_cli --phase reviewer --blueprint code.md --output review.md

  # Check all CLI tools are installed
  python cli_executor.py --check
""",
    )
    parser.add_argument(
        "--provider",
        choices=list(CLI_PROVIDERS.keys()),
        help="CLI provider to use",
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
        help="Task description (used for planner / state_export phase)",
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
        "--check",
        action="store_true",
        help="Verify all supported CLI tools are installed, then exit",
    )
    return parser


def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    if args.check:
        print("\nCLI provider availability check:\n")
        all_ok = True
        for prov_name, exe in CLI_PROVIDERS.items():
            found = _check_cli(exe)
            status = "✓ found" if found else "✗ NOT found"
            if not found:
                all_ok = False
            defaults = _load_provider_defaults()
            cfg = defaults["providers"].get(prov_name, {})
            setup = cfg.get("setup", {})
            print(f"  {prov_name:<14}  [{exe}] {status}")
            if not found and setup:
                print(f"             Install: {setup.get('install', 'n/a')}")
                print(f"             Auth   : {setup.get('auth', 'n/a')}")
        print()
        sys.exit(0 if all_ok else 1)

    if not args.provider or not args.phase:
        parser.print_help()
        sys.exit(1)

    # Determine input content
    if args.blueprint:
        bp = Path(args.blueprint)
        if not bp.exists():
            print(f"[cli_executor] ERROR: Blueprint file not found: {bp}", file=sys.stderr)
            sys.exit(1)
        content = bp.read_text(encoding="utf-8")
    elif args.task:
        content = args.task
    else:
        print(
            "[cli_executor] No --task or --blueprint provided. "
            "Reading from stdin (Ctrl+Z then Enter on Windows to finish)..."
        )
        content = sys.stdin.read()

    try:
        response = execute_phase(args.provider, args.phase, content)
    except (EnvironmentError, ValueError, KeyError, RuntimeError) as exc:
        print(f"[cli_executor] ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        out = Path(args.output)
        out.write_text(response, encoding="utf-8")
        print(f"[cli_executor] Response written to: {out}")
    else:
        print("=" * 70)
        print(response)
        print("=" * 70)


if __name__ == "__main__":
    main()
