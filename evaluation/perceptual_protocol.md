# Perceptual Protocol (Frozen Before Data Collection)

**Applies to:** Design 1 (SSR, MOS, BCN, preference) and Design 2 (SMOS, nMOS).
**Version:** 1.0. Freeze this file with a commit hash before the first participant.

---

## 1. Recruitment

- N = 35 (Design 1), N ≥ 20 listeners (Design 2).
- Balanced across gender and two age bands.
- Screening: normal hearing self-report; no known auditory processing condition.
- Compensation stated up front; withdrawal without penalty.

## 2. Session structure

1. Consent (see `docs/consent_form.md`).
2. Headphone check (channel test + volume calibration to a fixed reference tone).
3. Practice block (3 trials, not analyzed).
4. Main block, randomized order, balanced Latin square across conditions.
5. Debrief and opt-out window.

**Duration:** ≤ 40 minutes. **Breaks:** mandatory 2-minute break at the midpoint.

## 3. Stimuli

- 12 sentences per condition, drawn from a fixed, preregistered list (Harvard sentences subset).
- Normalized to −23 LUFS; no compression beyond loudness normalization.
- Headphones only for the primary analysis.

## 4. Scales

| Scale | Points | Anchors | Used in |
|---|---|---|---|
| SSR | 7 | 1 = "not at all like my inner voice" … 7 = "exactly like my inner voice" | Design 1 |
| MOS | 5 | 1 = "completely unnatural" … 5 = "completely natural" | Both |
| BCN | 5 | 1 = "clearly external" … 5 = "clearly inside my head" | Design 1 |
| SMOS | 5 | 1 = "different speaker" … 5 = "same speaker" | Design 2 |
| Preference | forced choice | A / B / no preference | Design 1 |

## 5. Blinding

- Condition labels replaced with random 6-character codes per participant.
- No condition metadata visible in the playback UI.
- Analyst receives coded data; the key is opened only after the analysis script is committed.

## 6. Analysis

- Linear mixed-effects models: `rating ~ condition + (1 | participant) + (1 | source_speaker)`.
- Pairwise contrasts: Bonferroni-corrected.
- Effect sizes: Cohen's d with 95% CIs.
- Missing data: participants with >20% missing trials excluded and the exclusion reported.

## 7. Deviations

Any deviation from this protocol is logged in `evaluation/deviations.md` with a date and reason,
and reported in the paper.
