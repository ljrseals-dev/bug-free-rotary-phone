# From Patent Claims to Reproducible Voice-AI Research: Two Adapter-First Designs for Inner-Voice Synthesis and Low-Resource Voice Cloning

**Author:** Lewis Seals Jr¹
**Affiliation:** ¹ Independent Researcher (provisional)
**Status:** Draft. Authorship, affiliation, and consent unconfirmed.

**Dedication:** *Soli Deo Gloria.*
**No endorsement by the named individuals or by either patent holder is implied.**

---

## Abstract

Patent filings increasingly define the functional boundaries of AI voice systems, yet their
claims are rarely translated into reproducible benchmarks. We present two research designs
selected from a bank of 47 candidate ideas using a scaffolded search–evaluate–adapt methodology.
Design 1 tests whether demographic- and anatomy-conditioned text-to-speech with simulated bone
conduction improves perceived self-similarity for inner-voice applications, informed by
US12614539B1. Design 2 tests whether LoRA fine-tuning of a partially trained TTS checkpoint with
30 seconds of speaker data approaches full fine-tuning in speaker similarity and naturalness,
informed by US20250349282A1. We contribute (i) a patent-to-benchmark translation method, (ii) a
scored candidate-asset protocol covering VoxCPM1.5, VITS-evo, and mlx-audio-train, (iii) paired
perceptual and embedding-based evaluation frameworks, and (iv) an ethics-first execution dossier
aligned with the NO FAKES Act of 2026. Our research differs from prior work by treating patent
claims as hypotheses rather than descriptions, and by requiring open-source adaptation rather
than from-scratch construction.

**Keywords:** voice cloning, text-to-speech, inner voice, bone conduction, LoRA, patent analysis

---

## 1. Introduction

Voice-AI research is shaped by three forces: patent claims, open-source checkpoints, and
regulatory pressure. Patents describe broad functional systems — personalized inner-voice
synthesis, zero-shot cloning without new labeled data. Repositories provide concrete but uneven
implementations. Regulators, most visibly in the 2026 NO FAKES Act, demand consent, traceability,
and takedown mechanisms for digital replicas.

Research that ignores any one of these forces is respectively irreproducible, unlicensed, or
irresponsible. This paper sits at the intersection. We take two recent patents and convert their
claims into testable designs, selected from a 47-idea bank by explicit scoring rather than
convenience.

Our two designs are deliberately complementary: one is perceptual (human ratings as the primary
outcome), the other is efficiency-oriented (embedding metrics plus compute accounting). Both are
executable on a single consumer GPU. Both freeze or minimally modify existing open-source models.

## 2. Related work and patent landscape

Prior voice-cloning research has concentrated on architecture and quality. The patents we study
add two different emphases: self-perception (the inner voice) and data efficiency (incompletely
trained models).

Open-source TTS has advanced quickly. VoxCPM1.5 offers native LoRA and zero-shot cloning under
Apache 2.0 at ~0.17 RTF on an RTX 4090. VITS-evo provides ONNX-based zero-shot cloning at
~0.18 RTF on CPU with a permissive license stack and ~31M parameters. The mlx-audio-train
project documents a speaker-cloning pipeline that injects speaker embeddings as a positional
token in the codec prefix and adapts the model with LoRA.

Evaluation science has converged on speaker-encoder cosine similarity (SECS) and mean opinion
scores (MOS/SMOS). Controlled 2026 studies report that similarity rises with reference-audio
duration with diminishing returns beyond roughly 20 seconds, and composite scoring formulas have
been proposed (e.g., 0.4 × SMOS + 0.3 × MOS + 0.3 × (100 − WER)).

Adjacent filings — adaptive excitation for personalized speech (US12620386B1) and long-text
personalization (CN121838730A) — confirm that personalization is crowded IP territory. What is
missing is a patent-to-benchmark bridge under explicit ethical constraints. This paper supplies
one.

## 3. Method: scaffolded selection from 47 ideas

