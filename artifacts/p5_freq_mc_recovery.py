"""
P5 Recovery: Frequency-Specific MC for p-adic periods.
Runs 200 simulations, computing null power at all 3 p-adic frequencies in one pass.
"""
import numpy as np
from scipy.signal import lombscargle
from scipy.interpolate import interp1d
import math, time

DATA_DIR = r"D:\qnfoworkspace\research\harmonische-paradigma\cal03\data"

# Load data
full_data = np.loadtxt(DATA_DIR + r'\COM_PowerSpect_CMB-TT-full_R3.01.txt', comments='#')
ell_full, dl_full, err_m, err_p = full_data[:, 0], full_data[:, 1], full_data[:, 2], full_data[:, 3]
errors_full = (err_m + err_p) / 2.0

theory_full = np.loadtxt(DATA_DIR + r'\planck_tt_bestfit.txt', comments='#')
bf_interp = interp1d(theory_full[:, 0].astype(int), theory_full[:, 1], kind='cubic', bounds_error=False, fill_value='extrapolate')
dl_bf_full = bf_interp(ell_full)

mask = (ell_full >= 30) & (ell_full <= 2500)
ell_a, dl_a, err_a, dl_bf_a = ell_full[mask], dl_full[mask], errors_full[mask], dl_bf_full[mask]

x_data = np.log(ell_a)
x_grid = np.linspace(np.log(30), np.log(2500), 1000)
e_interp = interp1d(x_data, err_a, kind='cubic', bounds_error=False, fill_value='extrapolate')
weights = 1.0 / (e_interp(x_grid) ** 2)
weights /= np.mean(weights)

# Residuals
r_interp_val = interp1d(x_data, dl_a - dl_bf_a, kind='cubic', bounds_error=False, fill_value='extrapolate')
y_grid = r_interp_val(x_grid)
y_mean = np.average(y_grid, weights=weights)
y_norm = y_grid - y_mean

# Target frequencies
targets = {
    'p=2': {'period': math.log(2), 'q': 2},
    'p=3': {'period': math.log(3), 'q': 3},
    'p=5': {'period': math.log(5), 'q': 5},
}
for name, tgt in targets.items():
    tgt['freq'] = 1.0 / tgt['period']
    tgt['ang_freq'] = 2 * np.pi * tgt['freq']

print("P5 Frequency-Specific MC Recovery (all 3 targets, single pass)", flush=True)
print("=" * 60, flush=True)

# Observed powers
for name, tgt in targets.items():
    pw = float(lombscargle(x_grid, y_norm, np.atleast_1d(tgt['ang_freq']),
                           normalize='normalize', weights=weights).item())
    tgt['obs_power'] = pw
    print(f"  {name} (q={tgt['q']}, f={tgt['freq']:.4f}): LS power = {pw:.6f}", flush=True)

# Run 200 null simulations
n_sims = 200
null_powers = {name: np.zeros(n_sims) for name in targets}
rng = np.random.default_rng(42)

print(f"\n  Running {n_sims} LambdaCDM+noise mocks...", flush=True)
t0 = time.time()
for i in range(n_sims):
    if (i+1) % 50 == 0:
        print(f"    {i+1}/{n_sims} ({time.time()-t0:.0f}s)...", flush=True)
    
    mock_dl = dl_bf_a + rng.normal(0, err_a)
    mock_res = mock_dl - dl_bf_a
    m_interp = interp1d(x_data, mock_res, kind='cubic', bounds_error=False, fill_value='extrapolate')
    m_grid = m_interp(x_grid)
    m_mean = np.average(m_grid, weights=weights)
    m_norm = m_grid - m_mean
    
    for name, tgt in targets.items():
        null_powers[name][i] = float(lombscargle(x_grid, m_norm, np.atleast_1d(tgt['ang_freq']),
                                                  normalize='normalize', weights=weights).item())

t_elapsed = time.time() - t0
print(f"  Done in {t_elapsed:.1f}s", flush=True)

# Results
print(f"\n{'Target':>6s}  {'Period':>8s}  {'q':>4s}  {'LS Power':>10s}  {'Null Med':>10s}  {'Freq-MC p':>10s}  {'Verdict':>20s}", flush=True)
print("-" * 80, flush=True)

for name, tgt in targets.items():
    pw = tgt['obs_power']
    null_med = float(np.median(null_powers[name]))
    p_freq = float(np.mean(null_powers[name] >= pw))
    
    verdict = 'NOT SIGNIFICANT'
    if p_freq < 0.05:
        verdict = 'SIGNIFICANT (p<0.05) — BONFERRONI CORRECTION NEEDED'
    if p_freq < 0.01:
        verdict = 'SIGNIFICANT (p<0.01)'
    
    print(f"  {name:6s}  {tgt['period']:8.4f}  {tgt['q']:4d}  {pw:10.6f}  {null_med:10.6f}  {p_freq:10.4f}  {verdict:20s}", flush=True)

# Bonferroni: 3 targets x 2 phases = 6 tests
print(f"\n  Bonferroni threshold (6 tests): p < 0.05/6 = 0.0083", flush=True)
print(f"\nDONE.", flush=True)
