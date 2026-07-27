# Calibration Register Update — 2026-07-27 (AMENDED — RED-TEAM v1)

**Paper:** Five Pillars, One Structure (v1.3)
**DOI:** 10.5281/zenodo.21547793 (concept), latest version 10.5281/zenodo.21603374
**OSF Registration:** 2ndsz — CMB Higher n-Point p-Adic Signature Search (submitted 2026-07-20)
**Next check date:** 2026-12 (earliest declared: P5 CMB, P6 Qubit)
**Days until next check:** ~157

---

## RED-TEAM AMENDMENT (2026-07-27)

The original v1 calibration memo contained a material error in its P5 assessment.
A red-team internal search (D1 + KG + Vectorize + disk audit) discovered that
**QNFO HAS performed a log-periodic CMB analysis of Planck 2018 data** via the
CAL-03 calibration paper (harmonische-paradigma project, DOI 10.5281/zenodo.21534747,
2026-07-23). The v1 memo incorrectly stated that the analysis had "not been
executed."

**Correction:** CAL-03 searched for log-periodic oscillations at periods
ln(q) = 1 (q = e), ln(q) = ln(π), and ln(q) = 3.122 (Efimov) — NOT the
p-adic periods k_p = 2π/log p predicted by P5. CAL-03's target periods and
P5's periods are distinct:

| Period | CAL-03 target | P5 target | Match? |
|:-------|:-------------|:----------|:-------|
| ln(2) ≈ 0.693 | Not tested | **P5 p=2** | No |
| ln(3) ≈ 1.099 | Near ln(π)=1.145 | **P5 p=3** | No (10.2% offset) |
| ln(5) ≈ 1.609 | Not tested | **P5 p=5** | No |

CAL-03's result — global p = 0.38 (full-spectrum, 2,507 ℓ points), no
significant log-periodic oscillations — does NOT test P5. P5 predicts
oscillations at different frequencies from those searched by CAL-03.

**CAL-03's reusable assets for P5:**
- Working Python pipeline: `cal03_log_periodogram_full.py`
- Planck 2018 unbinned TT data (2,507 points) archived locally
- Lomb-Scargle methodology validated on Planck data
- Monte Carlo null distribution pipeline
- Amplitude sensitivity: B₉₅ < 0.004 (constrains ALL log-periodic signals
  in Planck data, including p-adic periods — any P5 signal must exceed this
  amplitude to be detectable)

---

## Summary

All 7 predictions remain unconfirmed. The calibration register is 5 months
before its first declared check date (2026-12). Four predictions (P1-P3, P7)
are blocked by hardware access or proof requirements. Three predictions (P4-P6)
can be advanced now with available data or computational resources.

**Framework health:** 0/7 confirmed, 0/7 disconfirmed. The critical metric is
"how many disconfirmed" — a single disconfirmation would substantially weaken
the consilience claim.

---

## Individual Prediction Status

### P1 — ZBW p-Adic Harmonics
- **Status:** `[DESIGNED]` — unchanged
- **Protocol:** Spin noise spectroscopy on trapped electrons (6-paper chain)
- **Blockers:** Requires trapped-ion hardware and experimental collaboration
- **Disconfirms if:** ZBW frequency analysis shows no p-adic harmonic
  structure beyond random noise (p ∈ {2,3,5,7}, SNR > 3σ)

### P2 — Silent Radix Security Reduction
- **Status:** `[DESIGNED]` — unchanged
- **Required:** Formal security reduction to LWE, SVP, or equivalent
- **Disconfirms if:** Silent Radix admits a polynomial-time attack

### P3 — QEC O(1) Overhead Scaling
- **Status:** `[DESIGNED]` — unchanged
- **Current evidence:** 83% classification accuracy on 4 code families
- **Required:** Validation across full stabilizer code zoo, hardware
  demonstration at N=10³ qubits with fidelity >99.9%
- **Disconfirms if:** QEC code classification accuracy degrades below
  50% on expanded code family test set

### P4 — Ultrametric LLM Embeddings
- **Status:** `[UNTESTED]` — NOW ACTIONABLE
- **Required:** Train language model on token-distinction corpora;
  compute dendrogram cophenetic correlation; verify r > 0.85
- **Cost:** Compute only (software-only)
- **Disconfirms if:** Cophenetic correlation r < 0.5

### P5 — CMB Log-Periodic Oscillations ⭐ AMENDED

- **Status:** `[DESIGNED]` → `[PARTIALLY ANALYZED — p-adic periods NOT yet tested]`
- **Data:** Planck 2018 Legacy Archive (publicly available, final release)
- **Analysis performed:** CAL-03 (DOI 10.5281/zenodo.21534747, 2026-07-23)
  analyzed Planck 2018 full TT spectrum (2,507 points) for log-periodic
  oscillations at periods ln(q) = 1 (q=e), ln(π), and ln(22.694) — NOT the
  p-adic periods predicted by P5.
- **CAL-03 result:** Global p = 0.38 — fully consistent with ΛCDM + noise.
  No significant oscillations at e, π, or Efimov periods.
- **P5's untested periods:** k_p = 2π/log p for p=2,3,5:
  - p=2: ln(2) ≈ 0.693 — NOT tested by CAL-03
  - p=3: ln(3) ≈ 1.099 — NOT tested (closest CAL-03 target: ln(π)=1.145, 4.2% higher)
  - p=5: ln(5) ≈ 1.609 — NOT tested by CAL-03
