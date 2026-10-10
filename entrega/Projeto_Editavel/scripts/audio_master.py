"""Edit + finish the dialogue audio according to the plan, then mix sound effects.
1) assemble kept source intervals (48 kHz) with short equal-power crossfades at every splice
2) per-speaker level balance (Hellen measured ~2.6 LU quieter than Indira)
3) ffmpeg chain: HPF, gentle denoise, corrective EQ (de-box 250 Hz, presence, air), de-esser, moderate compression, limiter
4) two-pass EBU R128 loudness normalisation to -14 LUFS / -1 dBTP
5) mix SFX (synthesised, original) at their cue times
Usage: python project/audio_master.py plan.json out.wav"""
import json, sys, subprocess, numpy as np, soundfile as sf
P = json.load(open(sys.argv[1])); OUT = sys.argv[2]
SR = 48000; FPS = 30
x, sr = sf.read('audio/orig48k.wav', dtype='float32'); assert sr == SR
x = x.mean(1)  # source is dual-mono
segs = P['audio_edl'] if 'audio_edl' in P else [[a / FPS, b / FPS] for a, b in P['edl']]
XF = int(0.012 * SR)          # 12 ms equal-power crossfade centred on every splice (length-preserving)
h = XF // 2
t = np.linspace(0, np.pi / 2, XF, dtype=np.float32)
fo, fi = np.cos(t), np.sin(t)
total = sum(int(round(b * SR)) - int(round(a * SR)) for a, b in segs)
out = np.zeros(total, np.float32)
pos = 0
for k, (a, b) in enumerate(segs):
    i0, i1 = int(round(a * SR)), int(round(b * SR))
    L = i1 - i0
    # take h extra samples on each side from the source (natural continuation) for the crossfades
    src = x[max(0, i0 - h):min(len(x), i1 + h)]
    pad_l = h - (i0 - max(0, i0 - h)); src = np.concatenate([np.zeros(pad_l, np.float32), src])
    src = np.concatenate([src, np.zeros(L + 2 * h - len(src), np.float32)])
    env = np.ones(L + 2 * h, np.float32)
    if k > 0: env[:XF] = fi
    else: env[:h] = 0
    if k < len(segs) - 1: env[-XF:] = fo
    else: env[-h:] = 0
    o0 = pos - h
    seg = src * env
    a0 = max(0, o0); a1 = min(total, o0 + len(seg))
    out[a0:a1] += seg[a0 - o0:a1 - o0]
    pos += L
# per-speaker gain envelope on output timeline
gain = np.ones(len(out), np.float32)
for g in P.get('speaker_gain', []):   # {t0,t1,db} output seconds
    i0, i1 = int(g['t0'] * SR), int(g['t1'] * SR)
    gain[i0:i1] = 10 ** (g['db'] / 20)
k = int(0.06 * SR); ker = np.ones(k, np.float32) / k
gain = np.convolve(gain, ker, mode='same')
out *= gain
sf.write('audio/edit_raw.wav', out, SR, subtype='FLOAT')
chain = ("highpass=f=75:p=2,afftdn=nr=4:nf=-62:tn=1,"
         "equalizer=f=250:t=q:w=1.3:g=-2,equalizer=f=800:t=q:w=1.4:g=-1,"
         "equalizer=f=3200:t=q:w=1.0:g=2.5,highshelf=f=8000:g=1.5,lowshelf=f=160:g=1,"
         "deesser=i=0.2:m=0.5:f=0.5,"
         "acompressor=threshold=0.125:ratio=2:attack=10:release=160:knee=4:makeup=1.25,"
         "alimiter=limit=0.89:attack=3:release=60:level=disabled,aformat=channel_layouts=stereo")
subprocess.run(['ffmpeg', '-v', 'error', '-i', 'audio/edit_raw.wav', '-af', chain, '-ar', '48000', '-c:a', 'pcm_f32le', '-y', 'audio/edit_proc.wav'], check=True)
# loudness pass 1
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', 'audio/edit_proc.wav', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
js = r.stderr[r.stderr.rfind('{'):r.stderr.rfind('}') + 1]; m = json.loads(js)
ln = (f"loudnorm=I=-14:TP=-1.0:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
      f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=summary")
subprocess.run(['ffmpeg', '-v', 'error', '-i', 'audio/edit_proc.wav', '-af', ln, '-ar', '48000', '-c:a', 'pcm_f32le', '-y', 'audio/dialogue_master.wav'], check=True)
mix, _ = sf.read('audio/dialogue_master.wav', dtype='float32')
if mix.ndim == 1: mix = np.stack([mix, mix], 1)
for c in P.get('sfx', []):   # {t, file, db}
    s, ssr = sf.read(c['file'], dtype='float32'); assert ssr == SR
    if s.ndim == 1: s = np.stack([s, s], 1)
    i0 = int(c['t'] * SR); i1 = min(len(mix), i0 + len(s))
    mix[i0:i1] += s[:i1 - i0] * 10 ** (c.get('db', -18) / 20)
peak = np.abs(mix).max()
if peak > 0.89:   # SFX transients only: soft-clip-free safety gain on the whole mix would change loudness, so limit locally
    over = np.abs(mix) > 0.89
    mix = np.where(over, np.sign(mix) * (0.89 + (np.abs(mix) - 0.89) * 0.2), mix)
sf.write(OUT, mix, SR, subtype='PCM_24')
print('audio master', OUT, len(mix) / SR, 's')
