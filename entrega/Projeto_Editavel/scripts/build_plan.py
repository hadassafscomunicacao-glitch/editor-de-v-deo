"""Turn (cuts + visual map + speaker labels) into a render plan:
 EDL (frames), framing/reframing per shot, overlays + graphics render jobs, split-screen windows, SFX cues, subtitle words.
Usage: python project/build_plan.py [cuts.json] [edl_refined.json]"""
import json, sys, numpy as np, copy, re
sys.path.insert(0, '/home/user/work/project')
FPS = 30; NSRC = 37357; DUR = NSRC / FPS
W, H = 1080, 1920
cuts = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else []
cuts = sorted([[max(0, a), min(DUR, b)] for a, b in cuts if b > a])
# --- EDL in frames (each splice at a frame boundary; refined audio offsets handled in audio stage)
kept = []; t = 0.0
for a, b in cuts:
    if a > t: kept.append([t, a])
    t = max(t, b)
if t < DUR: kept.append([t, DUR])
edl = []
for a, b in kept:
    fa, fb = int(round(a * FPS)), int(round(b * FPS))
    if fb - fa >= 2: edl.append([fa, fb])
# merge adjacent
m = []
for a, b in edl:
    if m and a <= m[-1][1]: m[-1][1] = max(m[-1][1], b)
    else: m.append([a, b])
edl = m
audio_edl = [[a / FPS, b / FPS] for a, b in edl]
import os
if len(sys.argv) > 2 and os.path.exists(sys.argv[2]):      # refined, audio-aware EDL from finalize_cuts.py
    R = json.load(open(sys.argv[2])); edl = R['edl']; audio_edl = R['audio_edl']
out_starts = np.cumsum([0] + [b - a for a, b in edl])
NOUT = int(out_starts[-1])
def out_frame(src_t):
    f = src_t * FPS
    for k, (a, b) in enumerate(edl):
        if f < a: return float(out_starts[k])
        if a <= f < b: return float(out_starts[k] + (f - a))
    return float(NOUT)
def out_t(src_t): return out_frame(src_t) / FPS
splices = [int(out_starts[k]) for k in range(1, len(edl))]
# existing manual cuts in the footage (detected), mapped to output
SRC_CUTS = [34.00, 60.47, 62.67, 64.77, 80.03, 152.93, 353.53, 369.47, 409.40, 477.73, 530.03, 597.77, 630.40, 647.77, 677.63, 726.67, 749.33, 882.13, 1017.43, 1118.07]
bcam = (out_frame(62.67), out_frame(64.77))
# --- speakers (0 = Indira, left; 1 = Hellen, right; -1 unknown) per output frame
spk_sec = np.load('/home/user/work/analysis/speaker_per_second.npy')
src_of_out = np.concatenate([np.arange(a, b) for a, b in edl])
spk = spk_sec[np.clip((src_of_out / FPS).astype(int), 0, len(spk_sec) - 1)]
# --- visual cues -> overlays / jobs / splits / sfx
cues = json.load(open('/home/user/work/project/visual_map.json'))
def conv(obj, t0):
    if isinstance(obj, dict):
        if set(obj.keys()) == {'@t'}: return round(out_t(obj['@t']) - t0, 3)
        return {k: conv(v, t0) for k, v in obj.items()}
    if isinstance(obj, list): return [conv(v, t0) for v in obj]
    return obj
jobs, overlays, splits, sfx = [], [], [], []
SFXF = {'ding': 'project/sfx/ding.wav', 'whoosh_up': 'project/sfx/whoosh_up.wav', 'whoosh_down': 'project/sfx/whoosh_down.wav', 'tick': 'project/sfx/tick.wav', 'motor': 'project/sfx/motor.wav', 'impact': 'project/sfx/impact.wav'}
cues.sort(key=lambda c: c['start'])
# resolve overlaps between top-zone cues (name tags excluded): earlier cue exits before the next enters
tops = [c for c in cues if c['layout'] == 'top' and c['scene'] != 'nameTag']
for c, n in zip(tops, tops[1:]):
    if out_t(c['end']) > out_t(n['start']) - 0.05:
        c['end_out'] = out_t(n['start']) - 0.05
for c in cues:
    t0 = out_t(c['start']); t1 = c.get('end_out', out_t(c['end']))
    dur = round(t1 - t0, 3)
    if dur < 0.8: print('WARN short cue', c['id'], dur); continue
    params = conv(c['params'], t0); params['dur'] = dur
    jobs.append({'id': c['id'], 'scene': c['scene'], 'duration': dur, 'params': params})
    f0 = int(round(t0 * FPS))
    overlays.append({'id': c['id'], 'dir': f'/home/user/work/gfx/out/{c["id"]}', 'f0': f0, 'n': int(round(dur * FPS)), 'layout': c['layout'], 'z': 1 if c['layout'] == 'split' else 0})
    if c['layout'] == 'split':
        splits.append({'f0': f0 + 18, 'f1': f0 + int(round(dur * FPS)) - 18, 'tin': 18, 'tout': 18})
    for name, ts, db in c['sfx']:
        sfx.append({'t': round(out_t(ts), 3), 'file': SFXF[name], 'db': db, 'cue': c['id']})
# --- framing
words = json.load(open('/home/user/work/analysis/words.json'))
cutset = [(a, b) for a, b in cuts]
def kept_word(w): return not any(a - 0.01 <= (w['s'] + w['e']) / 2 <= b + 0.01 for a, b in cutset)
ow = [dict(w, os=out_t(w['s']), oe=out_t(w['e'])) for w in words if kept_word(w)]
bounds = sorted(set([0, NOUT] + splices + [int(out_frame(t)) for t in SRC_CUTS]))
# split long shots at sentence boundaries for rhythm (not mechanical: only at real pauses after a sentence/turn)
def sentence_points(f0, f1):
    pts = []
    for k in range(1, len(ow)):
        a, b = ow[k - 1], ow[k]
        fb = int(round(b['os'] * FPS))
        if f0 + 150 < fb < f1 - 150 and (b['os'] - a['oe']) >= 0.16 and re.search(r'[.?!]$', a['w']):
            pts.append(fb)
    return pts
