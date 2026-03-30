#!/usr/bin/env python3
"""Apply a light "release polish" pass to the workshop notebooks.

What this script does
- Prepends a standardized markdown header to each target notebook.
- Prepends a small config cell that centralizes the values users are expected to edit.
- Creates the standard output directory structure if it does not exist.
- Applies conservative path/name replacements so baseline outputs follow a predictable scheme.

This script is intentionally idempotent. Re-running it should update the
release-polish cells rather than duplicating them.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Any

import nbformat
from nbformat.v4 import new_markdown_cell, new_code_cell

HEADER_MARKER = "RELEASE_POLISH_HEADER_V1"
CONFIG_MARKER = "RELEASE_POLISH_CONFIG_V1"

NOTEBOOK_SPECS: Dict[str, Dict[str, Any]] = {
    "notebooks/aps/01_DataExploration_Preprocessing_TUTORIAL.ipynb": {
        "title": "Notebook 01 — Preprocessing + PCA",
        "purpose": "Load the raw APS CSVs, handle missingness, encode labels, scale, impute, and export the PCA datasets used by the later APS notebooks.",
        "inputs": [
            "../../data/raw/aps_failure_training_set.csv",
            "../../data/raw/aps_failure_test_set.csv",
        ],
        "outputs": [
            "../../data/processed/aps_imputed_train.csv",
            "../../data/processed/aps_imputed_test.csv",
            "../../data/processed/aps_pca_train.csv",
            "../../data/processed/aps_pca_test.csv",
        ],
        "runtime": "5–15 min code runtime",
        "run_after": "Start here",
        "internet": "No",
        "config": [
            ("TRAIN_CSV", "../../data/raw/aps_failure_training_set.csv"),
            ("TEST_CSV", "../../data/raw/aps_failure_test_set.csv"),
            ("IMPUTED_TRAIN_OUT", "../../data/processed/aps_imputed_train.csv"),
            ("IMPUTED_TEST_OUT", "../../data/processed/aps_imputed_test.csv"),
            ("PCA_TRAIN_OUT", "../../data/processed/aps_pca_train.csv"),
            ("PCA_TEST_OUT", "../../data/processed/aps_pca_test.csv"),
        ],
        "replacements": {
            "imp_aps_mean_failure_training_set.csv": "../../data/processed/aps_imputed_train.csv",
            "imp_aps_mean_failure_test_set.csv": "../../data/processed/aps_imputed_test.csv",
            "../../data/processed/pca_aps_mean_failure_train_set.csv": "../../data/processed/aps_pca_train.csv",
            "../../data/processed/pca_aps_mean_failure_test_set.csv": "../../data/processed/aps_pca_test.csv",
        },
    },
    "notebooks/aps/02_Failure_Clustering_TUTORIAL.ipynb": {
        "title": "Notebook 02 — Failure Clustering",
        "purpose": "Diagnose whether the APS failure class is heterogeneous or multi-modal in PCA space before synthetic-data generation.",
        "inputs": [
            "../../data/processed/aps_pca_train.csv",
            "../../data/processed/aps_pca_test.csv",
        ],
        "outputs": [
            "../../outputs/figures/aps_failure_clusters.png",
            "../../outputs/tables/aps_failure_clusters.csv (optional export)",
        ],
        "runtime": "3–10 min code runtime",
        "run_after": "Notebook 01",
        "internet": "No",
        "config": [
            ("PCA_TRAIN_CSV", "../../data/processed/aps_pca_train.csv"),
            ("PCA_TEST_CSV", "../../data/processed/aps_pca_test.csv"),
            ("CLUSTER_FIGURE_OUT", "../../outputs/figures/aps_failure_clusters.png"),
            ("CLUSTER_TABLE_OUT", "../../outputs/tables/aps_failure_clusters.csv"),
        ],
        "replacements": {
            "../../data/processed/pca_aps_mean_failure_train_set.csv": "../../data/processed/aps_pca_train.csv",
            "../../data/processed/pca_aps_mean_failure_test_set.csv": "../../data/processed/aps_pca_test.csv",
            "Failure_Cluster_Diagram.png": "../../outputs/figures/aps_failure_clusters.png",
        },
    },
    "notebooks/aps/03_Diffusion_Minority_Augmentation_TUTORIAL.ipynb": {
        "title": "Notebook 03 — Diffusion Minority Augmentation",
        "purpose": "Train a DDPM-style diffusion model on the APS failure PCA vectors and export a predictable set of synthetic-data artifacts.",
        "inputs": [
            "../../data/processed/aps_pca_train.csv",
            "../../data/processed/aps_pca_test.csv",
        ],
        "outputs": [
            "../../outputs/tables/diffusion_synth_failures.csv",
            "../../outputs/tables/aps_train_diffusion_augmented.csv",
            "../../outputs/models/aps_diffusion_denoiser.pth",
        ],
        "runtime": "10–25 min code runtime",
        "run_after": "Notebook 01 (and usually after Notebook 02)",
        "internet": "No",
        "config": [
            ("PCA_TRAIN_CSV", "../../data/processed/aps_pca_train.csv"),
            ("PCA_TEST_CSV", "../../data/processed/aps_pca_test.csv"),
            ("SYNTH_OUT", "../../outputs/tables/diffusion_synth_failures.csv"),
            ("AUGMENTED_TRAIN_OUT", "../../outputs/tables/aps_train_diffusion_augmented.csv"),
            ("DENOISER_OUT", "../../outputs/models/aps_diffusion_denoiser.pth"),
        ],
        "replacements": {
            "../../data/processed/pca_aps_mean_failure_train_set.csv": "../../data/processed/aps_pca_train.csv",
            "../../data/processed/pca_aps_mean_failure_test_set.csv": "../../data/processed/aps_pca_test.csv",
            "diffusion_synth_failure_pca_": "diffusion_synth_failures",
            "pca_aps_mean_failure_train_set_diffusion_augmented_": "aps_train_diffusion_augmented",
            "diffusion_denoiser_pca_": "aps_diffusion_denoiser",
        },
    },
    "notebooks/aps/04_Cost_Sensitive_Evaluation_TUTORIAL.ipynb": {
        "title": "Notebook 04 — Cost-Sensitive Evaluation",
        "purpose": "Compare the baseline classifier and diffusion-augmented classifier under the APS cost function, threshold search, and evaluation protocol.",
        "inputs": [
            "../../data/processed/aps_pca_train.csv",
            "../../data/processed/aps_pca_test.csv",
            "../../outputs/tables/diffusion_synth_failures.csv (optional)",
        ],
        "outputs": [
            "../../outputs/tables/aps_demo_results.csv",
            "../../outputs/tables/aps_diffusion_tuning_results.csv",
            "../../outputs/figures/threshold_curve_baseline.png",
            "../../outputs/figures/threshold_curve_diffusion.png",
        ],
        "runtime": "5–15 min code runtime",
        "run_after": "Notebook 01, and optionally Notebook 03",
        "internet": "No",
        "config": [
            ("PCA_TRAIN_CSV", "../../data/processed/aps_pca_train.csv"),
            ("PCA_TEST_CSV", "../../data/processed/aps_pca_test.csv"),
            ("SYNTH_CSV_GLOB", "../../outputs/tables/diffusion_synth_failures*.csv"),
            ("DEMO_RESULTS_OUT", "../../outputs/tables/aps_demo_results.csv"),
            ("TUNING_RESULTS_OUT", "../../outputs/tables/aps_diffusion_tuning_results.csv"),
            ("BASELINE_FIG_OUT", "../../outputs/figures/threshold_curve_baseline.png"),
            ("DIFFUSION_FIG_OUT", "../../outputs/figures/threshold_curve_diffusion.png"),
        ],
        "replacements": {
            "../../data/processed/pca_aps_mean_failure_train_set.csv": "../../data/processed/aps_pca_train.csv",
            "../../data/processed/pca_aps_mean_failure_test_set.csv": "../../data/processed/aps_pca_test.csv",
            "../../outputs/tables/diffusion_synth_failure_pca_": "../../outputs/tables/diffusion_synth_failures",
        },
    },
    "notebooks/agentic-search/90_Llama_RAG_WebURL_TUTORIAL.ipynb": {
        "title": "Notebook 90 — Baseline Firecrawl URL RAG",
        "purpose": "Build the simplest grounded-answering path from one known URL to chunks, embeddings, retrieval, and a local Ollama answer.",
        "inputs": [
            "One seed URL",
            "../../.env with FIRECRAWL_API_KEY",
        ],
        "outputs": [
            "In-memory Chroma collection",
            "Grounded answer",
            "Optional Gradio UI",
        ],
        "runtime": "5–15 min code runtime (plus model pulls the first time)",
        "run_after": "Can be run independently",
        "internet": "Yes — for Firecrawl scrape and the seed URL",
        "config": [
            ("LLM_MODEL", "llama3"),
            ("EMBED_MODEL", "nomic-embed-text"),
            ("URL", "https://en.wikipedia.org/wiki/Ohiya"),
            ("PERSIST_DIRECTORY", "../../outputs/vectorstores/rag_firecrawl_web_demo"),
        ],
        "replacements": {
            'collection_name="rag_firecrawl_web_demo"': 'collection_name="rag_firecrawl_web_demo",\n persist_directory="../../outputs/vectorstores/rag_firecrawl_web_demo"',
        },
    },
    "notebooks/agentic-search/90_Llama_RAG_WebURL_TUTORIAL_AGENTIC.ipynb": {
        "title": "Notebook 90+ — Firecrawl Agentic Search (explicit search → scrape)",
        "purpose": "Start with local retrieval, trigger Firecrawl Search when context is thin, then scrape, ingest, re-retrieve, and answer from the enlarged evidence base.",
        "inputs": [
            "A user question",
            "../../.env with FIRECRAWL_API_KEY",
        ],
        "outputs": [
            "Expanded in-memory Chroma collection",
            "Grounded answer with expanded evidence base",
        ],
        "runtime": "10–20 min code runtime depending on web retrieval",
        "run_after": "Notebook 90 or independently",
        "internet": "Yes — for Firecrawl search + scrape",
        "config": [
            ("LLM_MODEL", "llama3"),
            ("EMBED_MODEL", "nomic-embed-text"),
            ("MIN_CONTEXT_CHARS", 1500),
            ("PERSIST_DIRECTORY", "../../outputs/vectorstores/rag_firecrawl_agentic_search"),
        ],
        "replacements": {},
    },
    "notebooks/agentic-search/91_Llama_RAG_Firecrawl_TUTORIAL_AGENTIC.ipynb": {
        "title": "Notebook 91 — Firecrawl search-with-scraping agentic RAG",
        "purpose": "Use Firecrawl’s search-with-scraping path to expand the evidence base in one step when local retrieval is insufficient.",
        "inputs": [
            "A user question",
            "../../.env with FIRECRAWL_API_KEY",
        ],
        "outputs": [
            "Expanded in-memory Chroma collection",
            "Grounded answer with retrieved sources",
        ],
        "runtime": "10–20 min code runtime depending on web retrieval",
        "run_after": "Notebook 90 or independently",
        "internet": "Yes — for Firecrawl search-with-scraping",
        "config": [
            ("LLM_MODEL", "llama3"),
            ("EMBED_MODEL", "nomic-embed-text"),
            ("MIN_CONTEXT_CHARS", 1500),
            ("PERSIST_DIRECTORY", "../../outputs/vectorstores/rag_firecrawl_agentic_combined"),
        ],
        "replacements": {},
    },
}

STANDARD_DIRS = [
    "data/raw",
    "data/processed",
    "outputs/figures",
    "outputs/tables",
    "outputs/models",
    "outputs/vectorstores",
]


def build_header_markdown(spec: Dict[str, Any]) -> str:
    inputs = "\n".join(f"- `{item}`" for item in spec["inputs"])
    outputs = "\n".join(f"- `{item}`" for item in spec["outputs"])
    return f"""<!-- {HEADER_MARKER} -->
