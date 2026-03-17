# IEEE Diffusion Workshop

IEEE Diffusion Workshop is a hands-on workshop repository that combines diffusion-based augmentation for imbalanced APS failure prediction with a local agentic web search pipeline built on Ollama, Chroma, seed-URL indexing, and optional Firecrawl integration.

This repository contains two tracks:

1. **APS Failure Prediction with Diffusion Augmentation**
   - preprocessing
   - optional failure clustering
   - diffusion-based minority augmentation
   - cost-sensitive evaluation

2. **Agentic Web Search**
   - Ollama + Chroma local retrieval
   - seed-URL indexing
   - agentic web expansion
   - optional **Firecrawl** integration

---

## Repository layout

```text
ieee-diffusion-demo/
├── archive/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── notebooks/
│   ├── aps/
│   │   ├── 01_DataExploration_Preprocessing_TUTORIAL.ipynb
│   │   ├── 02_Failure_Clustering_TUTORIAL.ipynb
│   │   ├── 03_Diffusion_Minority_Augmentation_TUTORIAL.ipynb
│   │   └── 04_Cost_Sensitive_Evaluation_TUTORIAL.ipynb
│   └── agentic-search/
│       ├── 90_Llama_RAG_WebURL_TUTORIAL.ipynb
│       ├── 90_Llama_RAG_WebURL_TUTORIAL_AGENTIC.ipynb
│       └── 91_Llama_RAG_Firecrawl_TUTORIAL_AGENTIC.ipynb
├── outputs/
│   ├── figures/
│   ├── models/
│   └── tables/
├── report/
├── .env.example
├── .gitattributes
├── .gitignore
├── LOCAL_UPDATE_NOTES.md
├── README.md
└── requirements.txt

---

## What to clone

```bash
git clone https://github.com/rulala/ieee-diffusion-demo.git
cd ieee-diffusion-demo
```

If you are starting from the original repo instead:

```bash
git clone https://github.com/rulala/IEEE_Diffusion_Workshop.git ieee-diffusion-workshop
cd ieee-diffusion-workshop
```

---

## Set up a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
pip install firecrawl-py python-dotenv
jupyter notebook
```

---

## Ollama setup for the RAG notebooks

Start Ollama locally:

```bash
ollama serve
ollama pull llama3
ollama pull nomic-embed-text
```

---

## APS dataset placement

Place the raw APS CSV files here:

```text
data/raw/aps_failure_training_set.csv
data/raw/aps_failure_test_set.csv
```

The APS notebooks are already patched to read from `data/raw/` and write processed outputs to `data/processed/`.

---

## Recommended run order

### APS notebooks
1. `notebooks/aps/01_DataExploration_Preprocessing_TUTORIAL.ipynb`
2. `notebooks/aps/02_Failure_Clustering_TUTORIAL.ipynb` *(optional)*
3. `notebooks/aps/03_Diffusion_Minority_Augmentation_TUTORIAL.ipynb`
4. `notebooks/aps/04_Cost_Sensitive_Evaluation_TUTORIAL.ipynb`

### Agentic-search notebooks
5. `notebooks/agentic-search/90_Llama_RAG_WebURL_TUTORIAL.ipynb`
6. `notebooks/agentic-search/90_Llama_RAG_WebURL_TUTORIAL_AGENTIC.ipynb`
7. `notebooks/agentic-search/91_Llama_RAG_Firecrawl_TUTORIAL_AGENTIC.ipynb`

---

## Firecrawl setup

Create a `.env` file in the repo root:

```env
FIRECRAWL_API_KEY=your_api_key_here
```

A starter template is included as `.env.example`.

---

## Notes

- The notebook paths were updated to match this folder layout.
- Persisted Chroma data now lives under `data/vectorstores/chroma_db`.
- The Firecrawl notebook is a ready-made variant so you can move off DuckDuckGo + Trafilatura cleanly.

---

## Suggested next cleanup steps

- move repeated notebook logic into `src/`
- pin package versions more tightly
- add a results section with figures in `figures/`
- add your final paper/report under `docs/report/`

## For any help or to run this workshop contact:
rula@womeninai.co OR mona jaber
