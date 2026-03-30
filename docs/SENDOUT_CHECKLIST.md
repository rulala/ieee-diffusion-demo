# Final Send-Out Checklist

Use this immediately before sharing the repo/report with workshop participants, recruiters, collaborators, or reviewers.

## Report

- [ ] The current report is the stabilized Firecrawl-only baseline version.
- [ ] The opening sections make the cost-sensitive framing clear early.
- [ ] The report explains diffusion and RAG in practical language for non-specialist readers.
- [ ] Advanced work is parked under research directions rather than mixed into the baseline claims.

## Repo

- [ ] `README.md` is the primary entry point and matches the current repo structure.
- [ ] `README_FIRECRAWL_ONLY.md` matches the actual agentic-search notebooks.
- [ ] `notebooks/README.md` matches the actual notebook names and run order.
- [ ] `docs/ADVANCED_RESEARCH_DIRECTIONS.md` exists and clearly parks future work.
- [ ] `.env.example` is present and no real API key is committed.
- [ ] `.gitignore` keeps local APS artifacts, vectorstores, and secrets out of version control.

## Local setup

- [ ] `python scripts/check_setup.py` passes locally.
- [ ] `ollama serve` runs locally.
- [ ] `llama3` is available locally.
- [ ] `nomic-embed-text` is available locally.
- [ ] `FIRECRAWL_API_KEY` is loaded from `.env` and not hardcoded.

## Notebook release polish

- [ ] `python scripts/apply_notebook_release_polish.py .` has been run if you want standardized notebook intro/config cells.
- [ ] `python scripts/release_smoke_checks.py .` passes locally.
- [ ] APS outputs save into the expected `outputs/` and `data/processed/` paths.
- [ ] The RAG notebooks still use a Firecrawl-only web acquisition path.

## Nice-to-have captures

- [ ] One APS figure is saved under `outputs/figures/`.
- [ ] One grounded RAG answer with sources is captured.
- [ ] One screenshot exists for the RAG workflow if you want a more polished send-out package.


## Optional UI demo

- [ ] `python ui/search_demo.py` launches locally.
- [ ] The UI returns a grounded answer for at least one test question.
- [ ] Source URLs and retrieved chunks are visible in the UI.
- [ ] The UI reads `FIRECRAWL_API_KEY` from local `.env` and does not hardcode secrets.
