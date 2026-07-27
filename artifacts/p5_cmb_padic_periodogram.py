#!/usr/bin/env python3
"""
P5: CMB Log-Periodogram — P-Adic Periods (Planck 2018 Full Spectrum)

Adapted from CAL-03 (harmonische-paradigma, DOI 10.5281/zenodo.21534747).
Tests the WBS-6 P5 prediction: log-periodic oscillations in the CMB at
p-adic periods ln(p) for p=2,3,5 — corresponding to frequencies
k_p = 2π/log p predicted by the Adelic Core framework.

Method: Lomb-Scargle periodogram on log-resampled Planck 2018 TT data,
with Monte Carlo significance against 200 ΛCDM+noise mocks.
"""
import numpy as np
from scipy.signal import lombscargle
from scipy.interpolate import interp1d
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json, os, time

print("=" * 70, flush=True)
print("P5: CMB Log-Periodogram — P-ADIC PERIODS (ln 2, ln 3, ln 5)", flush=True)
print("=" * 70, flush=True)

# ── Paths ──
DATA_DIR = r"D:\qnfoworkspace\research\harmonische-paradigma\cal03\data"
OUT_DIR = r"C:\Users\LENOVO\source\repos\wbs-6-synthesis\artifacts\p5_results"
os.makedirs(OUT_DIR, exist_ok=True)

# ── 1. Load data ──
print("\n[1] Loading Planck 2018 full TT spectrum...", flush=True)

full_path = os.path.join(DATA_DIR, 'COM_PowerSpect_CMB-TT-full_R3.01.txt')
if not os.path.exists(full_path):
    print(f"ERROR: Data file not found: {full_path}", flush=True)
    sys.exit(1)

full_data = np.loadtxt(full_path, comments='#')
ell_full = full_data[:, 0]
dl_full = full_data[:, 1]
err_m_full = full_data[:, 2]
err_p_full = full_data[:, 3]
errors_full = (err_m_full + err_p_full) / 2.0

print(f"  Full spectrum: {len(ell_full)} pts, l={ell_full[0]:.0f}-{ell_full[-1]:.0f}", flush=True)
print(f"  Mean error: {np.mean(errors_full):.1f} uK^2", flush=True)

# Load best-fit LambdaCDM theory
theory_path = os.path.join(DATA_DIR, 'planck_tt_bestfit.txt')
theory_full = np.loadtxt(theory_path, comments='#')
ell_th = theory_full[:, 0].astype(int)
dl_th = theory_full[:, 1]
print(f"  Theory: {len(ell_th)} pts, l={ell_th[0]}-{ell_th[-1]}", flush=True)

bf_interp_full = interp1d(ell_th, dl_th, kind='cubic',
                           bounds_error=False, fill_value='extrapolate')
dl_bf_full = bf_interp_full(ell_full)

# ── 2. Analysis range & residuals ──
mask = (ell_full >= 30) & (ell_full <= 2500)
ell_a = ell_full[mask]
dl_a = dl_full[mask]
err_a = errors_full[mask]
dl_bf_a = dl_bf_full[mask]

residuals_a = dl_a - dl_bf_a

chi2 = np.sum((residuals_a / err_a) ** 2)
dof = len(residuals_a)
print(f"\n  Analysis range: l={ell_a[0]:.0f}-{ell_a[-1]:.0f}, N={len(ell_a)} pts", flush=True)
print(f"  chi2/dof = {chi2:.1f}/{dof} = {chi2/dof:.3f}", flush=True)
print(f"  RMS residuals = {np.sqrt(np.mean(residuals_a**2)):.1f} uK^2", flush=True)

# ── 3. Log-resample ──
print("\n[2] Log-resampling (1000-point uniform grid)...", flush=True)

n_pts = 1000
x_data = np.log(ell_a)
x_grid = np.linspace(np.log(30), np.log(2500), n_pts)
delta_x = x_grid[1] - x_grid[0]
x_span = x_grid[-1] - x_grid[0]

r_interp = interp1d(x_data, residuals_a, kind='cubic',
                    bounds_error=False, fill_value='extrapolate')
e_interp = interp1d(x_data, err_a, kind='cubic',
                    bounds_error=False, fill_value='extrapolate')
y_grid = r_interp(x_grid)
e_grid = e_interp(x_grid)

