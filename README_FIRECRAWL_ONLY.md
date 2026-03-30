# Firecrawl-only agentic-search note

The three notebooks under `notebooks/agentic-search/` have been aligned to a **Firecrawl-only** retrieval flow.

Included notebooks:
- `90_Llama_RAG_WebURL_TUTORIAL.ipynb` — baseline URL-grounded RAG using Firecrawl scrape for the seed URL
- `90_Llama_RAG_WebURL_TUTORIAL_AGENTIC.ipynb` — explicit Firecrawl search → scrape agentic loop
- `91_Llama_RAG_Firecrawl_TUTORIAL_AGENTIC.ipynb` — Firecrawl search with markdown scraping enabled in one operation

What changed:
- DuckDuckGo and Trafilatura are no longer part of the intended agentic-search path.
- The root `README.md` is now the primary setup guide.
- This file remains as a focused migration note for the RAG portion of the repo.

Configuration:
- store the key in `.env` at the repo root or in your shell environment as `FIRECRAWL_API_KEY`
- do not hardcode API keys in notebooks or committed files
