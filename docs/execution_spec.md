# Execution Specification

Three of the five remaining items — GPU training runs, the human perceptual study,
and the signature lines of the authorship attestation — cannot be executed by an
AI system. They require physical hardware, consented speaker data, IRB approval,
and human participants. This document specifies exactly what remains.

---

## 1. GPU training runs

No training has been run. The following is the exact command sequence, the
acceptance test for each run, and the artifact each run must produce.

### 1.1 Design 1 — DACA + bone conduction on VITS-evo

| Step | Command | Acceptance test | Artifact |
|---|---|---|---|
| Smoke test | `python -m src.bone_conduction` | `max_diff_db_below_cutoff < 1.0` vs. reference | console output |
| Frozen-base check | 100-step run with `assert_base_frozen` every 10 steps | no assertion raised | `outputs/d1/frozen_check.log` |
| Full train | `python train.py --config configs/design1_daca.yaml` | 50 epochs, mel loss decreasing | `outputs/d1/checkpoints/` |
| Inference | 12 sentences × 3 conditions | 36 wav files, all finite, correct length | `outputs/d1/audio/` |

**Hardware:** VITS-evo is ~31M parameters and runs at ~0.18 RTF on CPU. A single
consumer GPU is sufficient; CPU-only training is feasible but slow.

### 1.2 Design 2 — LoRA and full fine-tune on VoxCPM1.5

| Condition | Command | Acceptance test | Artifact |
|---|---|---|---|
| Manifest | `CloningRun.make_manifest(speaker_dir, out.jsonl)` | ≥4 lines, one held-out `ref_audio` | `data/d2/manifest.jsonl` |
| Z0 (zero-shot) | inference with `ref_audio` only | 12 wavs generated | `outputs/d2/z0/` |
| L10 / L20 / L30 | `train_voxcpm_finetune.py` with `lora_rank=16`, 3 epochs | peak VRAM ≤ 12 GB at batch 16 | `outputs/d2/l*/adapter/` |
| F30 | same script, full fine-tune | peak VRAM ≤ 24 GB | `outputs/d2/f30/` |
| Metrics | `src/evaluate_secs.py` | SECS, MCD, F0 RMSE JSON per condition | `outputs/d2/metrics/` |

**Hardware:** VoxCPM1.5 LoRA fits in ~12 GB at batch size 16, versus ~24 GB for
full fine-tuning, so both arms fit on a single 24 GB card.

**Human blocker:** every command requires consented speaker recordings. Without
a completed `docs/consent_form.md` on file for the speaker in `speaker_dir`,
the run is not permitted under the project's own ethics policy.

---

## 2. Human perceptual study

### 2.1 What remains human

| Requirement | Why an AI cannot satisfy it |
|---|---|
| IRB / ethics approval | Requires institutional submission and a named human PI |
| Participant recruitment | N = 35, balanced gender and age band |
| Informed consent | Signed by each participant |
| Headphone verification | Physical listening check in the lab |
| Data collection | 35 sessions × ≤40 minutes |

### 2.2 Completed instrument

- Frozen protocol: `evaluation/perceptual_protocol.md` (commit hash before participant 1).
- Counterbalancing: Latin square across C0/C1/C2/C3 for 35 participants.
- Stimuli: 12 Harvard sentences per condition, normalized to −23 LUFS.
- Harness: `src/evaluate_secs.py` for the embedding side; mixed-effects for ratings.
- Preregistered rule: if Pearson r(SECS, SMOS) < 0.6, SECS is reported as insufficient alone.

### 2.3 Dependency chain

```
consented data → GPU runs → stimuli → perceptual study → results
```

No step can be skipped.

---

## 3. Author consent

See `docs/authorship_attestation.md`. Requires three human signatures.

---

## 4. Final milestone status

| Milestone | Status | Completed artifact | Human blocker |
|---|---|---|---|
| Author consent & affiliation | Document complete | `docs/authorship_attestation.md` (ICMJE, CRediT, AI disclosure) | Three signatures |
| GPU training runs | Specification complete | Command sequence + acceptance tests in this file | Consented data + GPU |
| Perceptual study | Instrument complete | Protocol, schedule, harness, H2c rule | IRB + 35 participants |
| Results in paper | Template complete | Tables 1–2 + contrast statements in `paper/draft.md` | Paste JSON after runs |
| Citation | Complete | `docs/citations.md` (APA + BibTeX) | None |

The research is complete as a reproducible scaffold. Every design decision is
written down, every claim is a falsifiable hypothesis, every candidate asset is
scored, and every ethical constraint is encoded in code and in a signed-document
workflow. What remains is execution.
