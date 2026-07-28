"""
Phase 4: Bayesian Cascade — Five Pillars Framework Posterior Update
====================================================================
Updates P(H|evidence) given P4, P5, P6 results from the
calibration register (2026-07-28).

Method: Bayes' theorem with subjective likelihood estimates.
Evidence grade: MODERATE (combined LR = 9.92).
"""

import math, json

priors = {
    "neutral": 0.50,
    "conservative": 0.25,
    "skeptical": 0.10,
    "optimistic": 0.75
}

analyses = [
    {
        "id": "P4", "name": "Ultrametric LLM embeddings",
        "status": "NOT DISCONFIRMED",
        "evidence": "r = 0.8745 (positive control); r = 0.2004 (char n-gram)",
        "P_E_given_H": 0.90,
        "P_E_given_notH": 0.20,
    },
    {
        "id": "P5", "name": "CMB log-periodic oscillations",
        "status": "NOT DISCONFIRMED",
        "evidence": "global p = 0.38, p=3 freq-MC p=0.035 (fails Bonferroni)",
        "P_E_given_H": 0.70,
        "P_E_given_notH": 0.90,
    },
    {
        "id": "P6", "name": "Qubit-count press vs peer-reviewed ratio",
        "status": "SUPPORTED",
        "evidence": "3--10x ratio, N=20 claims, 5 institutions",
        "P_E_given_H": 0.85,
        "P_E_given_notH": 0.30,
    }
]

for a in analyses:
    a["LR"] = round(a["P_E_given_H"] / a["P_E_given_notH"], 3)

total_LR = round(math.prod(a["LR"] for a in analyses), 3)

print("=" * 65)
print("PHASE 4: BAYESIAN CASCADE — FIVE PILLARS FRAMEWORK UPDATE")
print("=" * 65)
print("\n## Likelihood Ratios\n")
print(f"{'Prediction':<6} {'Status':<18} {'P(E|H)':<10} {'P(E|notH)':<10} {'LR':<8}")
print("-" * 55)
for a in analyses:
    print(f"{a['id']:<6} {a['status']:<18} {a['P_E_given_H']:<10.2f} {a['P_E_given_notH']:<10.2f} {a['LR']:<8.3f}")
print("-" * 55)
print(f"{'TOTAL':<6} {'':<18} {'':<10} {'':<10} {total_LR:<8.3f}")

print("\n## Posterior Update\n")
print(f"{'Prior':<18} {'P(H)':<10} {'Posterior Odds':<16} {'Posterior P(H)':<14} {'Delta':<10}")
print("-" * 70)

results = {}
for name, prior in priors.items():
    prior_odds = prior / (1 - prior)
    posterior_odds = prior_odds * total_LR
    posterior = posterior_odds / (1 + posterior_odds)
    delta = posterior - prior
    results[name] = {
        "prior": prior, "posterior": round(posterior, 4),
        "delta": round(delta, 4), "odds_ratio": round(total_LR, 3)
    }
    print(f"{name:<18} {prior:<10.2f} {posterior_odds:<16.2f} {posterior:<14.4f} {delta:+.4f}")

# ============================================================
# SENSITIVITY ANALYSIS (Red-team addition, 2026-07-28)
# ============================================================
print("\n\n## Sensitivity Analysis (Red-Team v2)\n")
print(f"{'Scenario':<55} {'Combined LR':<12} {'Posterior':<10} {'Grade':<15}")
print("-" * 95)

def lr(p_e_h, p_e_not_h):
    return p_e_h / p_e_not_h

def compute_post(prior, lrs):
    odds = prior / (1 - prior)
    for l in lrs:
        odds *= l
    return odds / (1 + odds)

base = {a["id"]: {"E_given_H": a["P_E_given_H"], "E_given_notH": a["P_E_given_notH"]} for a in analyses}
scenarios = [
    ("Original (baseline)", base),
    ("P4 conservative: P(E|notH)=0.40", {**base, "P4": {"E_given_H": 0.90, "E_given_notH": 0.40}}),
    ("P6 conservative: P(E|notH)=0.50", {**base, "P6": {"E_given_H": 0.85, "E_given_notH": 0.50}}),
    ("Both P4+P6 conservative (worst plausible)", {**base,
        "P4": {"E_given_H": 0.90, "E_given_notH": 0.40},
        "P6": {"E_given_H": 0.85, "E_given_notH": 0.50}}),
    ("Drop P5 (only P4+P6)", {"P4": base["P4"], "P6": base["P6"]}),
    ("All noise (worst assumptions)", {**base,
        "P4": {"E_given_H": 0.70, "E_given_notH": 0.40},
        "P6": {"E_given_H": 0.70, "E_given_notH": 0.50}}),
]

for name, params in scenarios:
    lrs_test = [lr(params[k]["E_given_H"], params[k]["E_given_notH"]) for k in params]
    combined = math.prod(lrs_test)
    post = compute_post(0.50, lrs_test)
    grade = "SUBSTANTIAL" if combined > 10 else "MODERATE" if combined > 3 else "WEAK"
    print(f"{name:<55} {combined:<12.3f} {post:<10.4f} {grade:<15}")

# Resilience test
print(f"\n\nRESILIENCE TEST: What would it take to return posterior to 0.50?")
print("-" * 65)
orig_lrs = [a["LR"] for a in analyses]
combined_lr = math.prod(orig_lrs)
lr_needed = 1.0 / combined_lr
print(f"  Current combined LR: {combined_lr:.3f}")
print(f"  LR needed to return to prior: {lr_needed:.4f}")
print(f"  Example disconfirmation: P(P7|H)=0.05, P(P7|notH)=0.50 => LR={0.05/0.50:.4f}")
print(f"  A single strong disconfirmation (LR < {lr_needed:.4f}) nullifies all current evidence.")

print("\n\n## Caveats")
print("1. P4: Positive control only — direct LLM test NOT performed.")
print("2. P5: Non-result, LR < 1 weakly favors null hypothesis.")
print("3. P6: QNFO-authored evidence (independently verifiable).")
print("4. P1-P3,P7: No evidence weight.")
print("5. Likelihoods are subjective expert estimates, not frequencies.")
print("6. Posterior is illustrative — not a formal Bayesian model.")

# Export
output = {
    "phase": 4, "name": "Bayesian Cascade",
    "date": "2026-07-28",
    "framework": "Five Pillars, One Structure",
    "doi": "10.5281/zenodo.21603374",
    "predictions": [{"id": a["id"], "status": a["status"], "lr": a["LR"]} for a in analyses],
    "combined_lr": total_LR,
    "results": {n: {"prior": v["prior"], "posterior": v["posterior"], "delta": v["delta"]} for n, v in results.items()},
    "evidence_grade": "MODERATE",
    "sensitivity": {
        "baseline_posterior": results["neutral"]["posterior"],
        "worst_plausible_posterior": compute_post(0.50, [
            lr(0.90, 0.40), lr(0.70, 0.90), lr(0.85, 0.50)
        ]),
        "lr_to_nullify": round(lr_needed, 4)
    },
    "note": "Based on 1 SUPPORTED + 2 NOT DISCONFIRMED. Likelihoods are subjective estimates."
}

with open("cascade_results.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)
print(f"\nResults saved to cascade_results.json")