- **Reusable assets from CAL-03:**
  - Working pipeline: `cal03_log_periodogram_full.py` (1,000-point log-grid,
    5,000 frequency Lomb-Scargle, 200 MC simulations)
  - Planck 2018 data archived: `cal03-data/COM_PowerSpect_CMB-TT-full_R3.01.txt`
  - Verified ΛCDM subtraction: χ²/dof = 1.027
  - Amplitude sensitivity: B₉₅ < 0.004 (any p-adic signal must exceed this
    to be detectable in Planck data)
- **Protocol:** Designed (QNFO 2026-04-13), 3-step: (1) log-resampling C_ℓ,
  (2) Lomb-Scargle periodogram at p-adic frequencies, (3) MC significance
- **OSF Pre-registration:** 2ndsz (2026-07-20)
- **Analysis cost:** $0 — data and working code exist; modification to target
  p-adic periods is a parameter change in an existing pipeline
- **Next step:** Run `cal03_log_periodogram_full.py` with target periods set to
  ln(2), ln(3), ln(5) instead of ln(e), ln(π), ln(22.694). A ~10-line code
  change.
- **Disconfirms if:** CMB re-analysis finds no log-periodic structure at
  any p with significance > 3σ

### P6 — Qubit-Count Press vs. Peer-Reviewed Ratio
- **Status:** `[TESTABLE]` — 2026 data accumulating
- **Required:** Systematic collection comparing press release qubit claims
  against peer-reviewed paper claims. Threshold: >3× ratio, N > 20 claims.
- **Disconfirms if:** Ratio < 1.5 (press and peer-reviewed substantially aligned)

### P7 — SRE Sub-Exponential Time
- **Status:** `[SPECULATIVE]` — unchanged
- **Required:** Information-theoretic bound proving SRE is in NP ∩ co-NP

---

## Priority-Actionable Next Steps

| Priority | Prediction | Action | Cost | Timeline | Notes |
|:---------|:-----------|:-------|:-----|:---------|:------|
| **1** | P5 (CMB) | Adapt CAL-03 pipeline for p-adic periods | $0 | ~30 min | Code exists, parameter change only |
| **2** | P4 (Embeddings) | Train small LM, compute ultrametric clustering | Compute | Weeks | Software-only |
| **3** | P6 (Qubit) | Systematic press vs. peer-reviewed claim collection | $0 | Weeks | Literature review |
| 4 | P1 (ZBW) | Seek experimental collaboration | ~$10K | Months | Hardware-dependent |
| 5 | P2 (SRE proof) | Mathematical research | $0 | Unknown | Proof-dependent |
| 6 | P3 (QEC) | Hardware access + code porting | High | Years | Hardware-dependent |
| 7 | P7 (SRE bound) | Complexity theory | $0 | Unknown | Proof-dependent |

---

## Calibration Register — Consolidated (AMENDED)

| # | Prediction | Status (2026-07-27) | Next Check | Disconfirmation Gate |
|:--|:-----------|:---------------------|:-----------|:---------------------|
| P1 | ZBW p-adic harmonics | `[DESIGNED]` | 2026-12 | No harmonics > 3σ |
| P2 | Silent Radix reduction | `[DESIGNED]` | TBD | Poly-time attack found |
| P3 | QEC O(1) overhead | `[DESIGNED]` | 2027+ | Accuracy < 50% |
| P4 | Ultrametric LLM embeddings | `[UNTESTED]` **PRIORITY** | Can test now | r < 0.5 |
| P5 | CMB log-periodic oscillations | `[PARTIALLY ANALYZED — p-adic periods untested]` | **2026-12** | No structure at any p |
| P6 | Qubit-count ratio > 3× | `[TESTABLE, DATA ACCUMULATING]` | **2026-12** | Ratio < 1.5 |
| P7 | SRE sub-exponential | `[SPECULATIVE]` | TBD | N/A (not falsifiable) |

---

## Red-Team Self-Audit

| Gate | Finding | Verdict |
|:-----|:--------|:--------|
| CAL-03 existence | v1 memo claimed "QNFO has not executed the analysis" — FALSE. CAL-03 exists (harmonische-paradigma, DOI 10.5281/zenodo.21534747) and analyzed Planck 2018 full spectrum | **FAIL → CORRECTED** |
| Period differentiation | CAL-03 targeted e, π, Efimov periods; P5 targets ln(2), ln(3), ln(5). These are DISTINCT predictions — CAL-03 result does not test P5 | **PASS (with nuance)** |
| CAL-03 global p-value | Full-spectrum p = 0.38 (2,507 points, 5,000 frequencies, 200 MC sims) — the definitive number. The binned p = 0.09 was inflated by noise averaging. | **PASS** |
| CAL-03 methodology | Pipeline code exists and is verified working. Can be adapted to p-adic periods with minor parameter changes. | **PASS** |
| Amplitude constraint | B₉₅ < 0.004 applies to all log-periodic signals in Planck data. Any P5 signal must be above this threshold. | **PASS** |
| OSF registration | 2ndsz confirmed pre-registered 2026-07-20 | **PASS** |
| CMB-S4 protocol | CAL-03 includes pre-registered CMB-S4 protocol (2028). P5 can benefit from this independent effort. | **PASS** |
| CAL-03 not in D1/papers.qnfo.org | Confirmed: CAL-03 exists only on disk (D:\qnfoworkspace) and Zenodo. No D1/KG record. | **WARN — not blocking** |
| v1 memo now stale on R2/GitHub | The original calibration-update-2026-07-27.md with the error is committed. This amendment supersedes it. | **ACTION: update** |

---

**Author:** QNFO Research Collective
**Date:** 2026-07-27 (amended)
**Status:** Phase 4 Calibration Update (Red-Team v1)
**Related:** Paper v1.3 (10.5281/zenodo.21603374), OSF 2ndsz, CAL-03 (10.5281/zenodo.21534747)
