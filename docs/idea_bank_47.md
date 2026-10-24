# Idea Bank — 47 Candidate Research Ideas

Scores are 1–5. Higher is better for every column, including risk columns, which are phrased as
**manageability** (5 = low risk, easily mitigated).

**Columns**
- **PR** — patent relevance (does it test a live claim?)
- **OSF** — open-source feasibility (can it run on scored public assets?)
- **EC** — evaluation clarity (are metrics preregisterable?)
- **CC** — compute cost (5 = cheap, ≤1 consumer GPU)
- **LC** — license clarity (5 = permissive throughout)
- **ER** — ethical manageability (5 = low risk, mitigable)
- **NR** — novelty relative to the patents
- **Σ** — total

**Advancement gate:** OSF ≥ 4, EC ≥ 4, LC ≥ 4, ER ≥ 3.
**★** = advanced. **★★** = selected for the two designs.

---

## Family A — Inner-voice / self-perception (8)

| # | Idea | PR | OSF | EC | CC | LC | ER | NR | Σ | |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | Bone-conduction low-shelf + harmonic excitation for TTS | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 33 | ★★ |
| A2 | Demographic FiLM conditioning on a frozen VITS encoder | 5 | 5 | 4 | 5 | 5 | 4 | 4 | 32 | ★★ |
| A3 | Efference-copy timing simulation (delayed self-audio) | 3 | 3 | 3 | 4 | 4 | 3 | 4 | 24 | |
| A4 | Subvocalization-driven TTS from sEMG proxies | 2 | 1 | 2 | 2 | 2 | 2 | 5 | 16 | |
| A5 | Inner-voice naturalness scale (BCN) validation study | 4 | 5 | 5 | 5 | 5 | 5 | 4 | 33 | ★ |
| A6 | Reverberation-free constraint test (patent-implied) | 4 | 5 | 4 | 5 | 5 | 5 | 3 | 31 | ★ |
| A7 | Closed-loop iterative refinement simulation | 4 | 3 | 3 | 3 | 4 | 3 | 3 | 23 | |
| A8 | Cross-language inner-voice perception | 3 | 4 | 3 | 4 | 4 | 4 | 4 | 26 | |

## Family B — Low-resource cloning (12)

| # | Idea | PR | OSF | EC | CC | LC | ER | NR | Σ | |
|---|---|---|---|---|---|---|---|---|---|---|
| B1 | LoRA@30 s vs. full FT on VoxCPM1.5 | 5 | 5 | 5 | 4 | 5 | 3 | 4 | 31 | ★★ |
| B2 | Reference-duration ablation 10/20/30 s | 4 | 5 | 5 | 4 | 5 | 3 | 4 | 30 | ★★ |
| B3 | SECS–SMOS correlation study | 3 | 5 | 5 | 5 | 5 | 5 | 4 | 32 | ★ |
| B4 | Zero-shot vs. LoRA vs. full FT three-way | 5 | 5 | 5 | 3 | 5 | 3 | 3 | 29 | ★ |
| B5 | Cross-lingual speaker transfer under LoRA | 4 | 4 | 4 | 3 | 4 | 3 | 4 | 26 | |
| B6 | Adapter composition (speaker × language) | 3 | 3 | 4 | 3 | 4 | 3 | 5 | 25 | |
| B7 | Quantized (QLoRA) cloning on 8 GB GPU | 4 | 4 | 4 | 5 | 4 | 3 | 4 | 28 | |
| B8 | Adapter size vs. similarity Pareto frontier | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 27 | |
| B9 | Speaker-embedding baking ablation | 4 | 4 | 4 | 4 | 4 | 3 | 4 | 27 | |
| B10 | Partially trained checkpoint truncation study | 5 | 3 | 3 | 3 | 3 | 3 | 4 | 24 | |
| B11 | Noisy-reference robustness (SNR sweep) | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 27 | |
| B12 | CPU-only cloning on VITS-evo ONNX | 4 | 5 | 4 | 5 | 5 | 4 | 3 | 30 | ★ |

## Family C — Evaluation science (9)

