# Release QA Checklist

Use this before sending the repo/report out.

## APS checklist

- [ ] Notebook 01 runs after the raw APS CSVs are placed in `data/raw/`.
- [ ] Notebook 01 exports stable processed outputs into `data/processed/`.
- [ ] Notebook 02 loads the PCA files from `data/processed/` and renders the clustering figure.
- [ ] Notebook 03 produces synthetic failures plus an augmented train file in `outputs/tables/` and the denoiser checkpoint in `outputs/models/`.
- [ ] Notebook 04 completes the baseline vs diffusion evaluation using the APS cost function.
- [ ] The threshold plots save correctly into `outputs/figures/`.
- [ ] The demo result table matches the report narrative closely enough to avoid a trust mismatch.

## RAG checklist

- [ ] Baseline URL RAG answers only from retrieved context.
- [ ] The agentic notebook expands when context is thin.
- [ ] The refusal behavior still says "I don't know based on the provided context" when evidence is insufficient.
- [ ] `FIRECRAWL_API_KEY` is local only and is not committed.
- [ ] The Firecrawl-only notebook descriptions are consistent across the repo docs and report.

## Docs checklist

- [ ] `README.md` matches the actual notebook names and run order.
- [ ] `notebooks/README.md` matches the current notebook set.
- [ ] The stabilized report matches the repo naming and Firecrawl-only RAG story.
- [ ] There is no leftover DuckDuckGo/Trafilatura wording in the main docs if the repo is now Firecrawl-only.
- [ ] `python scripts/check_setup.py` passes locally.
- [ ] `python scripts/release_smoke_checks.py` passes locally.