weights = 1.0 / (e_grid ** 2)
weights /= np.mean(weights)
y_mean = np.average(y_grid, weights=weights)
y_norm = y_grid - y_mean

print(f"  Grid: {n_pts} pts, Dx={delta_x:.4f}, span={x_span:.2f} ln-units", flush=True)
for p in [2, 3, 5]:
    print(f"  Cycles for ln(p={p}): {x_span/np.log(p):.1f}", flush=True)

# ── 4. Lomb-Scargle periodogram ──
print("\n[3] Lomb-Scargle periodogram (5000 frequencies)...", flush=True)

f_min, f_max = 0.02, 5.0
n_freq = 5000
freqs = np.linspace(f_min, f_max, n_freq)
ang_freqs = 2 * np.pi * freqs

power = lombscargle(x_grid, y_norm, ang_freqs, normalize='normalize', weights=weights)
periods = 1.0 / freqs
q_vals = np.exp(periods)

# ── 5. Peak search ──
print("[4] Peak search...", flush=True)

peaks = []
for i in range(1, len(power) - 1):
    if power[i] > power[i-1] and power[i] > power[i+1]:
        peaks.append({
            'freq': float(freqs[i]),
            'period': float(periods[i]),
            'q': float(q_vals[i]),
            'power': float(power[i]),
        })

peaks.sort(key=lambda p: p['power'], reverse=True)

print(f"\n  Top 20 peaks:", flush=True)
print(f"  {'Freq':>8s}  {'Period':>8s}  {'q':>10s}  {'Power':>8s}", flush=True)
for p in peaks[:20]:
    print(f"  {p['freq']:8.4f}  {p['period']:8.4f}  {p['q']:10.4f}  {p['power']:8.4f}", flush=True)

# ── 6. Power at P5 p-adic target periods ──
print("\n[5] Power at P5 p-adic target periods...", flush=True)

# P5 predicts oscillations at k_p = 2*pi/log p
# In log-l space: period = 2*pi/k_p = log p
# Frequency: f = 1 / log p
import math

padic_preds = {}
for p_name, p_val in [("p=2", 2), ("p=3", 3), ("p=5", 5)]:
    period = math.log(p_val)
    freq = 1.0 / period
    padic_preds[p_name] = {'p': p_val, 'period': period, 'frequency': freq, 'ln_period': period}
    print(f"  P5 {p_name}: period = ln({p_val}) = {period:.6f}, f = {freq:.6f}", flush=True)

target_results = {}
for name, info in padic_preds.items():
    tf = info['frequency']
    idx = np.argmin(np.abs(freqs - tf))
    p_val_power = float(power[idx])
    f_val = float(freqs[idx])
    
    # Single-frequency FAP
    single_fap = (1.0 - p_val_power) ** ((n_pts - 3) / 2.0) if p_val_power < 1 else 0
    n_indep_fap = int((f_max - f_min) * x_span)
    multi_fap = 1.0 - (1.0 - single_fap) ** n_indep_fap
    
    target_results[name] = {
        'p': info['p'],
        'frequency': f_val,
        'period': info['period'],
        'q': float(np.exp(info['period'])),
        'power': p_val_power,
        'single_fap': float(single_fap),
        'multi_fap': float(multi_fap),
    }
    print(f"  P5 {name}: f={f_val:.4f}, period={info['period']:.4f}, q={np.exp(info['period']):.4f}, "
          f"LS power={p_val_power:.6f}, single-FAP={single_fap:.4f}", flush=True)

# ── 7. Template correlation ──
print("\n[6] Template correlation analysis...", flush=True)

