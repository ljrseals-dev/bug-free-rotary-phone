# Checkpoints

| Checkpoint | License | Params | RTF | LoRA | Role | Scorecard |
|---|---|---|---|---|---|---|
| VoxCPM1.5 (OpenBMB) | Apache 2.0 | ~750M | ~0.17 (RTX 4090) | Native | Design 2 primary | `voxcpm15.md` |
| VITS-evo (ZDisket) | Apache 2.0 / MIT | ~31M | ~0.18 (CPU) | ✗ | Design 1 base; Design 2 CPU baseline | `vitsevo.md` |
| CosyVoice 3 | Verify per release | — | — | — | External SECS comparison only | not accepted |
| Fish Speech | Verify per release | — | — | — | External comparison only | not accepted |
| IndexTTS2 | Verify per release | — | — | — | External comparison only | not accepted |

## Rules

1. **Pin the revision hash** in the config before training. Floating `main` is not acceptable.
2. **External-comparison-only** models are cited from their published numbers; we do not
   retrain or release derivatives of them.
3. **No baked speaker slots** are released from any checkpoint.
4. A checkpoint enters `configs/` only after its scorecard clears the gate.

## Pinning format

```yaml
base_model: "openbmb/VoxCPM1.5"
revision: "<commit-sha>"
```
