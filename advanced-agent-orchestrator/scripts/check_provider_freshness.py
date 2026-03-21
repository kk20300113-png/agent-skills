#!/usr/bin/env python3
"""Check official provider pages and optionally update approved model defaults."""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Dict, List, Tuple


USER_AGENT = "advanced-agent-orchestrator/1.0"


def fetch_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="ignore")


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def version_tuple(value: str) -> Tuple[int, ...]:
    parts: List[int] = []
    for token in re.findall(r"\d+(?:\.\d+)?", value):
        if "." in token:
            major, minor = token.split(".", 1)
            parts.extend([int(major), int(minor)])
        else:
            parts.append(int(token))
    return tuple(parts) if parts else (0,)


def best_match(candidates: List[str], *, exclude: Tuple[str, ...] = ()) -> str:
    unique = []
    seen = set()
    for item in candidates:
        lowered = item.lower()
        if any(flag in lowered for flag in exclude):
            continue
        if item not in seen:
            unique.append(item)
            seen.add(item)
    if not unique:
        raise ValueError("No matching candidates found.")
    return sorted(unique, key=version_tuple, reverse=True)[0]


def extract_anthropic(pages: Dict[str, str]) -> Dict[str, str]:
    config_page = pages["https://docs.anthropic.com/en/docs/claude-code/model-config"]
    models_page = pages["https://docs.anthropic.com/en/docs/about-claude/models/all-models"]

    label_match = re.search(r"opus`?\s*\|\s*Uses the most capable Opus model \(currently Opus ([0-9.]+)\)", config_page, re.I)
    if not label_match:
        label_match = re.search(r"currently Opus ([0-9.]+)", config_page, re.I)
    version = label_match.group(1) if label_match else "4.1"

    model_id_match = re.search(r"(claude-opus-[0-9-]+)\s*\|\s*`claude-opus-[0-9-]+-\d{8}`", models_page, re.I)
    if not model_id_match:
        model_id_match = re.search(r"(claude-opus-[0-9-]+)", models_page, re.I)
    model_id = model_id_match.group(1) if model_id_match else f"claude-opus-{version.replace('.', '-')}"

    return {
        "approved_alias": "opus",
        "approved_label": f"Claude Opus {version}",
        "approved_model_id": model_id,
        "why": "Anthropic's Claude Code alias table states that `opus` tracks the current Opus model for complex reasoning.",
    }


def extract_google(pages: Dict[str, str]) -> Dict[str, str]:
    models_page = pages["https://ai.google.dev/models/gemini"]
    changelog_page = pages["https://ai.google.dev/gemini-api/docs/changelog"]

    candidates = re.findall(r"gemini-\d+(?:\.\d+)?-pro(?:-(?!image)[a-z0-9]+)*", models_page, re.I)
    candidates += re.findall(r"gemini-\d+(?:\.\d+)?-pro(?:-(?!image)[a-z0-9]+)*", changelog_page, re.I)
    model_id = best_match([candidate.lower() for candidate in candidates], exclude=("image",))

    label_match = re.search(r"Gemini\s+([0-9.]+)\s+Pro(?:\s+Preview)?", models_page, re.I)
    if not label_match:
        label_match = re.search(r"Gemini\s+([0-9.]+)\s+Pro(?:\s+Preview)?", changelog_page, re.I)
    version = label_match.group(1) if label_match else re.search(r"gemini-([0-9.]+)-pro", model_id, re.I).group(1)
    is_preview = "preview" in model_id
    suffix = " Preview" if is_preview else ""

    return {
        "approved_alias": model_id,
        "approved_label": f"Gemini {version} Pro{suffix}",
        "approved_model_id": model_id,
        "why": "Google's Gemini models page and changelog identify the latest Pro-series model code exposed for reasoning-heavy API use.",
    }


