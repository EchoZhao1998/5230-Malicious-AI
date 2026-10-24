# Rebuilds figB from REPORT_m4.zip -> partB_scores.csv (the notebook's own figure has a clipped x-label).
# Usage: python3 make_figB.py path/to/partB_scores.csv
import sys, numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
s = pd.read_csv(sys.argv[1])
calib = s[s.group == 'clean (held-out, calibration)'].score
thr = np.percentile(calib, 5)
order = ['clean (held-out, calibration)', 'clean (test)', 'protected (N)', 'washed · A · IMPRESS 100 it.',
         'washed · C · A + mask', 'washed · D · diffusion 0.1 + mask', 'washed · D · diffusion 0.2 + mask']
label = {'clean (held-out, calibration)': 'clean, held-out (40)', 'clean (test)': 'clean, test (10)',
         'protected (N)': 'protected, N', 'washed · A · IMPRESS 100 it.': 'washed, A (IMPRESS)',
         'washed · C · A + mask': 'washed, C (A + mask)', 'washed · D · diffusion 0.1 + mask': 'washed, D 0.1',
         'washed · D · diffusion 0.2 + mask': 'washed, D 0.2'}
fig, ax = plt.subplots(figsize=(7.0, 3.4))
rng = np.random.default_rng(0)
for i, g in enumerate(order[::-1]):
    v = s[s.group == g].score.values
    c = '#9e9e9e' if g.startswith('clean') else '#c98b2b' if g.startswith('protected') else '#1f6fd1'
    ax.scatter(v, i + rng.uniform(-.15, .15, len(v)), s=18, color=c, edgecolor='white', lw=.5, zorder=3)
ax.axvline(thr, color='#222', ls='--', lw=1)
ax.text(thr * 0.88, -.6, f'pre-set threshold {thr:.3f} (5% of held-out clean)', fontsize=7, ha='right', color='#222')
cmax = s[s.group.str.startswith('clean')].score.max()
ax.axvline(cmax, color='#9e9e9e', ls=':', lw=1)
ax.text(cmax * 1.08, -.6, f'highest clean = {cmax:.2f}', fontsize=7, color='#555')
ax.set_xscale('log'); ax.set_yticks(range(len(order))); ax.set_yticklabels([label[g] for g in order[::-1]], fontsize=8)
ax.set_xlabel('VAE round-trip error, 10th-percentile 32×32 patch (×1000, log scale)', fontsize=8)
ax.tick_params(axis='x', labelsize=7); ax.set_ylim(-1, len(order) - .3)
ax.grid(axis='x', alpha=.3); ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(); fig.savefig('figures/figB_detector_rebuilt.png', dpi=200, bbox_inches='tight')
print('threshold', round(thr, 4), '| clean max', cmax, '| A min', s[s.group.str.contains('A ·')].score.min())