The 47 ideas are organized into five families: inner-voice/self-perception (8), low-resource
cloning (12), evaluation science (9), ethics/provenance (10), and application domains (8). Each
is scored 1–5 on seven criteria: patent relevance, open-source feasibility, evaluation clarity,
compute cost, license clarity, ethical manageability, and novelty relative to the patents.

The advancement gate requires open-source feasibility, evaluation clarity, and license clarity
≥4 and ethical manageability ≥3. Fourteen ideas clear the gate. The two selected designs score
highest on the conjunction of feasibility, evaluation clarity, and license clarity, and are
methodologically complementary.

Scoring is auditable: two reviewers score independently, disagreements of ≥2 points are
discussed and re-scored, and the lower final score is recorded.

## 4. Design 1: demographic-aware inner-voice synthesis

**Hypothesis.** DACA conditioning plus bone-conduction simulation increases Self-Similarity
Rating (SSR) over a generic TTS baseline without a meaningful naturalness loss
(non-inferiority margin 0.3 MOS).

**Model.** We adapt VITS-evo, freezing base weights. A ≈2M-parameter
Demographic-Anatomical Conditioning Adapter takes a 29-dimensional vector (age band, gender,
dialect region, vocal-tract-length proxy) and emits FiLM parameters applied to the text encoder.
A differentiable bone-conduction module applies a learned low-shelf filter plus harmonic
excitation below 500 Hz before the vocoder. The 30-iteration feedback loop claimed in the patent
is deliberately out of scope; we test the acoustic mechanism first.

**Data.** Common Voice, VCTK, and LibriTTS-R — no new voice data is collected for training.

**Study.** Within-subject, N = 35, four conditions (baseline; DACA only; full model; recorded
inner speech as optional anchor), randomized and blind. Headphones only for the primary
analysis. Linear mixed-effects models with Bonferroni-corrected contrasts.

**Contribution relative to the patent.** We isolate the acoustic claim from the interaction
claim, providing the first independent test of the core mechanism described in US12614539B1.
We also report per-demographic-group results to detect stereotyping.

## 5. Design 2: efficient few-shot cloning

**Hypothesis.** LoRA adaptation of VoxCPM1.5 with 30 seconds achieves SECS ≥ 0.9× full
fine-tuning at ≤20% of the GPU-hours.

**Method.** We port the mlx-audio-train speaker-cloning pipeline to VoxCPM1.5 on CUDA hardware:
speaker embedding from reference mel, injected as a positional token in the codec prefix, LoRA
rank 16, 3 epochs, batch 16. We sweep 10/20/30 seconds and compare against zero-shot cloning and
full fine-tuning on the same 30 seconds. Speaker embeddings are baked internally for evaluation
but never released.

**Metrics.** SECS via ECAPA-TDNN (primary) and Resemblyzer (replication); MCD; F0 RMSE; SMOS and
nMOS with ≥20 listeners; GPU-hours, peak VRAM, trainable-parameter count, RTF.

**Contribution relative to the patent.** The Microsoft filing claims zero-shot personalization
without labeled data. We test the efficiency frontier of that idea under a realistic low-resource
budget, and we report the SECS–SMOS correlation that patent language omits.


## 4. Results — Design 1 (inner voice)

**Table 1.** Perceptual ratings by condition (mean ± SD, 95% CI in brackets).

| Condition | SSR (7-pt) | MOS (5-pt) | BCN (5-pt) | Pref. vs C0 |
|---|---|---|---|---|
| C0 Baseline | __ ± __ [__, __] | __ ± __ | __ ± __ | — |
| C1 DACA only | __ ± __ [__, __] | __ ± __ | __ ± __ | __% |
| C2 Full model | __ ± __ [__, __] | __ ± __ | __ ± __ | __% |
| C3 Recorded anchor | __ ± __ [__, __] | __ ± __ | __ ± __ | — |

Mixed-effects contrasts (Bonferroni-corrected):
- C2 − C0 on SSR: β = __, 95% CI [__, __], p = __, d = __.
- Non-inferiority on MOS (margin 0.3): __ (supported / not supported).
- Per-demographic-group SSR: reported in Appendix D; no group deviates by > __ points.

**H1a** __ ; **H1b** __ ; **H1c** __ .

## 5. Results — Design 2 (few-shot cloning)

