# RED-TEAM AUDIT — WBS-6 Synthesis, Second Pass (2026-07-28)

**Date:** 2026-07-28
**Auditor:** DeepChat (qnfo-agent v3.59)
**Scope:** Calibration register claims for P4, P5, P6 + Bayesian cascade
**Prior audit:** `_redteam-audit-2026-07-28.md` (infrastructure gaps)

---

## EXECUTIVE SUMMARY

Second-pass red-team audit of the 2026-07-28 calibration register update (commits 470a6ba, 80515cf). Four substantive findings — one requires remediation (P4 internal inconsistency), two are caveats (P6 self-citation, cascade sensitivity), one is a reproducibility gap (code not in repo). No credential leaks. All P5 and P6 claims verified against raw data.

---

## FINDING 1: P4 Status Internal Inconsistency (MEDIUM)

**Evidence:** The calibration-update-2026-07-28.md contains conflicting P4 designations:

| Location | Text |
|:---------|:-----|
| Line 13, status header | `[ANALYZED — SUPPORTED]` |
| Line 33, closing verdict | `P4 NOT DISCONFIRMED.` |
| Line 101, consolidated table | `[ANALYZED — SUPPORTED]` |
| Line 106, framework health | `2/7 supported (P4, P6)` |

**Analysis:** "SUPPORTED" and "NOT DISCONFIRMED" are epistemically distinct:
- SUPPORTED = positive evidence favoring the prediction
- NOT DISCONFIRMED = survived a test, no negative evidence

The methods table shows:
- Method 1 (character n-gram, real token features): r = 0.2004 — **below disconfirmation threshold** (r < 0.5)
- Method 2 (simulated semantic hierarchy): r = 0.8745 — above support threshold (r > 0.85)
- Method 3 (character n-gram, Euclidean): r = 0.5515 — inconclusive

Method 2 deliberately built hierarchical structure, demonstrating that the cophenetic measurement works when hierarchy exists — it is a POSITIVE CONTROL, not a genuine test of the P4 prediction. P4 predicts that TRAINED LLM embeddings exhibit ultrametric structure; neither method tested this directly.

**Recommendation:** (a) Resolve the internal inconsistency — pick SUPPORTED or NOT DISCONFIRMED and apply consistently. (b) Consider [MECHANISM DEMONSTRATED, DIRECT TEST PENDING] as a third option that better captures the evidence. (c) If SUPPORTED is retained, strengthen the caveat that the "support" relies on a positive control, not a direct test.

---

## FINDING 2: P6 Self-Citation Risk (LOW)

**Evidence:** The Qubit Delusion paper (DOI 10.5281/zenodo.21481054) which provides P6's claim-gap analysis (Section 5.3: 3--10× ratio, 20 milestone claims, 5 institutions) is QNFO-authored.