# {spec['title']}

**Purpose**
{spec['purpose']}

**Inputs**
{inputs}

**Outputs**
{outputs}

**Estimated runtime**
- {spec['runtime']}

**Run order**
- Run after: **{spec['run_after']}**

**Needs internet?**
- {spec['internet']}

> Edit the config cell directly below if you need to change paths, model names, or the seed URL/question setup.
"""


def build_config_code(spec: Dict[str, Any]) -> str:
    lines = [f"# {CONFIG_MARKER}", "# Edit only the values in this cell when adapting the notebook."]
    for key, value in spec["config"]:
        if isinstance(value, str):
            lines.append(f'{key} = "{value}"')
        else:
            lines.append(f"{key} = {value}")
    lines.append("")
    lines.append("from pathlib import Path")
    lines.append("for _path in [Path('../../data/processed'), Path('../../outputs/figures'), Path('../../outputs/tables'), Path('../../outputs/models'), Path('../../outputs/vectorstores')]:")
    lines.append("    _path.mkdir(parents=True, exist_ok=True)")
    return "\n".join(lines)


def strip_existing_release_polish_cells(cells: List[Any]) -> List[Any]:
    cleaned = []
    for cell in cells:
        src = "".join(cell.get("source", []))
        if HEADER_MARKER in src or CONFIG_MARKER in src:
            continue
        cleaned.append(cell)
    return cleaned


def apply_replacements(nb: Any, replacements: Dict[str, str]) -> None:
    if not replacements:
        return
    for cell in nb.cells:
        if "source" not in cell:
            continue
        src = "".join(cell["source"])
        new_src = src
        for old, new in replacements.items():
            new_src = new_src.replace(old, new)
        if new_src != src:
            cell["source"] = [new_src]


def polish_notebook(nb_path: Path, spec: Dict[str, Any]) -> None:
    nb = nbformat.read(nb_path, as_version=4)
    nb.cells = strip_existing_release_polish_cells(nb.cells)
    header = new_markdown_cell(build_header_markdown(spec))
    config = new_code_cell(build_config_code(spec))
    nb.cells = [header, config] + nb.cells
    apply_replacements(nb, spec.get("replacements", {}))
    nbformat.write(nb, nb_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply release polish to workshop notebooks.")
    parser.add_argument("repo_root", nargs="?", default=".", help="Path to the local repo root")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    if not repo_root.exists():
        raise SystemExit(f"Repo root does not exist: {repo_root}")

    for rel_dir in STANDARD_DIRS:
        (repo_root / rel_dir).mkdir(parents=True, exist_ok=True)

    updated = []
    missing = []
    for rel_path, spec in NOTEBOOK_SPECS.items():
        nb_path = repo_root / rel_path
        if not nb_path.exists():
            missing.append(rel_path)
            continue
        polish_notebook(nb_path, spec)
        updated.append(rel_path)

    print("Release polish complete.")
    if updated:
        print("Updated notebooks:")
        for item in updated:
            print(f" - {item}")
    if missing:
        print("Skipped (not found in repo):")
        for item in missing:
            print(f" - {item}")


if __name__ == "__main__":
    main()
