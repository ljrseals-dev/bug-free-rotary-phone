# Asset Scorecard — mlx-audio-train (akashicMarga)

**Type:** library / training framework
**Role in project:** Methodological blueprint for LoRA speaker cloning
**Date:** 2026

| Criterion | Score | Justification |
|---|---|---|
| Maintenance | 3 | Active but young project |
| License | 4 | Open repository; verify per-model license terms before use |
| Real usage | 3 | Newer; limited third-party adoption so far |
| Dependencies | 3 | MLX stack; Apple Silicon constraint adds friction |
| Security | 4 | Small surface; no blocking issues found |
| Fit | 5 | Pipeline 2 (LoRA + Speaker Embedding) is a direct blueprint |
| Documentation | 4 | Pipeline structure and parameters are documented |
| **Total** | **26** | |

## Gate

- [x] License ≥ 4 (with per-model verification condition)
- [x] Fit ≥ 4
- [x] Security ≥ 3

**Decision:** **Accept with conditions** — port the **method**, not the code.

## Conditions

1. We do not run MLX on our CUDA hardware; we reimplement Pipeline 2 on VoxCPM1.5.
2. Any hyperparameters adopted from this repo are cited in the paper.
3. No MLX-specific weights are released.

## Method elements adopted

- Speaker embedding extracted from reference mel.
- Embedding injected as a positional token in the codec prefix.
- LoRA rank 16 for speaker identity.
- 3 epochs, batch size 16.
- Embedding averaging + baking used **internally only**, never released.