**Table 2.** Speaker similarity and efficiency by condition.

| Cond. | Ref. (s) | SECS (ECAPA) | SECS (Resemblyzer) | SMOS | nMOS | GPU-h | Peak VRAM | Trainable % |
|---|---|---|---|---|---|---|---|---|
| Z0 | — | __ ± __ | __ ± __ | __ | __ | 0 | __ | 0 |
| L10 | 10 | __ ± __ | __ ± __ | __ | __ | __ | __ | __ |
| L20 | 20 | __ ± __ | __ ± __ | __ | __ | __ | __ | __ |
| **L30** | **30** | **__ ± __** | **__ ± __** | **__** | **__** | **__** | **__** | **__** |
| F30 | 30 | __ ± __ | __ ± __ | __ | __ | __ | __ | 100 |

**H2a:** SECS(L30) / SECS(F30) = __ (criterion ≥ 0.9: __ ).
**H2b:** GPU-h(L30) / GPU-h(F30) = __ (criterion ≤ 0.2: __ );
trainable-parameter ratio = __ (criterion ≤ 0.3: __ ).
**H2c:** Pearson r(SECS, SMOS) = __, p = __ → __ (SECS sufficient / insufficient alone).

**Figure 1.** SECS vs. reference duration (10/20/30 s) with the published
diminishing-returns curve overlaid. Slope comparison: __ .

**Figure 2.** SECS–SMOS scatter, coloured by condition, with regression line and
95% CI band.

---

## 6. How our research is different

**It tests rather than restates.** Each patent claim becomes a falsifiable hypothesis with a
preregistered metric and an explicit baseline. We do not describe the patent; we interrogate it.

**It searches before building.** Every dataset, checkpoint, and library is scored against a
seven-criterion rubric before implementation. The rubric, scorecards, and reviewer disagreements
are part of the record.

**It adapts rather than reinvents.** Both designs freeze or minimally modify public models.
Novelty lives in conditioning (DACA), in adaptation strategy (LoRA vs. full fine-tuning), and in
evaluation (SSR/BCN, SECS–SMOS correlation).

**It evaluates perceptually and computationally.** SECS without SMOS is insufficient; SSR without
a baseline is uninterpretable. We preregister a decision rule: if corr(SECS, SMOS) < 0.6, the
paper reports SECS as insufficient alone.

**It treats ethics as a design constraint.** Written consent, tiered release, adapter-only
publication, and a 30-day withdrawal SLA are part of the method, aligned with the NO FAKES Act's
authorization and takedown framework.

## 7. Ethics and limitations

Voice cloning requires written consent and carries impersonation risk; 2026 policy activity
treats this as a live harm. Our protocol restricts cloning to consenting speakers, releases
adapters rather than identities, labels all synthetic audio, and honors withdrawal within 30
days. Inner-voice synthesis raises psychological-safety questions; the perceptual study
pre-screens participants and allows opt-out at any point.

Limitations. Our base models are open-source analogs, not the systems described in the patents;
patent claims may not map cleanly to public implementation details. Perceptual studies are
small-sample and listener-dependent. The 30-second cloning condition is a deliberately harsh
constraint and may not generalize to larger budgets. DACA uses a height-based proxy for
vocal-tract length, which is coarse. We do not test the patents' iterative feedback loops.

## 8. Conclusion

The two designs show that patent-informed voice-AI research can be reproducible,
open-source-first, and ethically constrained. The next step is execution: populate the candidate
matrices, complete ethics review, train the adapters, and run the perceptual protocols. We
release the rubric, protocols, configs, and reference code so that the results — positive or
negative — can be checked and extended.

---

## Appendix A — Idea bank summary

47 ideas across five families; 14 clear the gate; 2 selected. See `docs/idea_bank_47.md`.

## Appendix B — Asset scorecards

VoxCPM1.5 (30/35), VITS-evo (29/35), mlx-audio-train (26/35, accepted with conditions).
See `evaluation/scorecards/`.

## Appendix C — Reproducibility

Configs in `configs/`, reference code in `src/`, protocols frozen with commit hashes before data
collection.
