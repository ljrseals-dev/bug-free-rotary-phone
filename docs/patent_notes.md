# Patent Notes

Working notes on the two anchor patents and the surrounding landscape.
Patent status is as-of the dossier date; verify before relying on it.

---

## US12614539B1 — Personalized Inner Voice Synthesis

| Field | Value |
|---|---|
| Assignee | Randolph Ventures LLC |
| Filed | 2025-12-08 |
| Published | 2026-04-28 |
| Estimated expiration | 2045-12-08 |
| Status | Active |

### Problem stated

Conventional speech generation omits **bone-conducted low-frequency components**. The result is a
perceptual mismatch: an external voice does not match the voice a person "hears" internally, and
can be rejected as not-self or not-trustworthy.

### Claimed method

1. Generate a provisional voice clone from a recording.
2. Apply a **frequency shift** to compensate for the absent bone-conducted low-frequency adjustment.
3. Use a trained AI model to predict additional acoustic-parameter adjustments
 (formant structure, spectral envelope, prosodic patterns), conditioned on:
 - demographic factors,
 - anatomical factors,
 - content factors,
 - environment factors.
4. **Iteratively refine** the clone using user feedback until it aligns with the speaker's
 self-perceived inner voice.

### What we test vs. what we defer

| Patent element | Our treatment | Rationale |
|---|---|---|
| Bone-conduction compensation | **Tested** — differentiable low-shelf + harmonic excitation | This is the core acoustic claim |
| Demographic conditioning | **Tested** — FiLM adapter on demographic vectors | Directly claimable, cheap to implement |
| Anatomical conditioning | **Proxy tested** — vocal-tract-length estimate from self-reported height | Avoids collecting medical data |
| Iterative user feedback | **Deferred** — replaced by one-shot perceptual evaluation of 3 profiles | Product-grade loop; not needed to test the acoustic mechanism |

### Falsifiable hypotheses derived

- **H1a:** DACA + bone conduction > baseline on SSR (7-point), p < .05, mixed-effects.
- **H1b:** Non-inferiority on MOS, margin 0.3.
- **H1c (exploratory):** Preference gain holds for inner-monologue framing but not for
 external-playback framing.

### Prior-art notes

Bone-conduction transfer functions are well established in acoustics (see skull-vibration
literature). The novelty in the patent is the **application to inner-voice synthesis with
closed-loop user refinement**, not the filter itself. This matters for our framing: we test the
application, not the acoustics.

---

## US20250349282A1 — Voice Cloning with Incompletely Trained TTS Models

| Field | Value |
|---|---|
| Assignee | Microsoft Technology Licensing LLC |
| Filed | 2022-04-13 (PCT/CN2022/086591) |
| Published | 2025-11-13 |
| Status | Pending |

### Problem stated

Conventional TTS requires **large amounts of labeled training data** for personalization.
High-quality synthesis for a new speaker is therefore expensive.

### Claimed method

A zero-shot personalized TTS model with three components:

1. **Feature extractor** — acoustic and prosodic features from new target reference speech.
2. **Speaker encoder** — speaker embedding from those acoustic features.
3. **TTS module** — generates personalized voice from the speaker embedding and prosodic
 features **without applying the TTS module on new labeled training data**.

Claimed benefits: reduced training compute and latency; cross-lingual voice cloning; natural
speech for new speakers without new labeled data.

### What we test

The patent's efficiency claim is broad ("incompletely trained"). We test a **harsher, more
practical variant**:

> LoRA adaptation of a base checkpoint with **30 s** of consented speech reaches **≥0.9×** the
> SECS of full fine-tuning at **≤20%** of the GPU-hours.

We also add what patent language typically omits: **the SECS–SMOS correlation**, reported openly.

### Falsifiable hypotheses derived

- **H2a:** SECS(LoRA@30s) ≥ 0.9 × SECS(full FT).
- **H2b:** GPU-hours(LoRA) ≤ 0.2 × GPU-hours(full FT); trainable params ≤ 0.3 × total.
- **H2c:** corr(SECS, SMOS) ≥ 0.6; if not, SECS alone is flagged insufficient for this config.

---

## Landscape context (not tested here)

| Publication | Holder | Relevance |
|---|---|---|
| US12620386B1 | IncentMed IP LLC | Personalized speech via adaptive excitation signal generation |
| CN121838730A | Xi'an Univ. of Tech. | Tacotron2 + BERT for long-text personalized speech |
| WO2023197206A1 | Microsoft | PCT parent of US20250349282A1 |

These confirm that personalization and low-resource adaptation are crowded patent territory. That
strengthens the case for an **open, benchmark-driven counterpoint**: published protocols, scored
candidates, and honest negative results.

---

## Standing caveats

- Patent claims describe systems; they are not evidence of performance.
- Public implementation details are rarely available; our designs use the closest open analogs.
- Nothing here is legal advice. Consult counsel before commercial use of any patented method.
