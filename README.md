# IEEE Diffusion Demo

A workshop-first repository for two applied AI case studies in transport:

1. **Case Study I — APS failure prediction with diffusion-based minority augmentation**
2. **Case Study II — Firecrawl-only RAG and agentic web expansion with local LLaMA models**

This repo is designed as a **baseline workshop artifact**, not a state-of-the-art benchmark claim. The emphasis is on end-to-end reasoning, controlled comparisons, and reproducible notebook workflows.

## Why this workshop is framed differently

### For data scientists
This is **not** a generic accuracy benchmark. APS failure prediction is a high-stakes, cost-sensitive ITS problem, so the workshop de-emphasizes raw accuracy and anchors the task with the operational cost function:

```text
Cost = 10 x FP + 500 x FN
```

In fleet operations, missing a true failure is far more expensive than triggering an unnecessary maintenance check. That is also why diffusion appears here: the rare events with the highest safety and operational impact are often the hardest to collect at scale, so generative methods are explored as a practical way to expand minority coverage.

### For transport engineers
The technical story is kept practical. The diffusion model learns to reverse a gradual noising process on real failure vectors so it can generate additional plausible failures for downstream training; the goal is **not** a perfectly balanced dataset, but better coverage of minority cases. The RAG notebooks make the LLM side concrete too: a language model can sound plausible while being wrong, so grounding shifts the task from "answer from memory" to "answer from retrieved evidence" such as safety bulletins, operating procedures, incident reports, and maintenance manuals.

## Workshop path vs advanced path

### Workshop path
Use this if you want the clean, shareable baseline:
- APS notebooks 01 -> 04
- Firecrawl RAG notebooks 90 -> 91
- stabilized workshop report in `docs/`

### Advanced path
Potential follow-on work is intentionally parked in:
- `docs/ADVANCED_RESEARCH_DIRECTIONS.md`

That keeps the current release compact and easy to teach while preserving a clear paper-track roadmap.

## Start here

### 1) Clone the repo

```bash
git clone https://github.com/rulala/ieee-diffusion-demo.git
cd ieee-diffusion-demo
```

### 2) Create and activate a virtual environment

**Recommended Python:** 3.10 or 3.11

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

## Optional quick demo UI

If you want a lightweight demo surface for the RAG/search side without opening notebooks first, run:

```bash
python ui/search_demo.py
```

The tiny Gradio UI lets people:
- ask a question
- choose **Seed URL RAG**, **Firecrawl web search**, or **both**
- inspect the grounded answer
- inspect source URLs
- inspect retrieved chunks

This UI is intentionally small. It does **not** replace the notebooks and it does not train models.

## Setup at a glance

- **Internet required:** Firecrawl RAG notebooks only
- **Local only:** APS notebooks after the APS data is present; Ollama inference is local
- **Firecrawl key location:** `.env` at the repo root
- **Models expected locally:** `llama3`, `nomic-embed-text`
- **Best first run:** APS notebook 01 or RAG notebook 90, depending on which case study you want first

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

## Typical runtime expectations

### APS notebooks
- preprocessing + PCA: ~5-15 min code runtime
- failure clustering: ~3-10 min
- diffusion augmentation: ~10-25 min
- cost-sensitive evaluation: ~5-15 min

### Firecrawl RAG notebooks
- baseline URL RAG: usually quickest to start
- agentic variants: runtime depends on web retrieval, Firecrawl responses, and Ollama speed

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
│   ├── check_setup.py
│   ├── apply_notebook_release_polish.py
│   └── release_smoke_checks.py
├── ui/
│   ├── search_demo.py
│   └── README.md
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

For the stable naming scheme, see `docs/OUTPUT_CONVENTIONS.md`.

## Reports and documentation

- main workshop baseline report: see `docs/`
- notebook map and run guidance: see `notebooks/README.md`
- Firecrawl-only migration note: see `README_FIRECRAWL_ONLY.md`
- parked future work: see `docs/ADVANCED_RESEARCH_DIRECTIONS.md`
- send-out checks: see `docs/SENDOUT_CHECKLIST.md`
- optional tiny Gradio demo: see `ui/README.md`

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
- Rula Awad rula@womeninai.co / rula.awad@gmail.com
- Mona Jaber m.jaber@qmul.ac.uk
