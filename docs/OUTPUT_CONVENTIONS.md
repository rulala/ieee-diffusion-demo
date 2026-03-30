# Output Conventions

This repo uses a simple stable output layout so workshop users can find the generated files quickly.

## Directory layout

- `data/raw/` - user-supplied raw APS files
- `data/processed/` - cleaned / imputed / PCA outputs
- `outputs/figures/` - exported figures used in the report or QA
- `outputs/tables/` - CSV outputs and experiment tables
- `outputs/models/` - model checkpoints
- `data/vectorstores/chroma_db/` - local Chroma persistence (keep ignored by Git)

## Stable baseline filenames

Use predictable names for the baseline workshop path:

- `data/processed/aps_imputed_train.csv`
- `data/processed/aps_imputed_test.csv`
- `data/processed/aps_pca_train.csv`
- `data/processed/aps_pca_test.csv`
- `outputs/figures/aps_failure_clusters.png`
- `outputs/tables/diffusion_synth_failures.csv`
- `outputs/tables/aps_train_diffusion_augmented.csv`
- `outputs/models/aps_diffusion_denoiser.pth`
- `outputs/tables/aps_demo_results.csv`
- `outputs/tables/aps_diffusion_tuning_results.csv`
- `outputs/figures/threshold_curve_baseline.png`
- `outputs/figures/threshold_curve_diffusion.png`

## When to use timestamps

Use timestamps only for:

- multiple experimental runs you want to keep side by side
- checkpoints during tuning
- ablation runs that should not overwrite the baseline outputs

The workshop baseline should prefer the stable names above.
