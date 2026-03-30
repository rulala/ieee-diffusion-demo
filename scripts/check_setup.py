#!/usr/bin/env python3
"""Lightweight local setup checker for the IEEE Diffusion Demo repo."""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import requests

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"

REQUIRED_IMPORTS: Dict[str, str] = {
    "numpy": "numpy",
    "pandas": "pandas",
    "sklearn": "scikit-learn",
    "matplotlib": "matplotlib",
    "torch": "torch",
    "tqdm": "tqdm",
    "chromadb": "chromadb",
    "langchain_community": "langchain-community",
    "langchain_text_splitters": "langchain-text-splitters",
    "langchain_chroma": "langchain-chroma",
    "gradio": "gradio",
    "dotenv": "python-dotenv",
    "ollama": "ollama",
    "firecrawl": "firecrawl-py",
}

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


def print_status(label: str, ok: bool, message: str) -> None:
    color = GREEN if ok else RED
    state = "OK" if ok else "FAIL"
    print(f"{color}[{state}]{RESET} {label}: {message}")


def print_warn(label: str, message: str) -> None:
    print(f"{YELLOW}[WARN]{RESET} {label}: {message}")


def load_env_file(path: Path) -> None:
    try:
        from dotenv import load_dotenv
    except Exception:
        return
    if path.exists():
        load_dotenv(path, override=False)


def check_imports() -> Tuple[bool, List[str]]:
    missing: List[str] = []
    for module_name, package_name in REQUIRED_IMPORTS.items():
        try:
            importlib.import_module(module_name)
        except Exception:
            missing.append(package_name)
    return (len(missing) == 0, missing)


def check_env() -> bool:
    load_env_file(ENV_PATH)
    key = os.getenv("FIRECRAWL_API_KEY", "").strip()
    if not key:
        print_status("Environment", False, "FIRECRAWL_API_KEY is not set")
        return False
    if not key.startswith("fc-"):
        print_warn("Environment", "FIRECRAWL_API_KEY is present but does not start with 'fc-'")
    print_status("Environment", True, ".env loaded and FIRECRAWL_API_KEY found")
    return True


def check_ollama() -> bool:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    llm_model = os.getenv("LLM_MODEL", "llama3")
    embed_model = os.getenv("EMBED_MODEL", "nomic-embed-text")

    try:
        resp = requests.get(f"{base_url}/api/tags", timeout=3)
        resp.raise_for_status()
        payload = resp.json()
        names = {m.get("name", "") for m in payload.get("models", [])}
    except Exception as exc:
        print_status("Ollama", False, f"could not reach Ollama at {base_url} ({exc})")
        return False

    print_status("Ollama", True, f"reachable at {base_url}")

    if llm_model not in names and not any(name.startswith(f"{llm_model}:") for name in names):
        print_warn("Ollama model", f"'{llm_model}' not found in local tags")
    else:
        print_status("Ollama model", True, f"'{llm_model}' is available")

    if embed_model not in names and not any(name.startswith(f"{embed_model}:") for name in names):
        print_warn("Embedding model", f"'{embed_model}' not found in local tags")
    else:
        print_status("Embedding model", True, f"'{embed_model}' is available")

    return True


def check_repo_paths() -> None:
    expected = [
        ROOT / "notebooks" / "aps",
        ROOT / "notebooks" / "agentic-search",
        ROOT / "outputs",
        ROOT / "data",
    ]
    for path in expected:
        if path.exists():
            print_status("Repo path", True, str(path.relative_to(ROOT)))
        else:
            print_warn("Repo path", f"missing expected path: {path.relative_to(ROOT)}")

    raw_train = ROOT / "data" / "raw" / "aps_failure_training_set.csv"
    raw_test = ROOT / "data" / "raw" / "aps_failure_test_set.csv"
    if raw_train.exists() and raw_test.exists():
        print_status("APS data", True, "raw APS training/test CSVs found")
    else:
        print_warn("APS data", "raw APS CSVs not found; APS notebooks will not run until they are added")


def main() -> int:
    print("IEEE Diffusion Demo — local setup check\n")

    ok_imports, missing = check_imports()
    if ok_imports:
        print_status("Python packages", True, "all required imports resolved")
    else:
        print_status("Python packages", False, f"missing packages: {', '.join(missing)}")

    ok_env = check_env()
    ok_ollama = check_ollama()
    check_repo_paths()

    all_ok = ok_imports and ok_env and ok_ollama
    print()
    if all_ok:
        print(f"{GREEN}Setup looks good. You can move on to the notebooks.{RESET}")
        return 0

    print(f"{YELLOW}Setup check completed with issues. Fix the failures above before running the full workflow.{RESET}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
