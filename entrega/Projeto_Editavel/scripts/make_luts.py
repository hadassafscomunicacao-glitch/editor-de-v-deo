"""Bake the per-pixel colour transforms of the grade into two 65^3 .cube LUTs:
   fg.cube (subjects)  and  bg.cube (background). Spatial parts (matte blend, local contrast, vignette) stay in the ffmpeg graph."""
import numpy as np, sys
sys.path.insert(0, 'project')
from grade import WB_GAIN, MASTER, LUMA
N = 65
g = np.linspace(0, 1, N, dtype=np.float32)
b_, g_, r_ = np.meshgrid(g, g, g, indexing='ij')          # .cube order: R fastest, then G, then B
rgb = np.stack([r_, g_, b_], -1).reshape(-1, 3)

def curve(x): return MASTER[np.clip((x * 4095).astype(np.int32), 0, 4095)]

def fg(x, gain=1.0, vib=0.08):
    x = x * WB_GAIN * gain
    x = curve(np.clip(x, 0, 1))
    y = x @ LUMA; sat = np.abs(x - y[:, None]).max(-1)
    v = 1 + vib * (1 - np.clip(sat * 3, 0, 1))
    return np.clip(y[:, None] + (x - y[:, None]) * v[:, None], 0, 1)

def bg(x, gain=0.66, s=0.82):
    x = x * WB_GAIN
    y = x @ LUMA
    x = (y[:, None] + (x - y[:, None]) * s) * gain
    x = x + np.array([-0.006, 0.0, 0.010], np.float32) * (1 - np.clip(y, 0, 1))[:, None]
    return curve(np.clip(x, 0, 1))

def write(path, out):
    with open(path, 'w') as f:
        f.write(f'TITLE "{path}"\nLUT_3D_SIZE {N}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
        for r, gg, b in out: f.write(f'{r:.6f} {gg:.6f} {b:.6f}\n')
write('project/fg.cube', fg(rgb))
write('project/bg.cube', bg(rgb))
print('luts written')
