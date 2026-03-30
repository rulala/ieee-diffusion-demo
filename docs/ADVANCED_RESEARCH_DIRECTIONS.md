# Advanced Research Directions

These items are intentionally **parked** so the current repo can remain a clean, shareable workshop baseline.
They are best treated as follow-on work for a paper, advanced track, or second-phase build.

## Case Study I — APS diffusion

### 1) Learned latent spaces beyond PCA
The current workshop uses PCA as a practical, interpretable compromise for tabular diffusion.
A natural extension is to move diffusion into a learned latent space such as a VAE-based representation.

### 2) Conditional minority generation by failure cluster
The clustering notebook already motivates the idea that the failure class may be multi-modal.
A future notebook could allow targeted generation by cluster, such as "sample 50 failures from cluster 1".

### 3) Stronger multivariate synthetic-data checks
The workshop baseline uses KS as a lightweight sanity check.
Future work could add multivariate checks such as MMD or precision/recall-for-distributions.

## Case Study II — Firecrawl-grounded RAG

### 4) Hybrid retrieval over the Firecrawl-fetched corpus
The current workflow emphasizes vector retrieval.
A future extension could add BM25 + embeddings as a hybrid retriever for technical terms, exact phrases, and error-code style queries.

### 5) Reflection-style retrieval control
The current agentic trigger is a lightweight sufficiency heuristic.
A stronger variant could let the model evaluate whether the currently retrieved evidence is relevant and sufficient before deciding to expand the corpus.

### 6) Dedicated verification pass
A second-pass verifier could check whether the generated answer is actually supported by the retrieved chunks before the answer is shown to the user.

## Professional / deployment layer

### 7) Experiment tracking
MLflow or Weights & Biases could be added to compare APS runs, augmentation sizes, thresholds, and RAG parameter choices more systematically.

### 8) Small interactive dashboard
A compact dashboard could make the workshop more tangible by showing threshold-vs-cost behavior for APS or evidence/answer support for RAG.

### 9) Local deployment notes
A future appendix could cover practical local deployment options such as quantization for larger local LLMs on constrained hardware.

## Why these are parked

The current release is intended to be:
- compact
- understandable
- easy to send out
- faithful to the workshop baseline

Parking the items above protects that clarity while preserving a strong roadmap for future research and paper development.