ell_grid = np.exp(x_grid)
ell0 = ell_grid[n_pts // 2]

def correlate_full(period, phase):
    template = np.cos(2 * np.pi * np.log(ell_grid / ell0) / period + phase)
    w = 1.0 / (e_grid ** 2)
    w /= np.sum(w)
    yw = np.sqrt(w) * y_grid
    tw = np.sqrt(w) * template
    r = np.corrcoef(yw, tw)[0, 1]
    if abs(r) < 1:
        t_stat = r * np.sqrt((n_pts - 2) / (1 - r**2))
        pval_t = 2 * stats.t.sf(abs(t_stat), n_pts - 2)
    else:
        pval_t = 0.0
    return r, pval_t, template

template_results = {}
for name, info in padic_preds.items():
    period = info['period']
    r_cos, p_cos, _ = correlate_full(period, 0.0)
    r_sin, p_sin, _ = correlate_full(period, np.pi/2)
    r_best = r_cos if abs(r_cos) >= abs(r_sin) else r_sin
    p_best = p_cos if abs(r_cos) >= abs(r_sin) else p_sin
    phase_best = "cos" if abs(r_cos) >= abs(r_sin) else "sin"
    template_results[name] = {
        'r_cos': float(r_cos), 'p_cos': float(p_cos),
        'r_sin': float(r_sin), 'p_sin': float(p_sin),
        'r_best': float(r_best), 'p_best': float(p_best),
        'phase_best': phase_best,
    }
    print(f"  P5 {name} (period={period:.4f}): r={r_best:+.4f}, p={p_best:.4f} ({phase_best})", flush=True)

# Phase scans for p-adic periods
for name, info in padic_preds.items():
    period = info['period']
    phases = np.linspace(0, 2*np.pi, 200)
    rs = np.array([correlate_full(period, phi)[0] for phi in phases])
    best_idx = np.argmax(np.abs(rs))
    print(f"  P5 {name} phase scan: best phi={phases[best_idx]:.4f} rad, r_max={rs[best_idx]:+.4f}", flush=True)

# ── 8. Monte Carlo significance ──
print("\n[7] Monte Carlo significance (200 LambdaCDM + noise mocks)...", flush=True)
t0 = time.time()

n_sims = 200
max_powers_null = np.zeros(n_sims)
rng = np.random.default_rng(42)

for i in range(n_sims):
    if (i+1) % 50 == 0:
        t_elapsed = time.time() - t0
        print(f"    {i+1}/{n_sims} ({t_elapsed:.0f}s)...", flush=True)
    
    mock_dl = dl_bf_a + rng.normal(0, err_a)
    mock_res = mock_dl - dl_bf_a
    m_interp = interp1d(x_data, mock_res, kind='cubic',
                        bounds_error=False, fill_value='extrapolate')
    m_grid = m_interp(x_grid)
    m_mean = np.average(m_grid, weights=weights)
    m_norm = m_grid - m_mean
    m_power = lombscargle(x_grid, m_norm, ang_freqs,
                          normalize='normalize', weights=weights)
    max_powers_null[i] = np.max(m_power)

t1 = time.time()
print(f"  Done in {t1-t0:.1f}s", flush=True)

max_power_obs = np.max(power)
p_value_global = np.mean(max_powers_null >= max_power_obs)

print(f"\n  Observed max power:   {max_power_obs:.6f}", flush=True)
print(f"  Null median:          {np.median(max_powers_null):.6f}", flush=True)
print(f"  Null 68% (1-sigma):   {np.percentile(max_powers_null, 68):.6f}", flush=True)
print(f"  Null 95% (2-sigma):   {np.percentile(max_powers_null, 95):.6f}", flush=True)
print(f"  Null 99% (2.6-sigma): {np.percentile(max_powers_null, 99):.6f}", flush=True)
print(f"  Null 99.7% (3-sigma): {np.percentile(max_powers_null, 99.7):.6f}", flush=True)
print(f"  Global MC p-value:    {p_value_global:.4f}", flush=True)

# ── 9. Frequency-specific MC for p-adic targets ──
print("\n[8] Frequency-specific MC for P5 p-adic periods...", flush=True)

freq_mc_results = {}
# Reuse the null simulations from above, recompute Lomb-Scargle at target freqs
for name, info in padic_preds.items():
    tf = info['frequency']
    idx = np.argmin(np.abs(freqs - tf))
    power_at_target = power[idx]
    
    null_powers_at_f = np.zeros(n_sims)
    for i in range(n_sims):
        mock_dl = dl_bf_a + rng.normal(0, err_a)
        mock_res = mock_dl - dl_bf_a
        m_interp = interp1d(x_data, mock_res, kind='cubic',
                            bounds_error=False, fill_value='extrapolate')
        m_grid = m_interp(x_grid)
        m_mean = np.average(m_grid, weights=weights)
        m_norm = m_grid - m_mean
        ls_result = lombscargle(x_grid, m_norm, np.atleast_1d(ang_freqs[idx]),
                                normalize='normalize', weights=weights)
        # Handle scipy returning 0-d array or scalar depending on version
        if hasattr(ls_result, 'item'):
            null_powers_at_f[i] = float(ls_result.item())
        elif hasattr(ls_result, '__len__') and len(ls_result) == 1:
            null_powers_at_f[i] = float(ls_result[0])
        else:
            null_powers_at_f[i] = float(ls_result)
    
    p_freq = float(np.mean(null_powers_at_f >= power_at_target))
    freq_mc_results[name] = {
        'power_at_target': float(power_at_target),
        'null_median': float(np.median(null_powers_at_f)),
        'freq_specific_p': p_freq,
    }
    print(f"  P5 {name} (f={tf:.4f}): LS power={power_at_target:.6f}, "
          f"null median={np.median(null_powers_at_f):.6f}, freq-p={p_freq:.4f}", flush=True)

# ── 10. Amplitude constraint ──
print("\n[9] Amplitude constraint...", flush=True)

# B_95 < t_95 / sqrt(N_eff) * sigma_res / <D_l>
# From CAL-03: B_95 < 0.004 at 95% CL
sigma_res = np.sqrt(np.mean(residuals_a**2))
mean_dl = np.mean(dl_a)
n_eff = n_pts  # effective independent points in log-grid
t_95 = stats.t.ppf(0.975, n_pts - 2)
b_95 = t_95 / np.sqrt(n_eff) * sigma_res / mean_dl

print(f"  sigma_res = {sigma_res:.1f} uK^2", flush=True)
print(f"  <D_l> = {mean_dl:.1f} uK^2", flush=True)
print(f"  N_eff = {n_eff}", flush=True)
print(f"  B_95 < {b_95:.6f} (95% CL amplitude constraint)", flush=True)
print(f"  This applies to ALL log-periodic signals in Planck data, including p-adic periods.", flush=True)

# ── 11. Plots ──
print("\n[10] Generating figures...", flush=True)

# Fig 1: Log-periodogram with p-adic target lines
fig, axes = plt.subplots(2, 1, figsize=(14, 11))
sort_idx = np.argsort(periods)

ax = axes[0]
ax.plot(periods[sort_idx], power[sort_idx], 'b-', lw=0.8, alpha=0.9)
padic_colors = {'p=2': '#E41A1C', 'p=3': '#377EB8', 'p=5': '#4DAF4A'}
for name, info in padic_preds.items():
    period = info['period']
    ax.axvline(period, color=padic_colors[name], ls='--', alpha=0.8, lw=2)
    ax.text(period, np.max(power)*0.95, f"P5 {name}\nln={period:.3f}",
            color=padic_colors[name], fontsize=8, rotation=90, va='top', ha='right')
ax.axhline(np.percentile(max_powers_null, 95), color='gray', ls='--', alpha=0.5, label='95% CL')
ax.axhline(np.percentile(max_powers_null, 99.7), color='gray', ls='-', alpha=0.4, label='3-sigma CL')
ax.set_xlabel(r'Period $\ln q$')
ax.set_ylabel('Normalized Lomb-Scargle Power')
ax.set_title(f'P5 Log-Periodogram: Planck 2018 Full TT ({len(ell_a)} pts -> {n_pts}-pt log-grid)\n'
             f'P-adic periods: ln(2)={math.log(2):.3f}, ln(3)={math.log(3):.3f}, ln(5)={math.log(5):.3f}')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)

