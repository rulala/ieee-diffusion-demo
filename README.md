# IEEE Diffusion Demo

IEEE Diffusion Demo is a hands-on workshop repository with two complementary tracks:

1. **APS Failure Prediction with Diffusion Augmentation**
   - preprocessing
   - optional failure clustering
   - diffusion-based minority augmentation
   - cost-sensitive evaluation

2. **Agentic Web Search**
   - Ollama + Chroma local retrieval
   - seed-URL indexing
   - agentic web expansion
   - optional Firecrawl integration

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


## What to clone

git clone https://github.com/rulala/ieee-diffusion-demo.git
cd ieee-diffusion-demo

##Set up a virtual environment

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

## Install dependencies

pip install -r requirements.txt
pip install firecrawl-py python-dotenv
jupyter notebook

#Ollama setup for the agentic-search notebooks

**Start Ollama locally:

ollama serve
ollama pull llama3
ollama pull nomic-embed-text
APS dataset placement

Place the APS files here:

data/raw/aps_failure_training_set.csv
data/raw/aps_failure_test_set.csv
data/raw/aps_failure_description.txt

The preprocessing workflow writes intermediate files to data/interim/ and processed experiment files to data/processed/.

Recommended run order
APS notebooks

notebooks/aps/01_DataExploration_Preprocessing_TUTORIAL.ipynb

notebooks/aps/02_Failure_Clustering_TUTORIAL.ipynb (optional)

notebooks/aps/03_Diffusion_Minority_Augmentation_TUTORIAL.ipynb

notebooks/aps/04_Cost_Sensitive_Evaluation_TUTORIAL.ipynb

Agentic-search notebooks

notebooks/agentic-search/90_Llama_RAG_WebURL_TUTORIAL.ipynb

notebooks/agentic-search/90_Llama_RAG_WebURL_TUTORIAL_AGENTIC.ipynb

notebooks/agentic-search/91_Llama_RAG_Firecrawl_TUTORIAL_AGENTIC.ipynb

Firecrawl setup

Create a .env file in the repo root:

FIRECRAWL_API_KEY=your_api_key_here

A starter template is included as .env.example.

Notes

data/raw/ holds the original APS data.

data/interim/ holds intermediate local files.

data/processed/ holds processed and experiment-ready data artifacts.

outputs/figures/ and outputs/tables/ contain the main demo results used in the report.

report/ contains the workshop writeup and report assets.

Workshop goal

This project demonstrates how to generate synthetic failure-class data from an imbalanced APS dataset using diffusion, then use those generated failure examples to train a classifier and compare its performance against a simple baseline.

The main demo story is:

failure examples are rare

rare failure data make classification difficult

generating additional synthetic failure examples can improve a simple classifier

diffusion provides one way to create those minority-class examples

Demo comparison

The main APS demo compares:

Baseline: Logistic Regression trained on the original imbalanced APS training data

Improved model: Logistic Regression trained on APS data augmented with a small number of diffusion-generated failure examples

This repository is intended as a workshop/demo pipeline rather than a claim of state-of-the-art benchmark performance.

Suggested next cleanup steps

rename the Llama_RAG... notebook filenames so they consistently say Agentic_Search

add a short results section with figures from outputs/figures/

add a report summary section that references report/


Then run:

```bash
git add README.md
git commit -m "Update README to match current repo structure"
git push origin main

## For any help or to run this workshop contact:
rula@womeninai.co OR mona jaber