| # | Idea | PR | OSF | EC | CC | LC | ER | NR | Σ | |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Adversarial speaker probes for SECS | 2 | 4 | 5 | 5 | 5 | 5 | 4 | 30 | ★ |
| C2 | Long-form perceptual drift in cloning | 2 | 4 | 4 | 4 | 4 | 5 | 4 | 27 | |
| C3 | Listener-panel size vs. MOS stability | 2 | 5 | 5 | 5 | 5 | 5 | 3 | 30 | ★ |
| C4 | MCD / F0 RMSE vs. perceptual measures | 3 | 5 | 5 | 5 | 5 | 5 | 3 | 31 | ★ |
| C5 | Composite scoring formula replication | 3 | 5 | 5 | 5 | 5 | 5 | 3 | 31 | ★ |
| C6 | Headphone vs. speaker presentation effects | 3 | 4 | 4 | 4 | 4 | 4 | 3 | 26 | |
| C7 | Test–retest reliability of SSR | 3 | 5 | 4 | 5 | 5 | 5 | 4 | 31 | ★ |
| C8 | Cross-lingual MOS rater effects | 2 | 3 | 3 | 3 | 4 | 4 | 3 | 22 | |
| C9 | SECS under codec compression | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 27 | |

## Family D — Ethics and provenance (10)

| # | Idea | PR | OSF | EC | CC | LC | ER | NR | Σ | |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 | Consent-tier enforcement in cloning pipelines | 3 | 4 | 4 | 5 | 4 | 5 | 4 | 29 | |
| D2 | Watermark robustness to LoRA fine-tuning | 3 | 4 | 4 | 4 | 4 | 5 | 5 | 29 | |
| D3 | Synthetic-speech detection after adaptation | 3 | 4 | 4 | 3 | 4 | 5 | 5 | 28 | |
| D4 | Withdrawal / unlearning from adapters | 3 | 3 | 3 | 3 | 4 | 5 | 5 | 26 | |
| D5 | Provenance manifests for released adapters | 2 | 5 | 3 | 5 | 5 | 5 | 4 | 29 | |
| D6 | Consent-form comprehension study | 2 | 5 | 3 | 5 | 5 | 5 | 4 | 29 | |
| D7 | NO FAKES Act compliance checklist | 3 | 5 | 3 | 5 | 5 | 5 | 3 | 29 | |
| D8 | Adapter fingerprinting for takedowns | 3 | 3 | 3 | 4 | 4 | 5 | 4 | 26 | |
| D9 | Misuse red-team of released configs | 3 | 4 | 3 | 4 | 4 | 4 | 4 | 26 | |
| D10 | Listener trust vs. synthetic disclosure | 2 | 4 | 4 | 5 | 5 | 5 | 4 | 29 | |

## Family E — Application domains (8)

| # | Idea | PR | OSF | EC | CC | LC | ER | NR | Σ | |
|---|---|---|---|---|---|---|---|---|---|---|
| E1 | Dysphonia voice banking prototype | 3 | 3 | 3 | 3 | 3 | 3 | 5 | 23 | |
| E2 | Inner-voice prosthetics for aphasia | 4 | 2 | 2 | 3 | 2 | 2 | 5 | 20 | |
| E3 | Language-learning pronunciation cloning | 2 | 4 | 4 | 4 | 4 | 3 | 3 | 24 | |
| E4 | Audiobook narration consistency | 2 | 4 | 4 | 4 | 3 | 3 | 3 | 23 | |
| E5 | Accessibility TTS for reading apps | 2 | 5 | 4 | 5 | 4 | 4 | 2 | 26 | |
| E6 | Low-resource language voice preservation | 3 | 3 | 3 | 3 | 3 | 3 | 4 | 22 | |
| E7 | Podcast voice-consistency tooling | 2 | 4 | 3 | 4 | 3 | 3 | 2 | 21 | |
| E8 | Assistive inner-voice reading for dyslexia | 4 | 3 | 3 | 4 | 3 | 3 | 4 | 24 | |

---

## Selection summary

**Advanced (★):** A1, A2, A5, A6, B1, B2, B3, B4, B12, C1, C3, C4, C5, C7.

**Selected (★★):**

- **Design 1** = A1 + A2 (+ A5/A6 protocols folded into evaluation)
- **Design 2** = B1 + B2 (+ B3 correlation analysis folded into evaluation)

### Why this pair

1. Both clear the gate comfortably and score ≥31 total.
2. They are **methodologically complementary**: one is perceptual (human ratings as the primary
 outcome), the other is efficiency-oriented (embedding metrics plus compute accounting).
3. They cover **both anchor patents** without diluting either.
4. They share infrastructure: one perceptual harness, one embedding harness, one scoring rubric.
5. They are executable on ≤1 consumer GPU each — no cluster required.

### Deprioritized and why

- **A4, E2** — require new sensor or clinical data collection; out of scope and high ethical load.
- **B10** — "partially trained" is under-specified in the public record; would need
 checkpoints we cannot obtain, so B1's LoRA-on-base is the defensible stand-in.
- **C8** — cross-lingual rater effects are a study of listeners, not of voice systems.