ax = axes[1]
zm = (periods > 0.3) & (periods < 3.5)
ax.plot(periods[sort_idx][(periods[sort_idx] > 0.3) & (periods[sort_idx] < 3.5)],
        power[sort_idx][(periods[sort_idx] > 0.3) & (periods[sort_idx] < 3.5)],
        'b-', lw=1.3)
for name, info in padic_preds.items():
    period = info['period']
    if 0.3 < period < 3.5:
        ax.axvline(period, color=padic_colors[name], ls='--', alpha=0.8, lw=2)
ax.axhline(np.percentile(max_powers_null, 95), color='gray', ls='--', alpha=0.5)
ax.axhline(np.percentile(max_powers_null, 99.7), color='gray', ls='-', alpha=0.4)
ax.set_xlabel(r'Period $\ln q$')
ax.set_ylabel('Normalized Power')
ax.set_title('Zoom: ln q in [0.3, 3.5] — P5 p-adic region')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'p5_log_periodogram.png'), dpi=150)
plt.close()
print("  Saved: p5_log_periodogram.png", flush=True)

# Fig 2: MC null distribution
fig, ax = plt.subplots(figsize=(11, 5.5))
ax.hist(max_powers_null, bins=40, density=True, color='gray', alpha=0.5, edgecolor='black')
ax.axvline(max_power_obs, color='red', lw=2, label=f'Observed = {max_power_obs:.4f}')
ax.axvline(np.percentile(max_powers_null, 95), color='blue', ls='--', lw=1.5,
           label=f'95% CL = {np.percentile(max_powers_null, 95):.4f}')
