"""Merge reviewer + verifier results into the final cut list, then snap every splice to the frame grid while keeping
the audio splice in silence: each kept piece may slide its audio by up to +-20 ms (imperceptible lip-sync offset)
so both of its ends fall on the quietest available point. Writes build/cuts.json, build/audio_edl.json, build/cut_report.json."""
import json, sys, numpy as np, soundfile as sf
FPS = 30; SR = 48000
wf = json.load(open(sys.argv[1]))          # workflow result: [{chunk, review, verify}]
MIN_CONF = 0.55
cuts = []; report = []
for r in wf:
    rev, ver = r['review'], r['verify'] or {'verdicts': [], 'missed_cuts': []}
    vmap = {v['id']: v for v in ver.get('verdicts', [])}
    for c in rev['cuts']:
        v = vmap.get(c['id'])
        verdict = v['verdict'] if v else 'unverified'
        a, b = c['approx_start'], c['approx_end']
        if v and verdict in ('accept', 'modify') and v.get('start') is not None and v.get('end') is not None:
            a, b = v['start'], v['end']
        keep = verdict in ('accept', 'modify') or (verdict == 'unverified' and c['confidence'] >= 0.8)
        report.append({'chunk': r['chunk'], 'id': c['id'], 'type': c['type'], 'removed': c['removed_text'], 'result': (v or {}).get('result_text') or c['result_text'],
                       'verdict': verdict, 'conf': c['confidence'], 'a': a, 'b': b, 'used': bool(keep), 'evidence': (v or {}).get('evidence', '')})
        if keep and b - a > 0.02: cuts.append([a, b])
    for k, m in enumerate(ver.get('missed_cuts', [])):
        keep = False   # verifier-found cuts are only used when the editor approves them (build/cut_decisions.json)
        report.append({'chunk': r['chunk'], 'id': f"missed{r['chunk']}_{k}", 'type': m.get('type', 'other'), 'removed': m['removed_text'], 'result': m['result_text'],
                       'verdict': 'verifier-found', 'conf': m['confidence'], 'a': m['approx_start'], 'b': m['approx_end'], 'used': keep, 'evidence': m['reason']})
        if keep and m['approx_end'] - m['approx_start'] > 0.02: cuts.append([m['approx_start'], m['approx_end']])
import os
DEC = json.load(open('build/cut_decisions.json')) if os.path.exists('build/cut_decisions.json') else {}
# editor decisions: force-exclude ids, force-include verifier-found ids
for rp in report:
    if rp['id'] in DEC.get('exclude', []) and rp['used']:
        rp['used'] = False; rp['verdict'] += ' / excluído pelo editor'
        cuts = [c for c in cuts if not (abs(c[0] - rp['a']) < 1e-6 and abs(c[1] - rp['b']) < 1e-6)]
    if rp['id'] in DEC.get('include', []) and not rp['used']:
        rp['used'] = True; rp['verdict'] += ' / aprovado pelo editor'; cuts.append([rp['a'], rp['b']])
for c in (json.load(open('build/own_cuts.json')) if os.path.exists('build/own_cuts.json') else []):
    report.append({'chunk': 0, 'id': c['id'], 'type': c['type'], 'removed': c['removed'], 'result': c['result'], 'verdict': 'editor (sondagem de áudio)',
                   'conf': 0.9, 'a': c['a'], 'b': c['b'], 'used': True, 'evidence': c['evidence']})
    cuts.append([c['a'], c['b']])
cuts.sort()
merged = []
for a, b in cuts:
    if merged and a <= merged[-1][1] + 0.03: merged[-1][1] = max(merged[-1][1], b)
    else: merged.append([a, b])
cuts = merged
# ---- energy envelope (1 ms hop, 6 ms window)
x, _ = sf.read('audio/orig48k.wav', dtype='float32'); x = x.mean(1)
hop = SR // 1000; win = 6 * hop
sq = np.concatenate([[0], np.cumsum(x.astype(np.float64) ** 2)])
idx = np.arange(0, len(x) - win, hop)
env = 10 * np.log10((sq[idx + win] - sq[idx]) / win + 1e-12)
def E(t):
    i = int(round(t * 1000)) - 3
    return env[min(max(i, 0), len(env) - 1)]
DUR = len(x) / SR
# kept pieces between cuts
pieces = []; t = 0.0
for a, b in cuts:
    if a > t: pieces.append([t, a])
    t = max(t, b)
pieces.append([t, DUR])
edl = []; aedl = []; flags = []
for k, (s, e) in enumerate(pieces):
    best = None
    for fa in ([int(round(s * FPS)) + d for d in (-1, 0, 1)] if k > 0 else [0]):
        for fb in ([int(round(e * FPS)) + d for d in (-1, 0, 1)] if k < len(pieces) - 1 else [int(round(e * FPS))]):
            if fb - fa < 3: continue
            for dms in range(-20, 21, 2):
                d = dms / 1000
                a0, b0 = fa / FPS + d, fb / FPS + d
                # stay inside the intended kept region (+-15 ms tolerance) so no removed sound leaks in and no kept sound is lost
                if k > 0 and a0 < s - 0.015: continue
                if k < len(pieces) - 1 and b0 > e + 0.015: continue
                if k > 0 and a0 > s + 0.06: continue
                if k < len(pieces) - 1 and b0 < e - 0.06: continue
                # quiet splice points, but stay close to the verified boundaries (1 dB per 6 ms of drift)
                cost = (E(a0) if k > 0 else -90) + (E(b0) if k < len(pieces) - 1 else -90) + abs(dms) * 0.05 \
                       + (abs(a0 - s) * 170 if k > 0 else 0) + (abs(b0 - e) * 170 if k < len(pieces) - 1 else 0)
                if best is None or cost < best[0]: best = (cost, fa, fb, d)
    if best is None:
        fa, fb, d = int(round(s * FPS)), int(round(e * FPS)), 0.0
        flags.append({'piece': k, 'why': 'no candidate', 's': s, 'e': e})
    else:
        _, fa, fb, d = best
    if k > 0 and E(fa / FPS + d) > -38: flags.append({'piece': k, 'end': 'start', 't': fa / FPS + d, 'dB': round(float(E(fa / FPS + d)), 1)})
    if k < len(pieces) - 1 and E(fb / FPS + d) > -38: flags.append({'piece': k, 'end': 'end', 't': fb / FPS + d, 'dB': round(float(E(fb / FPS + d)), 1)})
    edl.append([fa, fb]); aedl.append([round(fa / FPS + d, 4), round(fb / FPS + d, 4)])
json.dump(cuts, open('build/cuts.json', 'w'), indent=0)
json.dump({'edl': edl, 'audio_edl': aedl, 'flags': flags}, open('build/edl_refined.json', 'w'), indent=0)
json.dump(report, open('build/cut_report.json', 'w'), ensure_ascii=False, indent=1)
print(f'{len(cuts)} cuts, removed {sum(b - a for a, b in cuts):.2f}s; pieces {len(edl)}; flagged splice ends {len(flags)}')
for f in flags: print('  FLAG', f)
