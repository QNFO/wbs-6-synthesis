# Predictions Scorecard — WBS.6

## Falsifiable Predictions

| # | Prediction | Pillar | Test Method | Threshold | Status |
|:--|:-----------|:-------|:------------|:----------|:-------|
| P1 | ZBW frequency spectrum contains p-adic harmonics at f = f_0 · p^(-k) | Adelic (P2) | Spin noise spectroscopy on trapped electrons | p ∈ {2,3,5,7}, SNR > 3σ | `[DESIGNED]` |
| P2 | Silent Radix key recovery requires Ω(2^(b/log b)) operations | Silent Radix (P1) | Formal security reduction to LWE/SVP | Proof of reduction | `[DESIGNED]` |
| P3 | QEC codes with v_p^max > 20 exhibit O(1) overhead scaling | Ultrametric (P5) | Port classification to real hardware | Fidelity > 99.9% at N=10³ qubits | `[DESIGNED]` |
| P4 | Language model embeddings cluster ultrametrically on token-distinction corpora | PBO/Autaxys (P3) | Dendrogram cophenetic correlation | r > 0.85 ultrametric | `[UNTESTED]` |
| P5 | CMB power spectrum contains log-periodic oscillations at k_p = 2π/log p for p=2,3,5 | Adelic (P2) | Re-analysis of Planck 2018 data | Peak at p=2,3,5, significance > 3σ | `[DESIGNED]` |
| P6 | Qubit-count claims in press releases exceed peer-reviewed claims by >3× on average | Qubit Delusion (P4) | Reproducibility scorecard update (2026 data) | Ratio > 3.0, N > 20 claims | `[TESTABLE]` |
| P7 | Any positional numeral system with unknown base resists decoding in sub-exponential time | Silent Radix (P1) | Information-theoretic bound | Proof that SRE is in NP ∩ co-NP? | `[SPECULATIVE]` |

## Priority Ordering for Testing

| Priority | Prediction | Rationale | Cost | Timeline |
|:---------|:-----------|:----------|:-----|:---------|
| 1 | P5 (CMB oscillations) | Uses existing Planck 2018 data; zero new experimental cost | $0 | Weeks |
| 2 | P1 (ZBW p-adic harmonics) | Existing trapped-ion hardware; protocol designed | ~$10K | Months |
| 3 | P4 (Ultrametric embeddings) | Software-only; train on standard corpora | Compute cost | Weeks |
| 4 | P6 (Qubit claims audit) | Literature review; no experiments | $0 | Weeks |
| 5 | P3 (O(1) QEC scaling) | Requires hardware access + code porting | High | Years |
| 6 | P2 (Silent Radix reduction) | Pure mathematics; no equipment | $0 | Unknown |
| 7 | P7 (Information-theoretic bound) | Deep theoretical work | $0 | Unknown |

## Disconfirmation Criteria

The framework is disconfirmed if **any** of the following are demonstrated:

1. ZBW frequency analysis shows no p-adic harmonic structure beyond random noise
2. Silent Radix admits a polynomial-time attack
3. QEC code classification accuracy degrades below 50% on expanded code family test set
4. CMB re-analysis finds no log-periodic structure at any p
5. Ultrametric embeddings produce cophenetic correlation r < 0.5
