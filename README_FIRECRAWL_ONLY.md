# Firecrawl-only agentic-search update

This bundle rewrites the notebooks under `notebooks/agentic-search` so they no longer use DuckDuckGo or Trafilatura.

Included notebooks:
- `90_Llama_RAG_WebURL_TUTORIAL.ipynb` — baseline URL-grounded RAG using Firecrawl scrape for the seed URL
- `90_Llama_RAG_WebURL_TUTORIAL_AGENTIC.ipynb` — explicit Firecrawl search → scrape agentic loop
- `91_Llama_RAG_Firecrawl_TUTORIAL_AGENTIC.ipynb` — Firecrawl search with markdown scraping enabled in one operation

Configuration:
- store the key in `../../.env` or your shell environment as `FIRECRAWL_API_KEY`
- do not hardcode the API key in notebooks committed to GitHub