shots = []
for f0, f1 in zip(bounds, bounds[1:]):
    if f1 - f0 < 1: continue
    seg = [f0]
    if f1 - f0 > 14 * FPS:
        pts = sentence_points(f0, f1); last = f0
        for p in pts:
            if p - last >= 8 * FPS and f1 - p >= 6 * FPS: seg.append(p); last = p
    seg.append(f1)
    for a, b in zip(seg, seg[1:]): shots.append([a, b, 'cut' if a in splices else 'shot'])
def top_overlay_frac(a, b):
    n = 0
    for o in overlays:
        if o['layout'] != 'split':
            n += max(0, min(b, o['f0'] + o['n']) - max(a, o['f0']))
    return n / max(1, b - a)
def in_split(a, b):
    return any(not (b <= s['f0'] - s['tin'] or a >= s['f1'] + s['tout']) for s in splits)
framing = []; state = 0
for k, (a, b, kind) in enumerate(shots):
    sp = spk[a:b]; sp = sp[sp >= 0]
    who = int(np.round(sp.mean())) if len(sp) else -1
    state = 1 - state
    if bcam[0] - 2 <= a <= bcam[1] + 2 or in_split(a, b):
        framing.append({'f0': a, 'f1': b, 'z0': 1.0, 'z1': 1.0, 'cx0': 540, 'cy0': 960, 'kind': kind}); continue
    topf = top_overlay_frac(a, b)
    if any(o['id'].startswith('v08_') and not (b <= o['f0'] or a >= o['f0'] + o['n']) for o in overlays):
        framing.append({'f0': a, 'f1': b, 'z0': 1.0, 'z1': 1.0, 'cx0': 540, 'cy0': 960, 'kind': kind, 'who': who}); state = 0; continue
    if state == 1:
        z0 = 1.0
    else:
        z0 = 1.13 if topf < 0.3 else 1.06
    cx = {0: 478, 1: 602}.get(who, 540) if z0 > 1.0 else 540
    cy = 905 if z0 > 1.0 else 960
    dur = (b - a) / FPS
    zmax = 1.08 if topf > 0.3 else 1.18
    z1 = min(zmax, z0 + (min(0.045, 0.004 * dur) if dur > 5 else 0))
    if z1 > 1.0 and z0 == 1.0: cx1, cy1 = ({0: 500, 1: 580}.get(who, 540), 930)
    else: cx1, cy1 = cx, cy
    framing.append({'f0': a, 'f1': b, 'z0': round(z0, 4), 'z1': round(z1, 4), 'cx0': cx, 'cy0': cy, 'cx1': cx1, 'cy1': cy1, 'ease': 'io', 'kind': kind, 'who': who})
# --- per-speaker level balance (Hellen measured ~2.6 LU below Indira): word-level speaker labels from diarization windows
DW = np.load('/home/user/work/analysis/diar_windows.npy')
def word_spk(w):
    m = (DW[:, 0] >= w['s'] - 0.3) & (DW[:, 0] <= w['e'] + 0.3)
    return int(np.round(DW[m, 1].mean())) if m.any() else -1
speaker_gain = []
run = None
for w in ow:
    sp_ = word_spk(w)
    if run and (sp_ == run['spk'] or sp_ == -1) and w['os'] - run['t1'] < 1.2:
        run['t1'] = w['oe']
    else:
        if run: speaker_gain.append(run)
        run = {'spk': sp_, 't0': w['os'], 't1': w['oe']}
if run: speaker_gain.append(run)
speaker_gain = [{'t0': max(0, g['t0'] - 0.12), 't1': g['t1'] + 0.12, 'db': 2.3} for g in speaker_gain if g['spk'] == 1]
plan = {
    'source': '/home/user/work/src/IMG_0623.MOV', 'matte': '/home/user/work/analysis/matte_src.mkv',
    'lut_fg': '/home/user/work/project/fg.cube', 'lut_bg': '/home/user/work/project/bg.cube', 'clarity': 0.38, 'vignette': 0.18,
    'fontsdir': '/home/user/work/project/fonts', 'subs': '/home/user/work/build/subs.ass',
    'edl': edl, 'audio_edl': audio_edl, 'nout': NOUT, 'speaker_gain': speaker_gain, 'framing': framing, 'overlays': overlays, 'splits': splits, 'sfx': sfx,
    'split': {'src_y0': 560, 'dst_y0': 1150},
}
import os; os.makedirs('/home/user/work/build', exist_ok=True)
json.dump(plan, open('/home/user/work/build/plan.json', 'w'), indent=0)
json.dump(jobs, open('/home/user/work/gfx/jobs.json', 'w'), ensure_ascii=False, indent=0)
json.dump([{'w': w['w'], 's': round(w['os'], 3), 'e': round(w['oe'], 3), 'i': w['i']} for w in ow], open('/home/user/work/build/out_words.json', 'w'), ensure_ascii=False)
print(f'EDL {len(edl)} pieces, output {NOUT} frames = {NOUT/FPS:.1f}s (source {DUR:.1f}s, removed {DUR-NOUT/FPS:.1f}s)')
print(f'shots {len(framing)}, overlays {len(overlays)}, splits {len(splits)}, sfx {len(sfx)}')
