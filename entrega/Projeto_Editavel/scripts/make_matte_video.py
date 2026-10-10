"""Build the per-source-frame person matte video (gray, 540x960, lossless FFV1) from analysis/mattes.npy.
Mattes were computed every 2nd frame; in-between frames take the max of their neighbours (never darkens a moving hand),
then a 3-tap temporal median removes flicker. Edges: slight choke + feather (no halos)."""
import numpy as np, cv2, subprocess, sys
sys.path.insert(0, 'project')
from matte import CROP_Y0, CROP_Y1
M = np.load('analysis/mattes.npy', mmap_mode='r')
N_SRC = int(sys.argv[1]) if len(sys.argv) > 1 else 37357; STEP = 2
OUTP = sys.argv[2] if len(sys.argv) > 2 else 'analysis/matte_src.mkv'
W, H = 540, 960
y0, y1 = CROP_Y0 // 2, CROP_Y1 // 2
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                        '-c:v', 'ffv1', '-level', '3', '-threads', '2', '-y', OUTP], stdin=subprocess.PIPE)
kern = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
ramp = 20
def sample(k):
    k = min(max(k, 0), len(M) - 1)
    return M[k].astype(np.float32) / 255
prev = None
for i in range(N_SRC):
    k = i // STEP
    if i % STEP == 0:
        m = np.median(np.stack([sample(k - 1), sample(k), sample(k + 1)]), 0)
    else:
        a = np.median(np.stack([sample(k - 1), sample(k), sample(k + 1)]), 0)
        b = np.median(np.stack([sample(k), sample(k + 1), sample(k + 2)]), 0)
        m = np.maximum(a, b)
    band = cv2.resize(m, (W, y1 - y0), interpolation=cv2.INTER_CUBIC)
    band = np.clip((band - 0.5) * 2.2 + 0.5, 0, 1)
    band[:ramp] *= np.linspace(0, 1, ramp)[:, None]; band[-ramp:] *= np.linspace(1, 0, ramp)[:, None]
    full = np.zeros((H, W), np.float32); full[y0:y1] = band
    full = cv2.erode(full, kern)
    full = cv2.GaussianBlur(full, (0, 0), 2.5)
    enc.stdin.write((full * 255 + .5).astype(np.uint8).tobytes())
    if i % 3000 == 0: print(i, flush=True)
enc.stdin.close(); enc.wait(); print('done')