**Mitigation:** All 20 milestone claims are independently verifiable against public records (press releases, peer-reviewed papers, financial disclosures). A skeptical reviewer could replicate every entry without accessing QNFO infrastructure. The calibration register already documents P6 caveats in the Bayesian cascade section (caveat #3).

**Recommendation:** No change required. The existing caveat is sufficient. If P6 is ever cited as external evidence (e.g., by another group), the self-citation should be explicitly flagged.

---

## FINDING 3: Bayesian Cascade Sensitivity (LOW)

**Evidence:** The cascade's posterior is sensitive to likelihood assumptions:

| Scenario | Combined LR | Neutral Posterior |
|:---------|:-----------:|:-----------------:|
| Original (baseline) | 9.92 | 0.908 (91%) |
| P4+P6 both conservative (worst still plausible) | 2.98 | 0.748 (75%) |
| All noise (bad assumptions) | 1.91 | 0.656 (66%) |
| Drop P5 entirely (P4+P6 only) | 12.75 | 0.927 (93%) |

The posterior never drops below 65% even under worst plausible assumptions, and the calibration register explicitly documents that likelihoods are "subjective expert estimates, not objective frequency data" (caveat #5). A single strong disconfirmation (LR < 0.10) would nullify all current evidence.

**Recommendation:** Add the sensitivity table above to the calibration register to strengthen the documented caveats.

---

## FINDING 4: Analysis Code Not in Repo (MEDIUM)

**Evidence:** The Python scripts that generated P4 results (`_p4_ultrametric.py`, `_p4_results.json`) and the Bayesian cascade (`_cascade.py`, `_cascade_results.json`) existed in the temp workspace but were DELETED during cleanup. They are NOT committed to the wbs-6-synthesis repo.

**Violation:** §8.5 Per-Turn Checkpoint — any file the agent creates that a human would care about losing must exist in a durable store before the tool call is considered "done." P4 analysis code and cascade code are research artifacts that should be reproducible.

**Remediation:** Reconstruct `_p4_ultrametric.py` from session context and commit to `artifacts/p4_ultrametric_analysis.py`. Reconstruct `_cascade.py` and commit to `artifacts/p4_bayesian_cascade.py`. These scripts are approximately 150 lines and 90 lines respectively — reconstruction is feasible and should be done in this thread.

---

## FINDING 5: Bayesian Cascade Uses Self-Referential "SUPPORTED" Input (LOW — informational)

**Evidence:** The cascade's likelihoods for P4 (LR=4.5) and P6 (LR=2.83) are derived from the calibration register's own SUPPORTED designations. If P4 is downgraded per Finding #1, the cascade's combined LR changes accordingly. This is a structural dependency, not a bug — the cascade is downstream of the calibration register.

**Recommendation:** If P4 status is changed per Finding #1, re-run the cascade with updated likelihoods.

---

## VERIFIED (PASS)

| Check | Method | Result |
|:------|:-------|:------|
| P5 raw JSON matches claims | Cross-reference p5_results.json | ✅ global p=0.38, p=3 freq-MC p=0.035, B_95=0.004 |
| P6 claim-gap data exists | D1 paper body (29,802 chars) | ✅ Section 5.3: 3--10×, 5 institutions, 20 milestones |
| All files on disk | Get-ChildItem artifacts/ | ✅ 11 files, all present |
| Git state clean | git status | ✅ Working tree clean, branch up to date |
| Git pushed to origin | git push output | ✅ 80515cf pushed |
| Credential leak scan | Regex scan calibration + paper | ✅ No tokens/keys found |
| Scratch files cleaned | Get-ChildItem _* | ✅ Zero orphan scratch files |

---

## RED-TEAM VERDICT

| Gate | Finding | Severity | Action |
|:-----|:--------|:---------|:-------|
| P4 status consistency | SUPPORTED vs NOT DISCONFIRMED mismatch | MEDIUM | Amend calibration register |
| P6 self-citation | QNFO-authored evidence | LOW | Caveat already documented |
| Cascade sensitivity | Posterior sensitive to assumptions | LOW | Add sensitivity table |
| Code reproducibility | Analysis code deleted, not in repo | MEDIUM | Reconstruct and commit |
| Credential safety | No leaks | PASS | — |
| File integrity | All 11 files on disk | PASS | — |
| P5 data accuracy | All JSON claims match | PASS | — |
| P6 data accuracy | All D1 claims verified | PASS | — |

**Overall: 4/4 critical gates PASS. 2 MEDIUM findings (P4 inconsistency, code reproducibility). 2 LOW findings (self-citation, sensitivity). No BLOCKING issues.**

---

## REMEDIATION PLAN

1. Resolve P4 internal inconsistency — amend calibration-update-2026-07-28.md
   - Either: change status line to NOT DISCONFIRMED (consistent with closing)
   - Or: change closing to SUPPORTED (consistent with status — would require stronger claim)
   - Recommended: change to [MECHANISM DEMONSTRATED] with explicit caveat that direct LLM test not performed
2. Reconstruct and commit P4 analysis code to artifacts/
3. Reconstruct and commit cascade code to artifacts/
4. Add sensitivity table to calibration register document
