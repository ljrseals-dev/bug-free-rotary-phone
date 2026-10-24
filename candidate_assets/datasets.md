# Datasets

All datasets must clear the asset gate in `docs/selection_rubric.md` before use.
**No dataset containing unconsented speech may be used for cloning.**

| Dataset | License | Use | Cloning permitted? | Notes |
|---|---|---|---|---|
| Mozilla Common Voice | CC0 | Design 1 demographic coverage; dialect diversity | Yes, with speaker-level consent terms verified | Demographic metadata is the key asset |
| VCTK | CC BY 4.0 | Design 1 accented English; Design 2 held-out speakers | Yes, attribution required | Multi-speaker, per-speaker licenses |
| LibriTTS-R | CC BY 4.0 | High-quality read speech; base-model sanity checks | Yes, attribution required | Do not use for released demo audio without consent |
| Harvard sentences (text) | Public domain | Fixed stimulus list for perceptual study | N/A (text only) | Preregistered subset of 12 |

## Inclusion criteria

- Explicit consent terms covering **synthetic voice generation**.
- Per-speaker metadata or speaker-level licensing.
- ≥30 speakers per gender × 2 age bands (Design 1 requirement).
- Height available or inferable (Design 1 anatomical proxy).

## Exclusion criteria

- Any corpus with ambiguous research-use terms.
- Any corpus scraped without per-speaker consent.
- Any corpus whose license forbids derivative synthetic audio.

## Handling

- Raw audio never committed (see `.gitignore`).
- Speaker embeddings treated as sensitive; not released.
- Withdrawal: delete within 30 days and retrain any affected adapter.
