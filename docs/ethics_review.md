# Ethics Review

**Status:** Draft for institutional review. Complete and sign before any cloning experiment.
**Designs covered:** 1 (inner voice), 2 (few-shot cloning).

---

## 1. Risk register

| ID | Risk | Likelihood | Impact | Mitigation | Residual |
|---|---|---|---|---|---|
| R1 | Non-consensual impersonation using released artifacts | Low | Severe | Release adapters only; no baked identities; watermarking | Low |
| R2 | Speaker re-identification from adapters or embeddings | Low | High | No embedding release; k-anonymity check on any released stats | Low |
| R3 | Psychological harm from inner-voice mismatch | Medium | Medium | Pre-screening, debrief, opt-out at any time | Low |
| R4 | Demographic conditioning encodes stereotypes | Medium | Medium | Demographic vectors used as controls, not targets; per-group reporting | Medium |
| R5 | License violation on base checkpoint or dataset | Low | High | License gate in asset rubric; no run until scored | Low |
| R6 | Synthetic audio mistaken for real in publication | Medium | Medium | All demo audio labeled; watermark where supported | Low |
| R7 | Withdrawal request after adapter training | Low | Medium | Documented deletion SLA; retrain or discard adapter | Low |

---

## 2. Consent requirements

Aligned with the NO FAKES Act (2026) authorization framework and the 2025 Interactive Media
Agreement consent standard.

- **Written, specific, revocable** consent is required for every speaker.
- Consent must name: purpose, data types, synthesis scope, retention period, release tier.
- **Tiered release** (default = Tier 1):

| Tier | Permits | Default |
|---|---|---|
| 1 | Research analysis only; no synthetic audio leaves the lab | ✅ |
| 2 | Tier 1 + consented synthetic demo audio in the paper | |
| 3 | Tier 2 + adapter release | |

- **Withdrawal:** raw audio and derived embeddings deleted within **30 days**; any trained
 adapter deleted or retrained without the speaker.

---

## 3. Data handling

- Raw audio stored on encrypted local storage; **never** committed to the repository.
- Embeddings treated as **sensitive biometric-adjacent data**; not released, not logged in
 plaintext, deleted on withdrawal.
- Access limited to named researchers on the project.
- Retention: raw audio ≤ 24 months from collection; embeddings ≤ duration of the study + 6 months.

---

## 4. Release policy

**Will release:**
- Training and evaluation code (MIT).
- Configs and scorecards.
- Preregistered protocols and result tables.
- Tier-2 consented synthetic evaluation audio.

**Will not release:**
- Raw speaker audio.
- Speaker embeddings.
- Baked speaker models or voice slots.
- Any adapter whose base-model license is incompatible with redistribution.

---

## 5. Dual-use statement

Voice cloning enables impersonation and fraud; 2026 policy activity treats this as a live harm.
This project mitigates by:

1. Restricting cloning to consenting speakers.
2. Releasing adapters and protocols, not identities.
3. Reporting detection-relevant artifacts (watermark presence, spectral fingerprints).
4. Framing efficiency results as **responsible-accessibility** findings, not scaling results.

---

## 6. Review sign-off

| Role | Name | Date | Signature |
|---|---|---|---|
| Principal investigator | | | |
| Ethics reviewer | | | |
| Data protection contact | | | |

> No experiment may begin until this table is complete.