def extract_moonshot(pages: Dict[str, str]) -> Dict[str, str]:
    newsletter = pages["https://platform.moonshot.ai/blog/posts/Kimi_API_Newsletter"]
    changelog = pages["https://platform.moonshot.ai/blog/posts/changelog"]
    _docs_page = pages["https://platform.moonshot.ai/docs/guide/use-kimi-k2-thinking-model"]

    candidates = re.findall(r"kimi-k2-thinking(?:-turbo)?", newsletter, re.I)
    candidates += re.findall(r"kimi-k2(?:-[0-9]{4}-preview|-thinking(?:-turbo)?|-turbo-preview)?", changelog, re.I)
    model_id = "kimi-k2-thinking" if "kimi-k2-thinking" in [item.lower() for item in candidates] else best_match([item.lower() for item in candidates])

    base_url = "https://api.moonshot.ai/v1"

    return {
        "approved_alias": model_id,
        "approved_label": "Kimi K2 Thinking" if model_id == "kimi-k2-thinking" else model_id,
        "approved_model_id": model_id,
        "base_url": base_url,
        "why": "Moonshot's official newsletter and release log identify the current Kimi K2 reasoning model line, and the quick-start guide documents the OpenAI-compatible base URL.",
    }


def extract_openai(pages: Dict[str, str]) -> Dict[str, str]:
    model_page = pages["https://platform.openai.com/docs/models/gpt-5.2-codex"]
    models_page = pages["https://platform.openai.com/docs/models"]

    label_match = re.search(r"GPT-([0-9.]+)-Codex", model_page, re.I)
    if not label_match:
        label_match = re.search(r"GPT-([0-9.]+)-Codex", models_page, re.I)
    version = label_match.group(1) if label_match else "5.2"

    model_id_match = re.search(r"(gpt-[0-9.]+-codex)", model_page, re.I)
    if not model_id_match:
        model_id_match = re.search(r"(gpt-[0-9.]+-codex)", models_page, re.I)
    model_id = model_id_match.group(1).lower() if model_id_match else f"gpt-{version}-codex"

    return {
        "approved_alias": model_id,
        "approved_label": f"GPT-{version}-Codex",
        "approved_model_id": model_id,
        "why": "OpenAI's official model pages identify the current Codex-aligned coding model family for agentic coding tasks.",
    }


PROVIDERS = {
    "anthropic": {
        "urls": [
            "https://docs.anthropic.com/en/docs/claude-code/model-config",
            "https://docs.anthropic.com/en/docs/about-claude/models/all-models",
        ],
        "extractor": extract_anthropic,
    },
    "google": {
        "urls": [
            "https://ai.google.dev/models/gemini",
            "https://ai.google.dev/gemini-api/docs/changelog",
        ],
        "extractor": extract_google,
    },
    "moonshot": {
        "urls": [
            "https://platform.moonshot.ai/blog/posts/Kimi_API_Newsletter",
            "https://platform.moonshot.ai/blog/posts/changelog",
            "https://platform.moonshot.ai/docs/guide/use-kimi-k2-thinking-model",
        ],
        "extractor": extract_moonshot,
    },
    "openai": {
        "urls": [
            "https://platform.openai.com/docs/models/gpt-5.2-codex",
            "https://platform.openai.com/docs/models",
        ],
        "extractor": extract_openai,
    },
}


def load_state(path: Path) -> Dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, data: Dict[str, object]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def detect(provider_name: str) -> Dict[str, str]:
    spec = PROVIDERS[provider_name]
    pages = {url: fetch_text(url) for url in spec["urls"]}
    return spec["extractor"](pages)


def apply_detected(state: Dict[str, object], detected: Dict[str, Dict[str, str]], timestamp: str) -> Dict[str, object]:
    updated = copy.deepcopy(state)
    updated["last_checked_at"] = timestamp

    workflow = updated.get("workflow", {})
    providers = updated.get("providers", {})

    for provider_name, result in detected.items():
        provider = providers[provider_name]
        provider["approved_alias"] = result["approved_alias"]
        provider["approved_label"] = result["approved_label"]
        provider["approved_model_id"] = result["approved_model_id"]
        provider["last_checked_at"] = timestamp
        provider["reason"] = result["why"]
        if "base_url" in result:
            provider["base_url"] = result["base_url"]

    workflow["planner"]["model"] = providers["anthropic"]["approved_alias"]
    workflow["planner"]["label"] = providers["anthropic"]["approved_label"]
    workflow["challenger"]["model"] = providers["anthropic"]["approved_alias"]
    workflow["challenger"]["label"] = providers["anthropic"]["approved_label"]
    workflow["plan_reviewer"]["model"] = providers["google"]["approved_model_id"]
    workflow["plan_reviewer"]["label"] = providers["google"]["approved_label"]
    workflow["executor"]["model"] = providers["google"]["approved_model_id"]
    workflow["executor"]["label"] = providers["google"]["approved_label"]
    workflow["alternate_executor"]["model"] = providers["moonshot"]["approved_model_id"]
    workflow["alternate_executor"]["label"] = providers["moonshot"]["approved_label"]
    return updated


