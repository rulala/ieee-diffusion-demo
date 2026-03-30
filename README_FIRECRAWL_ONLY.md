# Firecrawl-only agentic-search note

The notebooks under `notebooks/agentic-search/` are aligned to a **Firecrawl-only** retrieval flow.

Included notebooks:
- `90_Llama_RAG_WebURL_TUTORIAL.ipynb` — baseline URL-grounded RAG using Firecrawl scrape for the seed URL
- `90_Llama_RAG_WebURL_TUTORIAL_AGENTIC.ipynb` — explicit Firecrawl search -> scrape agentic loop
- `91_Llama_RAG_Firecrawl_TUTORIAL_AGENTIC.ipynb` — Firecrawl search with markdown scraping enabled in one operation

What changed:
- DuckDuckGo and Trafilatura are no longer part of the intended agentic-search path.
- The root `README.md` is the primary setup guide.
- Advanced follow-on work is parked in `docs/ADVANCED_RESEARCH_DIRECTIONS.md` rather than mixed into the workshop baseline.

Configuration:
- store the key in `.env` at the repo root or in your shell environment as `FIRECRAWL_API_KEY`
- do not hardcode API keys in notebooks or committed files
