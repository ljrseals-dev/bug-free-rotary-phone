# Speaker Similarity and Efficiency Metrics

## 1. SECS (primary objective metric)

- **Primary encoder:** ECAPA-TDNN speaker verification model.
- **Replication encoder:** Resemblyzer.
- **Procedure:** embed reference audio and synthesized audio; compute cosine similarity;
  average over 12 utterances per condition.
- **Report:** mean, SD, 95% CI, and per-speaker breakdown.

**Known limitation:** SECS measures similarity to a verification model's notion of speaker
identity, not perceptual identity. It can be high for voices humans judge distinct.
Hence H2c: we require corr(SECS, SMOS) ≥ 0.6 or we downgrade the claim.

## 2. MCD

- Mel-cepstral distortion, 25-order MFCC, DTW-aligned to the reference.
- Reported as a secondary faithfulness measure, not a primary outcome.

## 3. F0 RMSE

- Log-F0 RMSE over voiced frames, after octave-error correction.
- Reported per condition; used to check that prosody is not collapsed by adaptation.

## 4. Efficiency accounting

| Metric | How measured |
|---|---|
| GPU-hours | Wall-clock × GPU count, logged per run |
| Peak VRAM | `torch.cuda.max_memory_allocated()` |
| Trainable params | Count of `requires_grad=True` tensors |
| RTF | Synthesis wall-clock ÷ audio duration, 30-utterance mean |

## 5. Composite reporting

We do **not** collapse to a single composite score in the primary analysis. A composite is
reported only as a secondary summary, using the published weighting
`0.4 × SMOS + 0.3 × MOS + 0.3 × (100 − WER)`, and is clearly labeled as post hoc.

## 6. Correlation analysis

- Pearson and Spearman between SECS and SMOS, pooled and per condition.
- Scatter plot with per-condition colors; regression line with 95% CI band.
- Pre-registered decision: if r < 0.6, the paper reports SECS as **insufficient alone**.
