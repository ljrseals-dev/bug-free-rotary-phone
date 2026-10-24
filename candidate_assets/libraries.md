# Libraries

| Library | License | Role | Status |
|---|---|---|---|
| PyTorch | BSD-3 | Core training/inference | Accepted |
| torchaudio | BSD-2 | Audio I/O, resampling | Accepted |
| speechbrain | Apache 2.0 | ECAPA-TDNN speaker embeddings | Accepted |
| resemblyzer | Apache 2.0 | SECS replication encoder | Accepted |
| peft | Apache 2.0 | LoRA implementation | Accepted |
| mlx-audio-train | Open (verify) | Methodological blueprint only | Accepted with conditions |
| librosa | ISC | MCD, F0 analysis | Accepted |
| jiwer | Apache 2.0 | WER for secondary composite | Accepted |

## Security checks

- Run `pip-audit` (or equivalent) before each training run; record the output in the run log.
- Any newly disclosed CVE in a direct dependency blocks training until patched or mitigated.
- Pin all versions in `requirements.txt` (not included until the first run; add then).

## Prohibited

- Any library that phones home with audio by default.
- Any closed-source voice-cloning SaaS in the training or evaluation path.
