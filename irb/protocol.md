# IRB Protocol — Perceptual Evaluation of Synthetic Inner-Voice and Cloned Speech

## 1. Purpose
Evaluate whether (a) demographic/bone-conduction conditioning improves perceived
self-similarity for inner-voice applications, and (b) LoRA-adapted speech is
perceptually similar to full-fine-tuned speech at 30 s of reference audio.

## 2. Design
Within-subject, randomized, double-blind to condition label. Latin-square order.
N = 35 (Design 1); ≥20 listeners (Design 2). Session ≤40 min with a 2-min break.

## 3. Population
Adults 18+, normal self-reported hearing, English speakers. Excluded: known
auditory processing disorder, prior participation in this study.

## 4. Procedures
1. Consent and demographic form.
2. Headphone check (channel test + 1 kHz reference tone).
3. Practice block (3 trials, not analyzed).
4. Main block: 12 sentences × conditions, 7-pt SSR, 5-pt MOS, 5-pt BCN, forced choice.
5. Debrief and opt-out.

## 5. Risks
Mild: listening to a synthetic approximation of one's own voice may be
unsettling. Mitigation: stop at any time, debrief, no consequence for withdrawal.

## 6. Benefits
None direct. Informs accessible speech technology and responsible voice-AI practice.

## 7. Data
Responses stored with a random participant ID. Audio stimuli are synthesized;
no participant voice is recorded. Deletion on request within 30 days.

## 8. Consent
Written, signed, revocable. See docs/consent_form.md.

## 9. Analysis (preregistered)
Mixed-effects: rating ~ condition + (1|participant) + (1|speaker).
Bonferroni contrasts; Cohen's d with 95% CI. H1b non-inferiority margin 0.3 MOS.
H2c: Pearson r(SECS, SMOS) < 0.6 → SECS reported insufficient alone.

## 10. Deviations
Logged in evaluation/deviations.md with date and reason; reported in the paper.
