cd /home/claude/book && cat > RELEASE_NOTES.md <<'EOF'
# Release Notes

## v0.1.0 — 2026 (source-only; no archive attached)

**Distribution:** Source only. No `.zip`, `.tar`, wheel, or binary is attached to
this release. Clone the repository or download the source tree. Nothing here is
packaged for execution as a distributable artifact.

---

## What's included

### Research dossier
- `paper/draft.md` — sole-authored methods/scaffolding manuscript; results
  sections are fill-in templates, not measured numbers.
- `docs/patent_notes.md` — US12614539B1 and US20250349282A1: claims, what is
  tested vs. deferred, derived falsifiable hypotheses.
- `docs/idea_bank_47.md` — 47 ideas, 5 families, 7-criterion scoring, gate and
  selection rationale.
- `docs/selection_rubric.md` — idea rubric, asset rubric, two-reviewer
  conservative scoring.
- `designs/01_inner_voice_synthesis.md` — Design 1 full specification.
- `designs/02_few_shot_voice_cloning.md` — Design 2 full specification.
- `evaluation/perceptual_protocol.md` — frozen-before-collection protocol.
- `evaluation/speaker_similarity.md` — SECS / MCD / F0 RMSE / efficiency metrics.
- `evaluation/scorecards/` — VoxCPM1.5, VITS-evo, mlx-audio-train.

### Ethics and governance
- `docs/ethics_review.md` — risk register, sign-off table.
- `docs/consent_form.md` — tiered consent, 30-day withdrawal SLA.
- `docs/authorship_attestation.md` — ICMJE + CRediT, **unsigned**.
- `NOTICE.md` — no political affiliation or endorsement; no public official is
  an author, contributor, or endorser.
- `irb/protocol.md`, `irb/submission_checklist.md` — submission-ready drafts.

### Code
- `stereo_cat.py` — M/D stereo-field algebra: band split, cut/rotate/place,
  recipes, per-band report.
- `endless_beats.py` — seeded Euclidean beat grammar and three-voice drum
  renderer.
- `demo.py` — renders a beat and applies example recipes.
- `src/bone_conduction.py` — differentiable low-shelf biquad + harmonic exciter,
  with a scipy cross-check.
- `src/daca_adapter.py` — per-layer FiLM adapter, zero-init, condition dropout,
  frozen-base assertion.
- `src/lora_cloning.py` — VoxCPM1.5 LoRA driver scaffolding, release policy.
- `src/evaluate_secs.py` — ECAPA-TDNN SECS, MCD/F0, SECS–SMOS correlation rule.
- `src/run_design2.py` — training driver that **refuses to run without a signed
  consent record**.

### Tests
- `tests/test_stereo_cat.py` and `tests/test_endless_beats.py`.
- Covers M/D roundtrip, band-weight normalization and validation, split
  reconstruction, operator invariants (rotation preserves M²+D², pan is
  constant-power, diff=0 collapses to mono), Euclidean onset counts against
  known 3-8 / 5-8 / 5-16 patterns, render determinism under a fixed seed, and
  all render validation guards.
- Run: `python3 -m unittest discover -s tests -v`

---

## What is NOT included / not verified

- **No trained models, adapters, or weights.** None are committed or attached.
- **No GPU training runs have been executed.** `src/` modules are reference
  scaffolding; they pass shape and identity sanity checks only.
- **No human perceptual data.** The protocol is frozen and awaits IRB approval
  and participants.
- **No audio evaluation.** Voice output has not been listener-evaluated.
- **No external evaluation or endorsement** by any company, agency, or public
  figure is claimed or implied.
- **No benchmark results.** Every number in `paper/draft.md` is a placeholder.

---

## Known limitations

- Base-model integrations (VoxCPM1.5 API, VITS-evo ONNX graph) must be written
  against pinned revisions before training.
- `src/bone_conduction.py` is validated only against a scipy reference at init;
  perceptual quality is untested.
- DACA uses a height-based proxy for vocal-tract length — coarse by design.
- The 30 s cloning condition is deliberately harsh; results may not generalize.
- The perceptual protocol is small-sample (N=35) and listener-dependent.

---

## Upgrade / compatibility notes

- Python 3.9+ for `stereo_cat.py` and `endless_beats.py` (numpy only).
- `src/` modules additionally assume `torch`, `torchaudio`, `speechbrain`,
  `resemblyzer`, `scipy`, `soundfile` — none are vendored.
- Pin base-model revisions in `configs/*.yaml` before any run. Floating `main`
  is not supported.

---

## Ethics

Voice cloning requires written consent. No baked speaker models are released at
any consent tier. See `docs/ethics_review.md` and `NOTICE.md`.

## License

Code: MIT. Prose and figures: CC BY 4.0. Third-party models and datasets retain
their own licenses.
EOF
cat > CHANGELOG.md <<'EOF'
# Changelog

All notable changes are recorded here. Format follows Keep a Changelog;
versioning follows Semantic Versioning.

## [Unreleased]
- Design 1 GPU training run (blocked: consented audio + hardware)
- Design 2 LoRA / full-FT comparison (blocked: same)
- Perceptual study (blocked: IRB + 35 participants)
- Author signature on `docs/authorship_attestation.md`

## [0.1.0] - 2026
### Added
- Two research designs derived from US12614539B1 and US20250349282A1
- 47-idea scored bank and selection rubric
- Patent notes with test-vs-defer table
- Ethics review, tiered consent form, unsigned authorship attestation
- NOTICE.md: no political affiliation or endorsement
- IRB protocol and submission checklist drafts
- stereo_cat.py and endless_beats.py with test suites
- src/ reference scaffolding for both designs
- SECS / MCD / F0 RMSE evaluation harness with preregistered H2c rule
- Consent-gated Design 2 training driver
### Changed
- Design 2 revised to use VoxCPM1.5's native `ref_audio` conditioning instead of
  reimplementing speaker-embedding injection
### Removed
- Two placeholder co-author names from the byline (no consent, no contribution)
EOF
echo "written: RELEASE_NOTES.md, CHANGELOG.md"
ls *.md docs/ irb/ tests/ src/ 2>/dev/null
