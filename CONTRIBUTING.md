# Contributing

## Hard rules

1. **No voice data in pull requests.** Audio, embeddings, and adapter weights are excluded by
 `.gitignore` and will be rejected.
2. **No baked speaker models.** Adapters and configs only.
3. **Every new candidate asset needs a scorecard** in `evaluation/scorecards/` before it is
 referenced in a design or config.
4. **Consent before cloning.** No experiment may run against a speaker without a completed
 `docs/consent_form.md` on file.

## Workflow

1. Open an issue describing the change (new idea, new asset, design revision).
2. Score any new asset on the seven-criterion rubric.
3. Submit a PR with: the change, the scorecard, and a one-line justification.
4. For changes to `docs/idea_bank_47.md`, include the total-score arithmetic.

## Authorship

Author order and inclusion are unresolved. Do not add or remove names from `CITATION.cff` or
`paper/draft.md` without written confirmation from all listed individuals.
