# Patent-to-Benchmark Voice-AI Research

> **Status:** Execution-ready dossier (v0.1).
> **Authorship:** Provisional. The author line below is a draft placeholder and is
> **not** an assertion that the named individuals wrote, approved, or endorse this work.
> Written consent must be obtained before any public release.

Two scaffolded research designs selected from a bank of **47 candidate ideas** using the
Research Scaffolding method:

> **Search widely → evaluate candidates → adapt rather than reinvent → justify implementation.**

The designs translate recent AI voice patent claims into reproducible,
open-source-first benchmarks:

1. **Demographic-Aware "Inner Voice" Synthesis** — informed by `US12614539B1` (Randolph Ventures LLC).
2. **Efficient Few-Shot Voice Cloning with Incompletely Trained TTS Models** — informed by `US20250349282A1` (Microsoft Technology Licensing LLC).

No affiliation with, or endorsement by, either patent holder is implied.

## Authors (provisional — consent pending)

- Lewis Seals
- Lilibet Diana Windsor
- Alexandria Ocasio-Cortez

## Research questions

**Design 1.** Can demographic/anatomical conditioning plus simulated bone conduction improve
perceived self-similarity for inner-monologue applications over a strong generic TTS baseline,
without a meaningful naturalness loss?

**Design 2.** Can LoRA fine-tuning of a partially trained TTS checkpoint, using ~30 s of target-speaker
data, approach full fine-tuning in speaker similarity and naturalness at ≤20% of the GPU-hours?

## How this research is different

- **Tests patent claims rather than restating them.** Each claim is converted into a falsifiable
  hypothesis with preregistered metrics and explicit baselines.
- **Searches widely before building.** Datasets, checkpoints, and libraries are inventoried and
  scored on a seven-criterion rubric before implementation begins.
- **Adapts existing models.** Novelty lives in conditioning, adaptation, and evaluation — not in
  rebuilding a TTS stack from zero.
- **Dual evaluation.** Human perceptual ratings are paired with speaker-embedding metrics; a low
  SECS–SMOS correlation is treated as a finding, not hidden.
- **Ethics as a design constraint.** Written consent, tiered release, and no-release rules for
  baked speaker identities, aligned with the NO FAKES Act (2026) framework.

## Repository layout

```
.
├── docs/                # patent notes, 47-idea bank, rubric, ethics, consent,
│                        # authorship attestation, citations, execution spec
├── designs/             # two full research designs
├── evaluation/          # perceptual protocol, similarity metrics, scorecards
├── candidate_assets/    # scored datasets, checkpoints, libraries
├── paper/draft.md       # full manuscript draft + results template
├── configs/             # runnable YAML configs for both designs
└── src/                 # reference implementations (completed scaffolding)
```

## Quickstart

1. Read `docs/selection_rubric.md` and `docs/idea_bank_47.md`.
2. Read both files in `designs/`.
3. Complete `docs/ethics_review.md` and collect `docs/consent_form.md` **before** any cloning run.
4. Populate `candidate_assets/` scores from `evaluation/scorecards/`.
5. Adapt `configs/*.yaml` and run the reference scripts in `src/` (scaffolding only).
6. Record results back into `paper/draft.md`.

## Evaluation metrics

| Design | Primary | Secondary |
|---|---|---|
| 1 — Inner voice | Self-Similarity Rating (SSR, 7-point) | MOS, preference rate, Bone-Conduction Naturalness (BCN) |
| 2 — Cloning | SECS (ECAPA-TDNN / Resemblyzer) | SMOS, nMOS, GPU-hours, peak memory, trainable params |

## Candidate scoring rubric (7 criteria, 1–5 each)

Maintenance · License · Real usage · Dependencies · Security · Fit · Documentation.

Selection gate for advancement: **≥4** on open-source feasibility, evaluation clarity, and license
clarity; **≥3** on ethical manageability.

## Ethics and safety

- Voice cloning requires **explicit written consent** and disclosure.
- **Do not release baked speaker models.** Release adapters, configs, and consented synthetic
  evaluation audio only.
- Watermark or clearly label all synthetic outputs.
- Honor withdrawal requests: delete raw audio and derived embeddings within 30 days.
- Review every dataset, checkpoint, and library license before use.

## Roadmap

- [x] 47-idea bank and selection rubric
- [x] Candidate asset scoring (VoxCPM1.5, VITS-evo, mlx-audio-train)
- [x] Ethics review and consent form drafts
- [x] Design 1 DACA + bone-conduction implementation (`src/`, `configs/`)
- [x] Design 2 LoRA pipeline on VoxCPM1.5 (native `ref_audio` path)
- [x] Perceptual + embedding evaluation instruments (protocol + `evaluate_secs.py`)
- [x] Results template folded into `paper/draft.md`
- [x] Authorship attestation workflow (`docs/authorship_attestation.md`)
- [x] Citation block + BibTeX (`docs/citations.md`)
- [x] Execution specification for remaining human/GPU steps (`docs/execution_spec.md`)
- [ ] Author signatures (three human signatures required)
- [ ] GPU training runs (requires consented data + hardware)
- [ ] Human perceptual study (requires IRB + participants)

## Citation

See `CITATION.cff`. Until authorship is confirmed, cite as an unpublished draft.

## License

Code: MIT (see `LICENSE`). Prose and figures: CC BY 4.0.
Third-party models and datasets retain their own licenses — see `candidate_assets/`.
