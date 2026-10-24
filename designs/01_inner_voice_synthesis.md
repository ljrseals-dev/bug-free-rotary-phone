# Design 1 — Demographic-Aware "Inner Voice" Synthesis

**Informed by:** US12614539B1 (Randolph Ventures LLC)
**Idea bank entries:** A1 (bone conduction) + A2 (demographic conditioning), with A5/A6
protocols folded into evaluation.
**Status:** Specification complete; implementation pending.

---

## 1. Hypotheses

- **H1a (primary).** A TTS model conditioned on demographic vectors and a simulated
  bone-conduction filter produces higher **Self-Similarity Rating (SSR)** than a strong generic
  TTS baseline, p < .05 in a mixed-effects model.
- **H1b (secondary).** The conditioned model is **non-inferior** on naturalness MOS, margin 0.3.
- **H1c (exploratory).** The SSR gain is larger under an inner-monologue framing than under an
  external-playback framing.

## 2. Construct operationalization

| Patent construct | Operationalization | Justification |
|---|---|---|
| Bone-conducted low-frequency components | Differentiable low-shelf (200–500 Hz cutoff, learned gain) + harmonic excitation at F0 multiples < 500 Hz, applied pre-vocoder | Direct analogue of the patent's frequency shift |
| Demographic data | Age band (8-d), gender (4-d), dialect region (16-d) embeddings | Matches patent's demographic conditioning |
| Anatomical data | Vocal-tract-length proxy from self-reported height (1-d, normalized) | Minimally invasive; avoids medical data |
| Iterative user feedback | Deferred; replaced by one-shot comparison of 3 conditioning profiles | Tests the acoustic mechanism first |

## 3. Data

**No new voice data is collected for model training.** Reuse scored corpora only:

| Corpus | License | Role |
|---|---|---|
| Mozilla Common Voice | CC0 | Demographic coverage, dialect diversity |
| VCTK | CC BY 4.0 | Accented English, multi-speaker |
| LibriTTS-R | CC BY 4.0 | High-quality read speech for base-model sanity checks |

**Inclusion:** ≥30 speakers per gender × 2 age bands; height available or inferable.
**Exclusion:** any corpus without explicit consent terms for synthetic voice research.

## 4. Model

**Base:** VITS-evo (Apache 2.0, ONNX, 31M params, ~0.18 RTF on CPU). Chosen for license clarity
and CPU feasibility; VoxCPM1.5 is held as a quality-ceiling replication target.

**Novel module — DACA (Demographic-Anatomical Conditioning Adapter):**
- Small MLP, ≈2M params, inserted between the text encoder and the duration predictor.
- Input: concatenated `[age(8) ‖ gender(4) ‖ dialect(16) ‖ VTL(1)]` → 29-d vector.
- Output: FiLM-style per-channel `(γ, β)` applied to encoder hidden states.
- Base VITS weights **frozen**; only DACA + filter parameters train.

**Bone-conduction module:** see `src/bone_conduction.py`. Differentiable, 3 parameters
(shelf cutoff, shelf gain, harmonic mix).

**Training objective:**
`L = L_mel + λ1 · L_speaker_embed + λ2 · L_filter_reg`
where `L_speaker_embed` is cosine distance between generated and reference speaker embeddings
(the "self-similarity proxy"), and `L_filter_reg` keeps the shelf gain in a plausible range.

**Config:** `configs/design1_daca.yaml`.

## 5. Perceptual study

**Design:** within-subject, 4 conditions, randomized order, blind labels.

| Condition | DACA | Bone conduction |
|---|---|---|
| C0 — Baseline | ✗ | ✗ |
| C1 — DACA only | ✓ | ✗ |
| C2 — Full model | ✓ | ✓ |
| C3 — Recorded inner speech (anchor, optional) | — | — |

**Participants:** N = 35 (target), balanced gender and age band.

**Measures:**
- **SSR** — 7-point Likert: "How much does this sound like the voice you hear when you read silently?"
- **MOS** — 5-point naturalness.
- **BCN** — 5-point: "Does this sound like it comes from inside your head?"
- **Preference** — forced choice, C2 vs. C0.

**Presentation:** headphones only for primary analysis; a speaker-playback arm is run as a
secondary check and reported separately.

**Analysis:** linear mixed-effects, random intercepts for participant and source speaker,
Bonferroni-corrected pairwise contrasts across C0/C1/C2.

**Power:** N = 35, within-subject r = 0.5 → 80% power to detect d = 0.5 (α = .05, two-tailed).

**Preregistration:** `evaluation/perceptual_protocol.md` is frozen before data collection.

## 6. Success criteria

- H1a supported: C2 > C0 on SSR with p < .05 and effect size d ≥ 0.4.
- H1b supported: C2 MOS ≥ C0 MOS − 0.3.
- Either way, per-group SSR is reported to check for demographic stereotyping (risk R4).

## 7. Risks

| Risk | Mitigation |
|---|---|
| Bone-conduction sim sounds unnatural on external playback | Headphones-only primary analysis; separate speaker arm |
| Demographic conditioning encodes stereotypes | Demographic vectors as controls; per-group reporting; no "typical voice" generation |
| Participants lack a stable inner-voice percept | Pre-screening task; anchor condition; report exclusion rate |
| Base model quality ceiling (VITS-evo) | Pre-specified replication on VoxCPM1.5 if budget allows |

## 8. Deliverables

- `src/daca_adapter.py`, `src/bone_conduction.py`
- `configs/design1_daca.yaml`
- Frozen protocol + result tables
- Tier-2 consented synthetic examples (if consent allows)
