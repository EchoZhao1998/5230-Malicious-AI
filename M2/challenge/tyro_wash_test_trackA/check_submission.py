#!/usr/bin/env python3
"""
Tyro Wash Test - Track A : self-check your submission before you send it.

    python check_submission.py  path/to/your_protected_folder

Checks (no GPU, no downloads):
  1. all 10 filenames present, nothing extra
  2. every image is exactly 512 x 512 RGB PNG
  3. perceptual cost vs our clean image, so you know before we do:
        - always: PSNR;  SSIM as well if scikit-image is installed
        - if torch + lpips are installed: LPIPS, and whether you are inside
          the ranking budget of 0.10

Nothing here is scoring code for R_pipe - that runs on our side.
"""
import sys, os
from PIL import Image
import numpy as np

HERE  = os.path.dirname(os.path.abspath(__file__))
CLEAN = os.path.join(HERE, 'clean')
BUDGET = 0.10          # = our purifier's own pur_eps LPIPS allowance


def fail(msg):
    print(f'  FAIL  {msg}')
    return 1


def main(sub_dir):
    expected = sorted(os.listdir(CLEAN))
    got      = sorted(f for f in os.listdir(sub_dir) if not f.startswith('.'))
    errors = 0

    print(f'\nchecking {sub_dir}\n' + '-' * 60)

    missing = set(expected) - set(got)
    extra   = set(got) - set(expected)
    if missing: errors += fail(f'missing {len(missing)}: {sorted(missing)}')
    if extra:   errors += fail(f'unexpected files: {sorted(extra)}')
    if not missing and not extra:
        print(f'  ok    all {len(expected)} filenames present, none extra')

    rows, _no_ssim = [], []
    for n in expected:
        if n in missing:
            continue
        p = os.path.join(sub_dir, n)
        im = Image.open(p)
        if im.size != (512, 512):
            errors += fail(f'{n}: size {im.size}, must be (512, 512)')
            continue
        if im.mode != 'RGB':
            print(f'  note  {n}: mode {im.mode}, will be converted to RGB')
        a = np.asarray(im.convert('RGB')).astype(np.float64)
        b = np.asarray(Image.open(os.path.join(CLEAN, n)).convert('RGB')).astype(np.float64)
        mse  = float(np.mean((a - b) ** 2))
        psnr = 99.0 if mse == 0 else 10 * np.log10(255.0 ** 2 / mse)
        try:
            from skimage.metrics import structural_similarity as ssim_fn
            ssim = float(ssim_fn(a, b, channel_axis=2, data_range=255))
        except ImportError:
            ssim = float('nan')
            _no_ssim.append(n)
        rows.append((n, ssim, psnr, a, b))

    if rows:
        print(f'\n  {"image":<22}{"SSIM":>8}{"PSNR":>9}')
        for n, s, p_, *_ in rows:
            print(f'  {n:<22}{s:>8.4f}{p_:>9.2f}')
        print(f'  {"mean":<22}{np.mean([r[1] for r in rows]):>8.4f}'
              f'{np.mean([r[2] for r in rows]):>9.2f}')
    if _no_ssim:
        print('\n  note  SSIM shown as nan: scikit-image is not installed.'
              '\n        pip install scikit-image   (PSNR and LPIPS above are unaffected)')

    # --- LPIPS: the axis we actually rank on -------------------------------
    try:
        import torch, lpips
        net = lpips.LPIPS(net='alex')   # MUST match the scorer's net (notebook cell 8)
        vals = []
        for n, _, _, a, b in rows:
            t = lambda x: torch.from_numpy(x.transpose(2, 0, 1)[None]).float() / 127.5 - 1.0
            vals.append(float(net(t(a), t(b)).item()))
        m = float(np.mean(vals))
        print(f'\n  LPIPS (mean, vs clean) = {m:.4f}   budget = {BUDGET}')
        print('  -> INSIDE the budget, you will be ranked.' if m <= BUDGET else
              '  -> OVER the budget. Still plotted and discussed, but not ranked.')
    except ImportError:
        print(f'\n  LPIPS skipped (pip install lpips torch to check the {BUDGET} budget).')
        print('  Rough guide: SSIM below ~0.90 vs clean usually means you are over it.')

    print('\n' + ('  submission looks valid.' if errors == 0
                  else f'  {errors} problem(s) above - fix before sending.') + '\n')
    return errors


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(1 if main(sys.argv[1]) else 0)
