# IEEE Diffusion Demo

A workshop-first repository for two applied AI case studies in transport:

1. **Case Study I — APS failure prediction with diffusion-based minority augmentation**
2. **Case Study II — Firecrawl-only RAG and agentic web expansion with local LLaMA models**

This repo is designed as a **baseline workshop artifact**, not a state-of-the-art benchmark claim. The emphasis is on end-to-end reasoning, controlled comparisons, and reproducible notebook workflows.

## What is in scope

### APS workflow
- raw APS CSV ingestion and cleanup
- missing-value handling, scaling, and PCA
- failure clustering as a diagnostic step
- diffusion-based minority augmentation in PCA space
- cost-sensitive evaluation with threshold moving

### RAG workflow
- baseline URL-grounded RAG using **Firecrawl scrape**
- Firecrawl-only agentic expansion when local retrieval is too thin
- local inference with **Ollama**
- local vector retrieval with **Chroma**

## Start here

### 1) Clone the repo

```bash
git clone https://github.com/rulala/ieee-diffusion-demo.git
cd ieee-diffusion-demo
```

### 2) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Create your local environment file

```bash
cp .env.example .env
```

Then edit `.env` and set your Firecrawl key.

### 5) Set up Ollama

In one terminal:

```bash
ollama serve
```

Then pull the required local models:

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

### 6) Run the setup check

```bash
python scripts/check_setup.py
```

### 7) Launch Jupyter

```bash
jupyter notebook
```

## Recommended notebook paths

### Workshop path A — APS predictive maintenance

Run in this order:

1. `notebooks/aps/01_DataExploration_Preprocessing_TUTORIAL.ipynb`
2. `notebooks/aps/02_Failure_Clustering_TUTORIAL.ipynb`
3. `notebooks/aps/03_Diffusion_Minority_Augmentation_TUTORIAL.ipynb`
4. `notebooks/aps/04_Cost_Sensitive_Evaluation_TUTORIAL.ipynb`

Use this path if you want the full rare-event classification workflow from raw APS files through cost-sensitive evaluation.

### Workshop path B — Firecrawl-only RAG

Run in this order:

1. `notebooks/agentic-search/90_Llama_RAG_WebURL_TUTORIAL.ipynb`
2. `notebooks/agentic-search/90_Llama_RAG_WebURL_TUTORIAL_AGENTIC.ipynb`
3. `notebooks/agentic-search/91_Llama_RAG_Firecrawl_TUTORIAL_AGENTIC.ipynb`

Use this path if you want the grounded-answering workflow from a single scraped URL to Firecrawl-powered agentic expansion.

## Required local assets

### APS data

Place the APS files here:

```text
data/raw/aps_failure_training_set.csv
data/raw/aps_failure_test_set.csv
data/raw/aps_failure_description.txt
```

These raw files are ignored by Git and should stay local.

### Firecrawl

The RAG notebooks expect:

```env
FIRECRAWL_API_KEY=fc-REPLACE_ME
```

stored in `.env` at the repo root or in your shell environment.

## Repository layout

```text
ieee-diffusion-demo/
├── archive/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── vectorstores/
├── docs/
├── notebooks/
│   ├── aps/
│   ├── agentic-search/
│   └── README.md
├── outputs/
│   ├── figures/
│   ├── models/
│   └── tables/
├── report/
├── scripts/
│   └── check_setup.py
├── .env.example
├── .gitignore
├── README.md
├── README_FIRECRAWL_ONLY.md
└── requirements.txt
```

## Output conventions

### APS notebooks
- intermediate artifacts: `data/interim/`
- processed experiment-ready data: `data/processed/`
- report-ready figures/tables: `outputs/figures/`, `outputs/tables/`
- model checkpoints: `outputs/models/`

### RAG notebooks
- optional persisted Chroma store: `data/vectorstores/chroma_db/`
- local screenshots or demo captures: save under `outputs/figures/` if you want to reference them in the report

## Which notebook should I open first?

- Want the workshop’s main predictive-maintenance story? Start with **APS notebook 01**.
- Want the local LLaMA + retrieval demo? Start with **90_Llama_RAG_WebURL_TUTORIAL.ipynb**.
- Want the most stable report companion? Read the report in `docs/` first, then follow the notebook order in `notebooks/README.md`.

## Reports and documentation

- Main workshop baseline report: see `docs/`
- Notebook map and run guidance: see `notebooks/README.md`
- Firecrawl-only migration note: see `README_FIRECRAWL_ONLY.md`

## Troubleshooting quick hits

- If APS CSV columns look wrong, check `skiprows=20`.
- If missingness appears to be zero, confirm the string `"na"` was converted to real `NaN` values.
- If diffusion training diverges, reduce learning rate, increase batch size, or stay in PCA space.
- If the RAG notebooks retrieve weak context, adjust chunk size, chunk overlap, and top-k.
- If the RAG answer is unsupported, strengthen the refusal rule and inspect the retrieved chunks.

## Notes on reproducibility

- This repo favors **clear teaching flow** over maximal abstraction.
- Generated local artifacts such as APS checkpoints, timestamped CSVs, and persisted vectorstores should usually stay out of version control.
- The report documents the workshop baseline faithfully, but some RAG sections are architecture-led rather than screenshot-led unless local run artifacts have been captured.

## Contact

For workshop-related questions:
- `rula@womeninai.co`
