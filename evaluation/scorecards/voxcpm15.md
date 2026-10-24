# Asset Scorecard — VoxCPM1.5 (OpenBMB)

**Type:** checkpoint / TTS base model
**Role in project:** Design 2 primary base (LoRA + SFT)
**Date:** 2026

| Criterion | Score | Justification |
|---|---|---|
| Maintenance | 4 | Active OpenBMB releases; regular updates |
| License | 5 | Apache 2.0 — commercial and derivative use permitted |
| Real usage | 4 | Widely adopted in the TTS community; third-party fine-tunes exist |
| Dependencies | 4 | Standard PyTorch stack; MiniCPM-4 backbone adds weight |
| Security | 4 | No blocking CVEs in the core dependency tree at time of review |
| Fit | 5 | Native LoRA and SFT support — exactly what Design 2 requires |
| Documentation | 4 | Clear README; LoRA/fine-tune paths documented |
| **Total** | **30** | |

## Gate

- [x] License ≥ 4 (Apache 2.0)
- [x] Fit ≥ 4
- [x] Security ≥ 3

**Decision:** **Accept** as Design 2 primary base.

## Notes

- 44.1 kHz output; token rate 6.25 Hz; RTF ~0.17 on RTX 4090.
- Supports zero-shot cloning from a short reference clip.
- Freeze the exact revision hash in `configs/design2_lora.yaml` before training.
