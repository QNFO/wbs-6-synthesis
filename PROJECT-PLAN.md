# PROJECT-PLAN: WBS.6 Cross-Pillar Consilient Synthesis

**Project:** wbs-6-synthesis | **Status:** Active | **Date:** 2026-07-25
**Branch:** feature/wbs-6-synthesis | **Repo:** QNFO/wbs-6-synthesis

---

## §1 Charter

Synthesize the five cross-pillar QNFO research programs (Silent Radix, Adelic Physics, PBO/Autaxys, Qubit Delusion, Ultrametric Foundations) into a single consilience paper demonstrating structural convergence on the Adelic Core — valuation theory + Bruhat-Tits geometry + Ostrowski's theorem + adelic ring as the correct state-space for physics, computation, and optimization.

## §1.2 Core Claim

Ultrametric (non-Archimedean) mathematics provides the correct state-space geometry for physics, computation, and optimization, and the Archimedean (∞-place) description is a limit-point readout of this richer structure. `[speculative — no experimental confirmation]`

**Falsification criteria:** (1) ZBW frequency analysis shows no p-adic harmonic structure, (2) Silent Radix admits polynomial-time attack, (3) QEC code classification accuracy degrades below 50% on expanded test set.

---

## §2 WBS — Work Breakdown Structure

| Phase | Name | Status | Deliverable | Gate |
|:------|:-----|:------:|:------------|:-----|
| 0 | Project Init | ✅ | Repo, scaffold, .gitignore, README | P1-P8 |
| 1 | Due Diligence | ✅ | KG + D1 + Vectorize + external query | Cross-ref report |
| 2 | Literature Search | ✅ | Vectorize + KG + external APIs queried (SS blocked, arXiv empty) | `artifacts/literature-classification.md` |
| 3 | Citation Management | ✅ | 16 refs audited, 5 DOIs verified, 2 DOIs missing | `artifacts/citation-audit.md` |
| 4 | Deep Research | ⬜ | Bayesian cascade (if triggered) | Calibration register |
| 5 | Publication | ✅ | paper.md + PDF + Zenodo v1.0 + v1.1 | DOI resolves, D1 synced |
| 6 | Deployment | ✅ | D1 living-paper, papers-server | HTTP 200 |
| 7 | Dissemination | ✅* | Buffer: Bluesky ✅ Twitter ✅ LinkedIn ⛔ (queue full); SEO ✅; IA ✅ | 2/3 channels, IA submitted |
| 8 | Core Distribution | ✅ | R2 archive, KG node, GitHub + Zenodo + D1 | 4-layer verification |

---

## §3 Milestones & Gate Criteria

| Milestone | Phase | Gate | Status |
|:----------|:------|:-----|:------:|
| M1: Repo Ready | 0 | Pre-flight P1-P8 all HARD pass | ✅ |
| M2: Paper v1.0 Published | 5 | Zenodo DOI, D1, papers-server | ✅ `10.5281/zenodo.21547793` |
| M3: ACRP-01 Corrections | 5 | C1-C7 applied, red-team passed, v1.1 published | ✅ `10.5281/zenodo.21575332` |
| M4: Social Dissemination | 7 | Buffer posts on Twitter/LinkedIn/Bluesky | ⬜ |
| M5: Core Distribution | 8 | GitHub + Zenodo + R2 + D1/KG all consistent | ⬜ |

---

## §4 Deliverable Registry

| ID | Deliverable | Path | Archival | Status |
|:---|:------------|:-----|:---------|:------:|
| D1 | Consilience Paper v1.1 | `paper/paper.md` | Zenodo `21575332`, D1 | ✅ |
| D2 | Consilience Map | `artifacts/consilience-map.md` | Git, R2 | ✅ |
| D3 | Predictions Scorecard | `artifacts/predictions-scorecard.md` | Git, R2 | ✅ |
| D4 | PROJECT-PLAN.md | `PROJECT-PLAN.md` | Git, R2 | ✅ |
| D5 | Citation Audit | `artifacts/citation-audit.md` | Git, R2 | ⬜ |
| D6 | Literature Classification | `artifacts/literature-classification.md` | Git, R2 | ⬜ |
| D7 | SEO Audit Report | `artifacts/seo-audit.md` | Git, R2 | ⬜ |

---

## §5 Risk Register

| ID | Risk | Severity | Mitigation | Status |
|:---|:-----|:---------|:-----------|:------:|
| R1 | Pandoc+XeLaTeX PDF build fails on Unicode math | HIGH | Use `scripts/build-paper.py` per KIF-27; markdown is canonical source | ✅ |
| R2 | Zenodo newversion token/auth failure | MEDIUM | Token stored in env var; `zenodo-token-check.py` diagnostic | ✅ |
| R3 | Buffer social posting 401 | MEDIUM | Buffer 401 Diagnostic Protocol; token in 4-5 locations | ⬜ |
| R4 | KG seed drift from D1 | LOW | D1-first; reconcile KG post-publication | ⬜ |
| R5 | Consilience claim = confirmation bias | HIGH | External reviewer gates; symmetry template enforced | ⬜ |

---

## §6 Success Criteria
1. Paper published with persistent DOI on Zenodo ✅
2. All 7 falsifiable predictions documented with quantitative thresholds ✅
3. Paper accessible via papers.qnfo.org ✅
4. Core distribution: GitHub tag + Zenodo DOI + R2 archive + D1/KG record
5. Social dissemination on Twitter, LinkedIn, Bluesky
6. Internet Archive snapshot

---

## §7 Version History

| Version | Date | Tag | Description |
|:--------|:-----|:----|:------------|
| v1.0 | 2026-07-25 | v1.0 | Initial publication |
| v1.1 | 2026-07-25 | v1.1-ACRP-01 | ACRP-01 Phase 1 corrections (C1-C7) |
| v1.12 | 2026-07-26 | — | Phase 2-3 complete; KIF-29 scaffold fix; red-team audit passed |

---

## §8 Red-Team & Kaizen Register

| ID | Finding | Severity | Status | Resolution |
|:---|:--------|:---------|:------:|:-----------|
| KIF-29 | Phase 0 scaffold incomplete: `docs/`, `notebooks/`, `releases/` dirs missing | MEDIUM | ✅ | Created dirs, committed `c55f73f` |
| AR01 | `.zenodo_versions.json` `latest_deposit_id` blank in earlier version | LOW | ✅ | Updated during v1.1 publish to `21575332` |
| AR02 | Buffer LinkedIn blocked by account queue limit (10/10) | LOW | ⛔ | User must clear Buffer queue/upgrade plan |
| AR03 | 14 skills in trigger table not installed (KIF-13 propagation) | LOW | ⬜ | Skill ecosystem gap — `cloudflare`, `knowledge`, etc. not deployed |
| AR04 | Phase 2 external search partially blocked (SS 429, arXiv empty) | LOW | ⬜ | Need Semantic Scholar API key; paper already has 9 external refs |
| AR05 | 2 missing DOIs in references (Faddeev-Niemi 1997, Distler-Garibaldi 2010) | LOW | ⬜ | Add at next paper revision (v1.2) |
