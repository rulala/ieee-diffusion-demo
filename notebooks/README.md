# Notebook guide

This repo contains two notebook paths:

- **APS** — predictive maintenance with diffusion-based minority augmentation
- **agentic-search** — Firecrawl-backed grounded answering with local LLaMA models

## APS notebook path

| Notebook | Purpose | Run after | Main outputs | Typical runtime |
|---|---|---|---|---|
| `aps/01_DataExploration_Preprocessing_TUTORIAL.ipynb` | Read APS CSVs, clean missingness, scale, and export PCA-ready data | none | cleaned/interim CSVs, PCA exports | 5–15 min |
| `aps/02_Failure_Clustering_TUTORIAL.ipynb` | Diagnose whether the minority class looks multi-modal | 01 | cluster labels, clustering visuals | 3–10 min |
| `aps/03_Diffusion_Minority_Augmentation_TUTORIAL.ipynb` | Train a diffusion model on failure-only PCA vectors and sample synthetic failures | 01, optionally 02 | synthetic failure CSVs, optional checkpoints | 10–25 min |
| `aps/04_Cost_Sensitive_Evaluation_TUTORIAL.ipynb` | Compare baseline vs augmented classifiers with threshold moving and APS cost | 01 and 03 | metrics tables, cost curves, threshold plots | 5–15 min |

## Agentic-search notebook path

| Notebook | Purpose | Run after | Main outputs | Notes |
|---|---|---|---|---|
| `agentic-search/90_Llama_RAG_WebURL_TUTORIAL.ipynb` | Baseline URL-grounded RAG using Firecrawl scrape | none | grounded answers, optional Gradio UI | Best first notebook for RAG |
| `agentic-search/90_Llama_RAG_WebURL_TUTORIAL_AGENTIC.ipynb` | Firecrawl explicit search → scrape → re-retrieve loop | 90 baseline recommended | expanded evidence base, sourced answers | Uses a simple retrieval-sufficiency trigger |
| `agentic-search/91_Llama_RAG_Firecrawl_TUTORIAL_AGENTIC.ipynb` | Firecrawl search-with-scraping in one step | 90 baseline recommended | expanded evidence base, sourced answers | Most direct Firecrawl-only variant |

## Before you run the RAG notebooks

Make sure all of the following are true:

1. `ollama serve` is running locally
2. `llama3` has been pulled
3. `nomic-embed-text` has been pulled
4. `.env` exists at the repo root
5. `FIRECRAWL_API_KEY` is set

You can test this with:

```bash
python scripts/check_setup.py
```

## Data expectations

### APS
The APS notebooks expect local raw files in `data/raw/`.

### RAG
The RAG notebooks expect internet access plus a valid Firecrawl key.

## Good first runs

- Want the cleanest predictive-maintenance story? Run APS notebooks `01 → 04`.
- Want the cleanest grounded-answering story? Run `90_Llama_RAG_WebURL_TUTORIAL.ipynb` first, then step up to the agentic notebooks.
