# Selection Rubric

## Purpose

Make idea selection auditable. Every idea in `idea_bank_47.md` is scored on the same seven
criteria, and every candidate asset in `candidate_assets/` is scored on the same asset rubric.

---

## 1. Idea-level rubric (7 criteria, 1–5)

| Criterion | 1 | 3 | 5 |
|---|---|---|---|
| **Patent relevance (PR)** | No connection to a claim | Tangential to a claim | Directly tests a stated claim |
| **Open-source feasibility (OSF)** | No public assets exist | Partial assets, heavy glue work | Scored public checkpoints + data exist |
| **Evaluation clarity (EC)** | No obvious metric | Metric exists but is contested | Preregisterable metric + baseline |
| **Compute cost (CC)** | Multi-GPU cluster | Single A100-class GPU | ≤1 consumer GPU or CPU |
| **License clarity (LC)** | Unclear or restrictive | Mixed; needs review | Permissive throughout |
| **Ethical manageability (ER)** | Unmitigable misuse risk | Mitigable with process controls | Low risk with standard consent |
| **Novelty vs. patents (NR)** | Restates the patent | Minor extension | Adds a claim the patent omits |

**Advancement gate:** OSF ≥ 4 **and** EC ≥ 4 **and** LC ≥ 4 **and** ER ≥ 3.

---

## 2. Asset-level rubric (7 criteria, 1–5)

Used in `evaluation/scorecards/` for datasets, checkpoints, and libraries.

| Criterion | What to check |
|---|---|
| **Maintenance** | Commit recency, open-issue response, release cadence |
| **License** | Explicit permissive license (Apache 2.0 / MIT preferred); no ambiguous "research only" |
| **Real usage** | Evidence of third-party adoption; not just a demo notebook |
| **Dependencies** | Count, weight, and stability of transitive deps |
| **Security** | Known CVEs in the dependency tree; supply-chain surface |
| **Fit** | Direct match to a design requirement (e.g., native LoRA support) |
| **Documentation** | Setup reproducibility from the README alone |

**Asset gate:** License ≥ 4 and Fit ≥ 4 and Security ≥ 3.

---

## 3. Scoring procedure

1. Two reviewers score independently.
2. Disagreements of ≥2 points are discussed and re-scored.
3. The lower of the two final scores is recorded (conservative rule).
4. Every score includes a one-line justification in the scorecard.

---

## 4. Tie-breaking

When ideas tie on total, prefer in order:

1. Higher **EC** (clearer evaluation beats broader scope).
2. Higher **CC** (cheaper beats more ambitious).
3. Higher **ER** (lower ethical risk beats higher novelty).
