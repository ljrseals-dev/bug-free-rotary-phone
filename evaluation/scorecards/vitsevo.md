# Asset Scorecard — VITS-evo (ZDisket)

**Type:** checkpoint / library
**Role in project:** Design 1 base (CPU-feasible); Design 2 compute-efficient secondary
**Date:** 2026

| Criterion | Score | Justification |
|---|---|---|
| Maintenance | 3 | Smaller project; slower cadence than OpenBMB |
| License | 5 | Apache 2.0 with MIT DeepPhonemizer components — clean |
| Real usage | 3 | Used in community projects; smaller footprint than VoxCPM |
| Dependencies | 5 | Light: ONNX runtime path, minimal transitive deps |
| Security | 4 | Small dependency surface reduces supply-chain risk |
| Fit | 5 | ONNX release for speaker encoder + TTS; ~0.18 RTF on CPU |
| Documentation | 4 | ONNX usage and voice blending documented |
| **Total** | **29** | |

## Gate

- [x] License ≥ 4
- [x] Fit ≥ 4
- [x] Security ≥ 3

**Decision:** **Accept** as Design 1 base and Design 2 efficiency baseline.

## Notes

- ~31M parameters; ~5.6× faster than real time on CPU.
- Zero-shot cloning only — **no** native LoRA. Design 1 therefore trains only the DACA module
  and the bone-conduction filter, keeping base weights frozen.
