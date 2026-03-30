#!/usr/bin/env python3
"""Minimal release-smoke checks for the workshop repo."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

EXPECTED_DOCS = [
    "README.md",
    "docs/README.md",
    "docs/QA_CHECKLIST.md",
    "docs/OUTPUT_CONVENTIONS.md",
    "notebooks/README.md",
    ".env.example",
    ".gitignore",
    "scripts/check_setup.py",
]

EXPECTED_DIRS = [
    "data/raw",
    "data/processed",
    "outputs/figures",
    "outputs/tables",
    "outputs/models",
    "outputs/vectorstores",
]

NOTEBOOKS = [
    "notebooks/aps/01_DataExploration_Preprocessing_TUTORIAL.ipynb",
    "notebooks/aps/02_Failure_Clustering_TUTORIAL.ipynb",
    "notebooks/aps/03_Diffusion_Minority_Augmentation_TUTORIAL.ipynb",
    "notebooks/aps/04_Cost_Sensitive_Evaluation_TUTORIAL.ipynb",
    "notebooks/agentic-search/90_Llama_RAG_WebURL_TUTORIAL.ipynb",
    "notebooks/agentic-search/90_Llama_RAG_WebURL_TUTORIAL_AGENTIC.ipynb",
    "notebooks/agentic-search/91_Llama_RAG_Firecrawl_TUTORIAL_AGENTIC.ipynb",
]

RELEASE_MARKERS = [
    "RELEASE_POLISH_HEADER_V1",
    "RELEASE_POLISH_CONFIG_V1",
]


def check_exists(repo_root: Path, rel_paths: list[str], kind: str) -> list[str]:
    missing = []
    for rel in rel_paths:
        if not (repo_root / rel).exists():
            missing.append(rel)
    if missing:
        print(f"Missing {kind}:")
        for rel in missing:
            print(f" - {rel}")
    else:
        print(f"All expected {kind} are present.")
    return missing


def check_release_markers(repo_root: Path) -> list[str]:
    missing = []
    for rel in NOTEBOOKS:
        path = repo_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if not all(marker in text for marker in RELEASE_MARKERS):
            missing.append(rel)
    if missing:
        print("Notebooks missing release-polish markers:")
        for rel in missing:
            print(f" - {rel}")
    else:
        print("All notebooks contain the standardized release-polish header/config markers.")
    return missing


def check_firecrawl_wording(repo_root: Path) -> list[str]:
    flagged = []
    for rel in ["README.md", "notebooks/README.md", "docs/README.md"]:
        path = repo_root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        if "duckduckgo" in text or "trafilatura" in text:
            flagged.append(rel)
    if flagged:
        print("Found legacy wording that should be reviewed:")
        for rel in flagged:
            print(f" - {rel}")
    else:
        print("No DuckDuckGo/Trafilatura wording found in the key docs checked.")
    return flagged


def main() -> int:
    parser = argparse.ArgumentParser(description="Run minimal release smoke checks.")
    parser.add_argument("repo_root", nargs="?", default=".", help="Path to the local repo root")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    doc_missing = check_exists(repo_root, EXPECTED_DOCS, "docs/files")
    dir_missing = check_exists(repo_root, EXPECTED_DIRS, "directories")
    nb_missing = check_exists(repo_root, NOTEBOOKS, "notebooks")
    marker_missing = check_release_markers(repo_root)
    wording_flagged = check_firecrawl_wording(repo_root)

    failed = bool(doc_missing or dir_missing or nb_missing or marker_missing or wording_flagged)
    if failed:
        print("\nRelease smoke checks: FAILED")
        return 1

    print("\nRelease smoke checks: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
