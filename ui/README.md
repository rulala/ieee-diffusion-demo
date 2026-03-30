# Tiny Gradio Search Demo

This folder adds a **small technical UI** for the repo's RAG/search side.

It is intentionally narrow in scope:
- ask a question
- choose **Seed URL RAG**, **Firecrawl web search**, or **both**
- inspect the grounded answer
- inspect the source URLs
- inspect the retrieved chunks

It is **not** a training UI and it does not replace the notebooks.

## Run

From the repo root:

```bash
pip install -r requirements.txt
python ui/search_demo.py
```

## What it expects

- `ollama serve` running locally
- `llama3` pulled locally
- `nomic-embed-text` pulled locally
- `FIRECRAWL_API_KEY` in a local `.env` file at the repo root

## Why it exists

This gives the repo a quick demo surface for workshop participants, recruiters, or collaborators who want to try the **search / grounded-answering** part without opening notebooks first.