def compare_state(state: Dict[str, object], detected: Dict[str, Dict[str, str]]) -> List[Dict[str, str]]:
    drifts = []
    providers = state.get("providers", {})
    for provider_name, result in detected.items():
        current = providers[provider_name]
        changes = []
        for key in ("approved_alias", "approved_label", "approved_model_id"):
            if current.get(key) != result.get(key):
                changes.append(key)
        if current.get("base_url") != result.get("base_url") and "base_url" in result:
            changes.append("base_url")
        drifts.append(
            {
                "provider": provider_name,
                "changed": "yes" if changes else "no",
                "fields": ", ".join(changes) if changes else "",
                "current_alias": str(current.get("approved_alias", "")),
                "detected_alias": result.get("approved_alias", ""),
                "current_label": str(current.get("approved_label", "")),
                "detected_label": result.get("approved_label", ""),
                "current_model_id": str(current.get("approved_model_id", "")),
                "detected_model_id": result.get("approved_model_id", ""),
                "current_base_url": str(current.get("base_url", "")),
                "detected_base_url": result.get("base_url", ""),
                "why": result.get("why", ""),
            }
        )
    return drifts


def print_report(drifts: List[Dict[str, str]], *, approve: bool) -> None:
    print("Provider freshness check")
    print("=======================")
    drift_found = False
    for item in drifts:
        print(f"- {item['provider']}:")
        print(f"  current:  {item['current_label']} [{item['current_alias'] or item['current_model_id']}]")
        print(f"  detected: {item['detected_label']} [{item['detected_alias'] or item['detected_model_id']}]")
        if item["changed"] == "yes":
            drift_found = True
            print(f"  drift:    yes ({item['fields']})")
            if item["current_base_url"] or item["detected_base_url"]:
                print(f"  base_url: current={item['current_base_url']} detected={item['detected_base_url']}")
            print(f"  why:      {norm(item['why'])}")
        else:
            print("  drift:    no")
    print()
    if drift_found and not approve:
        print("Action required: review the drift above and rerun with --approve after user approval.")
    elif drift_found and approve:
        print("Approved update: state files will be rewritten with the detected defaults.")
    else:
        print("No drift detected.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", required=True, help="Path to the global provider-defaults.json file.")
    parser.add_argument("--repo-state", help="Optional repo-local provider-defaults.json file to sync on approval.")
    parser.add_argument("--approve", action="store_true", help="Rewrite the state files using the detected defaults.")
    args = parser.parse_args()

    state_path = Path(args.state)
    state = load_state(state_path)

    detected: Dict[str, Dict[str, str]] = {}
    failures = {}
    for provider_name in PROVIDERS:
        try:
            detected[provider_name] = detect(provider_name)
        except Exception as exc:  # noqa: BLE001
            failures[provider_name] = str(exc)

    if failures:
        print("Provider freshness check failed.", file=sys.stderr)
        for provider_name, message in failures.items():
            print(f"- {provider_name}: {message}", file=sys.stderr)
        return 2

    drifts = compare_state(state, detected)
    print_report(drifts, approve=args.approve)

    if not args.approve:
        return 1 if any(item["changed"] == "yes" for item in drifts) else 0

    timestamp = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    updated = apply_detected(state, detected, timestamp)
    save_state(state_path, updated)

    if args.repo_state:
        repo_path = Path(args.repo_state)
        repo_state = load_state(repo_path)
        updated_repo = apply_detected(repo_state, detected, timestamp)
        save_state(repo_path, updated_repo)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
