# Design 2 — Efficient Few-Shot Voice Cloning

**Informed by:** US20250349282A1 (Microsoft Technology Licensing LLC)
**Idea bank entries:** B1 (LoRA@30 s) + B2 (duration ablation), with B3 (SECS–SMOS correlation)
folded into evaluation.
**Status:** Specification complete; implementation pending.

---

## 1. Hypotheses

- **H2a (primary).** LoRA fine-tuning with 30 s of target-speaker data achieves
 **SECS ≥ 0.9 ×** the SECS of full fine-tuning on the same 30 s.
- **H2b (secondary).** LoRA uses **≤20%** of the GPU-hours and **≤30%** of the trainable
 parameters of full fine-tuning.
- **H2c (exploratory).** corr(SECS, SMOS) ≥ 0.6. If not, SECS alone is flagged insufficient
 for this configuration.

## 2. Why this is a stricter test than the patent

The patent claims zero-shot personalization **without labeled training data** on the new speaker.
Our design tests a **harsher, more practical** budget: a tiny labeled set (30 s) plus an
adapter. This probes the efficiency frontier of the same underlying idea and produces numbers
that downstream practitioners can actually use.

## 3. Candidate assets (scored)

| Asset | License | Role | Scorecard |
|---|---|---|---|
| **VoxCPM1.5** (OpenBMB) | Apache 2.0 | Primary base: native LoRA + SFT, 44.1 kHz, RTF ~0.17 on RTX 4090 | `evaluation/scorecards/voxcpm15.md` |
| **VITS-evo** (ZDisket) | Apache 2.0 / MIT components | CPU baseline; zero-shot only; 31M params, RTF ~0.18 on CPU | `evaluation/scorecards/vitsevo.md` |
| **mlx-audio-train** (akashicMarga) | Check repo | Methodological blueprint for speaker-embedding injection + LoRA | `evaluation/scorecards/mlx_audio_train.md` |

**Decision:** VoxCPM1.5 is primary (strong cloning + native LoRA). VITS-evo is the
compute-efficient secondary. The **method** from mlx-audio-train Pipeline 2 (speaker embedding
as positional token in codec prefix) is ported to VoxCPM1.5 on CUDA hardware.

## 4. LoRA configuration

| Parameter | Value | Source |
|---|---|---|
| Rank | 16 | mlx-audio-train speaker-cloning guidance (rank 16 for speaker, vs. rank 8 for language) |
| Target modules | Attention + MLP in the talker transformer | mlx-audio-train Pipeline 2 |
| Epochs | 3 | mlx-audio-train Pipeline 2 |
| Batch size | 16 | mlx-audio-train Pipeline 2 |
| Speaker conditioning | Speaker embedding from reference mel, injected as a positional token in the codec prefix | mlx-audio-train Pipeline 2 |
| Data | 3 × 10 s clips = 30 s, plus a held-out 10 s eval clip | Design choice |

**Post-training:** **Do not** bake speaker embeddings into a released artifact. Averaging and
baking is a deployment convenience; it creates an irreversible identity artifact. We evaluate
the baked path internally and release only the adapter.

## 5. Conditions

| Condition | Data | Trainable | Purpose |
|---|---|---|---|
| Z0 — Zero-shot | reference clip only | none | Lower bound |
| L10 — LoRA @ 10 s | 10 s | ~2–4% | Duration ablation |
| L20 — LoRA @ 20 s | 20 s | ~2–4% | Duration ablation |
| **L30 — LoRA @ 30 s** | 30 s | ~2–4% | **Primary condition** |
| F30 — Full FT @ 30 s | 30 s | 100% | Upper reference |
| P — Published baseline | — | — | External comparison (CosyVoice / VALL-E 2 figures) |

**Reference-duration rationale:** 2026 controlled studies report similarity rising with reference
length with diminishing returns beyond ~20 s. The 10/20/30 s sweep maps our results onto that curve.

## 6. Metrics

**Objective:**
- **SECS** — cosine similarity via ECAPA-TDNN (primary) and Resemblyzer (replication).
- **MCD** — mel-cepstral distortion.
- **F0 RMSE** — prosody faithfulness.
- **Efficiency** — GPU-hours, peak VRAM, trainable parameter count, RTF.

**Subjective:**
- **SMOS** — 5-point similarity MOS.
- **nMOS** — 5-point naturalness MOS.
- **Protocol** — ≥20 listeners, ≥40 stimuli each, blind randomized playback.

**Success criteria:** SECS(L30) ≥ 0.9 × SECS(F30) **and** GPU-hours(L30) ≤ 0.2 × GPU-hours(F30).

## 7. Analysis plan

1. Report SECS/SMOS/nMOS with 95% CIs for every condition.
2. Fit a monotone curve of SECS vs. reference duration (10/20/30 s) and compare slope to the
 published duration–similarity curve.
3. Compute Pearson and Spearman corr(SECS, SMOS) pooled across conditions; report per-condition
 correlations as well.
4. If H2c fails (r < 0.6), report that SECS is **not** a sufficient proxy for this configuration
 and downgrade the primary metric claim accordingly.

## 8. Risks

| Risk | Mitigation |
|---|---|
| 30 s insufficient for stable LoRA | Report 10/20/30 s learning curves; 30 s is primary, not sole |
| SECS overstates perceptual similarity | Every SECS result paired with SMOS; correlation reported |
| Base-model license restricts cloning | Scored before training (Apache 2.0 ✓); no run until gate passes |
| Baked embeddings create irreversible identity artifact | Never released; adapter-only release policy |
| Hardware mismatch (mlx-audio-train targets Apple Silicon) | Port the method, not the code; validate on VoxCPM1.5 + CUDA |

## 9. Deliverables

- `src/lora_cloning.py`, `src/evaluate_secs.py`
- `configs/design2_lora.yaml`
- Result tables (SECS, SMOS, nMOS, GPU-hours, params)
- Adapter release only if all consent tiers permit
