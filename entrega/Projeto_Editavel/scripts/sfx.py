"""Original, synthesized sound effects (no third-party samples -> no licensing issues). 48 kHz stereo WAV."""
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
SR = 48000
rng = np.random.default_rng(7)
def st(x, w=0.0004):  # tiny inter-channel delay for width
    d = int(w * SR); return np.stack([x, np.concatenate([np.zeros(d), x[:-d]])], 1)
def norm(x, peak_db): return x / (np.abs(x).max() + 1e-9) * 10 ** (peak_db / 20)

def ding(f0=1175.0, dur=1.6):
    t = np.arange(int(dur * SR)) / SR
    y = np.zeros_like(t)
    for ratio, amp, dec in [(1, 1, 1.1), (2.0, .25, .7), (2.76, .22, .5), (5.4, .07, .25)]:
        y += amp * np.sin(2 * np.pi * f0 * ratio * t) * np.exp(-t / dec * 2.2)
    att = np.clip(t / .004, 0, 1); y *= att
    return st(norm(y, -6))

def whoosh(dur=0.75, up=True):
    n = int(dur * SR); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    out = np.zeros(n); blk = 512
    for i in range(0, n, blk):
        k = i / n; fc = (350 + 2200 * k) if up else (2500 - 2100 * k)
        sos = butter(2, [fc * .6, min(fc * 1.6, 20000)], btype='band', fs=SR, output='sos')
        out[i:i + blk] = sosfilt(sos, noise[max(0, i - 2048):i + blk])[-len(noise[i:i + blk]):]
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.6
    return st(norm(out * env, -9), .0011)

def tick():
    n = int(0.06 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * 2100 * t) * np.exp(-t / .012) + .4 * rng.standard_normal(n) * np.exp(-t / .004)
    sos = butter(2, 900, btype='high', fs=SR, output='sos'); y = sosfilt(sos, y)
    return st(norm(y, -14))

def motor(dur=1.3):
    n = int(dur * SR); t = np.arange(n) / SR
    noise = sosfilt(butter(2, [90, 420], btype='band', fs=SR, output='sos'), rng.standard_normal(n))
    hum = .35 * np.sin(2 * np.pi * 110 * t) + .15 * np.sin(2 * np.pi * 220 * t)
    env = np.clip(t / .25, 0, 1) * np.clip((dur - t) / .35, 0, 1)
    return st(norm((noise + hum) * env, -12))

def soft_impact():
    n = int(0.9 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * (70 + 40 * np.exp(-t / .05)) * t) * np.exp(-t / .22)
    y += .15 * sosfilt(butter(2, 2500, fs=SR, output='sos'), rng.standard_normal(n)) * np.exp(-t / .03)
    return st(norm(y, -8))

for name, x in [('ding', ding()), ('whoosh_up', whoosh(up=True)), ('whoosh_down', whoosh(up=False)), ('tick', tick()), ('motor', motor()), ('impact', soft_impact())]:
    sf.write(f'project/sfx/{name}.wav', x.astype(np.float32), SR, subtype='FLOAT')
print('ok')