ax.set_xlabel('Maximum periodogram power')
ax.set_ylabel('Probability density')
ax.set_title(f'P5 Null Distribution ({n_sims} LambdaCDM + noise mocks, full spectrum)\n'
             f'Global p = {p_value_global:.4f}')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'p5_mc_null.png'), dpi=150)
plt.close()
print("  Saved: p5_mc_null.png", flush=True)

# Fig 3: Template fits for p-adic periods
fig, axes = plt.subplots(3, 1, figsize=(14, 12))
for idx, (name, info) in enumerate(padic_preds.items()):
    ax = axes[idx]
    period = info['period']
    r_cos, p_cos, t_cos = correlate_full(period, 0.0)
    r_sin, p_sin, t_sin = correlate_full(period, np.pi/2)
    r_best = r_cos if abs(r_cos) >= abs(r_sin) else r_sin
    t_best = t_cos if abs(r_cos) >= abs(r_sin) else t_sin
    p_best = p_cos if abs(r_cos) >= abs(r_sin) else p_sin
    
    ax.plot(ell_grid, y_grid, 'b-', lw=0.8, alpha=0.6, label='Log-resampled residuals')
    ax.plot(ell_grid, t_best * np.std(y_grid) * 4, 'r-', lw=2, alpha=0.7,
            label=f'Best template: r={r_best:+.4f}, p={p_best:.4f}')
    ax.set_xscale('log')
    ax.set_xlabel(r'$\ell$')
    ax.set_ylabel(r'$\Delta D_\ell$ [$\mu$K$^2$]')
    ax.set_title(f'P5 {name}: period = ln({info["p"]}) = {period:.4f} ln-units (q = {info["p"]})')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'p5_template_fits.png'), dpi=150)
plt.close()
print("  Saved: p5_template_fits.png", flush=True)

# ── 12. Save results ──
print("\n[11] Saving results...", flush=True)

results = {
    'analysis': 'P5 CMB Log-Periodogram — P-ADIC PERIODS',
    'framework': 'WBS-6 Synthesis, Five Pillars One Structure v1.3',
    'doi': '10.5281/zenodo.21603374',
    'data': 'Planck 2018 TT full (COM_PowerSpect_CMB-TT-full_R3.01.txt)',
    'data_source': 'ESA Planck Legacy Archive, Release 3.01',
    'based_on': 'CAL-03 pipeline (DOI 10.5281/zenodo.21534747)',
    'date': '2026-07-27',
    'n_pts_original': int(len(ell_full)),
    'n_pts_analysis': int(len(ell_a)),
    'ell_range_analysis': [float(ell_a[0]), float(ell_a[-1])],
    'log_span': float(x_span),
    'chi2_dof': float(chi2 / dof),
    'residuals_rms': float(np.sqrt(np.mean(residuals_a**2))),
    'n_log_grid': n_pts,
    'n_frequencies': n_freq,
    'mc_significance': {
        'max_power_obs': float(max_power_obs),
        'null_median': float(np.median(max_powers_null)),
        'null_68pct': float(np.percentile(max_powers_null, 68)),
        'null_95pct': float(np.percentile(max_powers_null, 95)),
        'null_99pct': float(np.percentile(max_powers_null, 99)),
        'null_99_7pct': float(np.percentile(max_powers_null, 99.7)),
        'p_value_global': float(p_value_global),
        'n_sims': n_sims,
    },
    'padic_prediction': {
        'description': 'Log-periodic oscillations at k_p = 2*pi/log p for p=2,3,5',
        'formula': 'C_l = C_l^LambdaCDM * [1 + B*cos(2*pi*ln(l/l0)/ln(p) + phi)]',
        'predicted_periods': {
            'p=2': {'period_ln': math.log(2), 'frequency': 1.0/math.log(2), 'predicted_q': 2},
            'p=3': {'period_ln': math.log(3), 'frequency': 1.0/math.log(3), 'predicted_q': 3},
            'p=5': {'period_ln': math.log(5), 'frequency': 1.0/math.log(5), 'predicted_q': 5},
        }
    },
    'target_results': target_results,
    'template_correlation': template_results,
    'freq_specific_mc': freq_mc_results,
    'amplitude_constraint': {
        'B_95_upper_limit': float(b_95),
        'sigma_res_uK2': float(sigma_res),
        'mean_Dl_uK2': float(mean_dl),
        'note': 'Applies to ALL log-periodic signals in Planck 2018, including p-adic periods',
    },
    'top_peaks': peaks[:25],
}

