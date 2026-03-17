# Local update notes

This curated folder was assembled from your original repo zip plus the later experiment result tables.

## Main cleanup applied
- removed `.git`, `.DS_Store`, and `__MACOSX` artifacts
- normalized `data/proccessed/` to `data/processed/`
- kept notebooks under `notebooks/aps/` and `notebooks/agentic-search/`
- placed the PDF draft under `report/`
- copied the available experiment result CSVs into both `outputs/tables/` and `report/tables/`

## Before pushing to GitHub
- review whether you want to keep large CSV files and model checkpoints in git
- review notebook paths after moving anything else locally
- decide whether to rename the `Llama_RAG` notebook filenames to `Agentic_Search` for consistency
