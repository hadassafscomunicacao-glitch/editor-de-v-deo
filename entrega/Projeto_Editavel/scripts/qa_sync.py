"""Lip-sync QC: in wide shots, correlate the active speaker's mouth motion with the audio envelope; report the best lag.
Usage: python project/qa_sync.py video.mp4 plan.json"""
import sys, json, subprocess, numpy as np, soundfile as sf
V, P = sys.argv[1], json.load(open(sys.argv[2]))
W, H, FPS = 1080, 1920, 30
subprocess.run(['ffmpeg', '-v', 'error', '-i', V, '-ac', '1', '-ar', '16000', '-y', '/tmp/qs.wav'], check=True)
a, sr = sf.read('/tmp/qs.wav', dtype='float32')
env = np.array([np.sqrt(np.mean(a[int(i / FPS * sr):int((i + 1) / FPS * sr)] ** 2)) for i in range(int(len(a) / sr * FPS))])
spk = None
wide = [f for f in P['framing'] if f['z0'] == 1.0 and f['z1'] == 1.0 and f['f1'] - f['f0'] > 240 and f.get('who', -1) in (0, 1)]
split_frames = set()
for s in P['splits']: split_frames.update(range(s['f0'] - s['tin'], s['f1'] + s['tout']))
res = []
for f in wide[::max(1, len(wide) // 12)]:
    a0, a1 = f['f0'] + 10, min(f['f1'] - 10, f['f0'] + 10 + 300)
    if any(x in split_frames for x in range(a0, a1)): continue
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{a0 / FPS:.3f}', '-i', V, '-frames:v', str(a1 - a0), '-vf', 'format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
    box = (slice(880, 960), slice(260, 380)) if f['who'] == 0 else (slice(835, 915), slice(760, 880))
    m = np.abs(np.diff(fr[:, box[0], box[1]], axis=0)).mean((1, 2))
    e = np.abs(np.diff(env[a0:a0 + len(fr)]))[:len(m)]
    m = (m - m.mean()) / (m.std() + 1e-9); e = (e - e.mean()) / (e.std() + 1e-9)
    lags = range(-8, 9)
    cc = [np.mean(m[max(0, L):len(m) + min(0, L)] * e[max(0, -L):len(e) - max(0, L)]) for L in lags]
    best = list(lags)[int(np.argmax(cc))]
    res.append({'t': round(a0 / FPS, 1), 'who': ['Indira', 'Hellen'][f['who']], 'best_lag_frames': best, 'corr': round(float(max(cc)), 3)})
print(json.dumps(res, indent=0))
lags = [r['best_lag_frames'] for r in res if r['corr'] > 0.15]
print('median lag (frames, + = video late):', float(np.median(lags)) if lags else None, 'n =', len(lags))
