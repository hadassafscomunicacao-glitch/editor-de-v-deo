"""Color grade: technical correction first, then a restrained cinematic look.
The person matte separates subjects from the background so the background can be
darkened/cooled without touching skin. Float32 RGB in [0,1]."""
import numpy as np, cv2
from scipy.interpolate import PchipInterpolator

LUMA = np.array([0.2126, 0.7152, 0.0722], np.float32)
# 1) technical: neutralise the warm cast measured on the grey curtain (R 81 / G 78 / B 72), keep a hint of warmth
WB_GAIN = np.array([0.962, 1.0, 1.055], np.float32)
# 2) look: filmic S-curve — deeper (not crushed) blacks, protected mids, soft highlight roll-off
_x = np.linspace(0, 1, 4096, dtype=np.float32)
MASTER = PchipInterpolator([0, .06, .20, .45, .70, .88, 1.0], [0.012, .035, .17, .46, .735, .895, .965])(_x).astype(np.float32)

DEFAULT = dict(bg_gain=0.66, bg_sat=0.82, fg_gain=1.0, fg_clarity=0.16, vignette=0.20, skin_vib=0.08)

def _vignette(H, W, amount):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W * 0.5) / (W * 0.62)) ** 2 + ((yy - H * 0.42) / (H * 0.58)) ** 2)
    return (1 - amount * np.clip((r - 0.55) / 0.6, 0, 1) ** 2).astype(np.float32)

_VIG = {}
def grade_frame(rgb, matte, p=DEFAULT):
    H, W = matte.shape
    x = rgb * WB_GAIN
    y = cv2.transform(x, LUMA.reshape(1, 3))[..., 0] if False else x @ LUMA
    # subject presence: large-radius local contrast, only on subjects
    if p['fg_clarity']:
        small = cv2.resize(y, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        blur = cv2.resize(cv2.GaussianBlur(small, (0, 0), 4.5), (W, H), interpolation=cv2.INTER_LINEAR)
        x += (p['fg_clarity'] * (y - blur) * matte)[..., None]
    gain = p['bg_gain'] + (p['fg_gain'] - p['bg_gain']) * matte
    bgw = 1 - matte
    y = x @ LUMA
    # background: darker, slightly desaturated, faint cool tint in its shadows (depth)
    s = 1 - (1 - p['bg_sat']) * bgw
    x = (y[..., None] + (x - y[..., None]) * s[..., None]) * gain[..., None]
    x += np.array([-0.006, 0.0, 0.010], np.float32) * (bgw * (1 - np.clip(y, 0, 1)))[..., None]
    np.clip(x, 0, 1, out=x)
    x = MASTER[(x * 4095).astype(np.int32)]
    if p['skin_vib']:
        y = x @ LUMA
        sat = np.abs(x - y[..., None]).max(-1)
        vib = 1 + p['skin_vib'] * (1 - np.clip(sat * 3, 0, 1)) * matte
        x = y[..., None] + (x - y[..., None]) * vib[..., None]
    if p['vignette']:
        key = (H, W, p['vignette'])
        if key not in _VIG: _VIG[key] = _vignette(H, W, p['vignette'])
        x *= _VIG[key][..., None]
    return np.clip(x, 0, 1, out=x)