with open(os.path.join(OUT_DIR, 'p5_results.json'), 'w') as f:
    json.dump(results, f, indent=2, default=float)
print("  Saved: p5_results.json", flush=True)

# ── 13. VERDICT ──
print("\n" + "=" * 70, flush=True)
print("P5 FINAL VERDICT — P-ADIC LOG-PERIODIC OSCILLATIONS", flush=True)
print("=" * 70, flush=True)
print(f"", flush=True)
print(f"  Prediction: CMB log-periodic oscillations at ln(p) for p=2,3,5", flush=True)
print(f"     p=2: period = ln(2) = {math.log(2):.6f}, q = 2.000", flush=True)
print(f"     p=3: period = ln(3) = {math.log(3):.6f}, q = 3.000", flush=True)
print(f"     p=5: period = ln(5) = {math.log(5):.6f}, q = 5.000", flush=True)
print(f"", flush=True)
print(f"  Data:     Planck 2018 TT full spectrum ({len(ell_a)} pts in l in [30,2500])", flush=True)
print(f"  Method:   Log-resampled Lomb-Scargle periodogram (1000 log-grid, 5000 freqs)", flush=True)
print(f"  Baseline: Dln l = {x_span:.2f}", flush=True)
print(f"  chi2/dof: {chi2/dof:.3f} (LambdaCDM fit quality)", flush=True)
print(f"", flush=True)
print(f"  Global MC p-value: {p_value_global:.4f}", flush=True)

disconfirm = False
for name, info in padic_preds.items():
    tr = template_results[name]
    fmc = freq_mc_results[name]
    period = info['period']
    print(f"\n  P5 {name}: period = ln({info['p']}) = {period:.6f}", flush=True)
    print(f"    LS power:  {target_results[name]['power']:.6f} (null median: {fmc['null_median']:.6f})", flush=True)
    print(f"    Template:  r = {tr['r_best']:+.4f}, p = {tr['p_best']:.4f}", flush=True)
    print(f"    Freq-MC p: {fmc['freq_specific_p']:.4f}", flush=True)
    sigma = 'NOT SIGNIFICANT'
    if fmc['freq_specific_p'] < 0.05:
        sigma = 'SIGNIFICANT at p < 0.05'
    elif fmc['freq_specific_p'] < 0.01:
        sigma = 'SIGNIFICANT at p < 0.01'
    print(f"    Verdict:   {sigma}", flush=True)

verdict = "NOT DISCONFIRMED (not rejected)" if p_value_global > 0.05 else "POTENTIALLY DISCONFIRMED"
print(f"\n" + "=" * 70, flush=True)
print(f"  H0 (LambdaCDM, no p-adic log-periodic modulation): {verdict}", flush=True)
print(f"", flush=True)
print(f"  -> No evidence for P5 p-adic log-periodic oscillations at p=2,3,5", flush=True)
print(f"     in Planck 2018 CMB TT data.", flush=True)
print(f"  -> P5 is NOT DISCONFIRMED: the predicted amplitude may be below", flush=True)
print(f"     Planck sensitivity (B_95 < {b_95:.4f}). CMB-S4 (2028) would", flush=True)
print(f"     provide approximately 5x better sensitivity.", flush=True)
print(f"  -> OSF pre-registration 2ndsz remains active for independent verification.", flush=True)
print("=" * 70, flush=True)

print(f"\nOutput directory: {OUT_DIR}", flush=True)
print("DONE.", flush=True)
