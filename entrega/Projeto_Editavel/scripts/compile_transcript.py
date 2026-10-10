"""Compile the reviewed transcript: reviewers' clean text per segment + verifiers' text fixes + speaker per segment.
Input: build/review_results.json (workflow output). Output: analysis/transcricao_final.json / .md"""
import json, numpy as np, re
R = json.load(open('/home/user/work/build/review_results.json'))
asr = json.load(open('/home/user/work/analysis/asr_parakeet.json'))['segments']
DW = np.load('/home/user/work/analysis/diar_windows.npy')
NAMES = {0: 'Indira', 1: 'Hellen'}
segs = {}
for r in R:
    for s in r['review']['segments']:
        segs[s['seg']] = {'clean': s['clean'], 'verbatim': s['verbatim'], 'uncertain': s.get('uncertain', [])}
    for fx in (r['verify'] or {}).get('text_fixes', []):
        s = segs.get(fx['seg'])
        if s and fx['wrong'] in s['clean']:
            s['clean'] = s['clean'].replace(fx['wrong'], fx['right'], 1); s.setdefault('fixes', []).append(fx)
out = []
for k, a in enumerate(asr):
    s = segs.get(k, {'clean': a['text'], 'verbatim': a['text']})
    # speaker turns inside the segment (by word)
    turns = []
    for w in a['words']:
        m = (DW[:, 0] >= w['s'] - .3) & (DW[:, 0] <= w['e'] + .3)
        sp = int(np.round(DW[m, 1].mean())) if m.any() else -1
        if turns and (turns[-1][0] == sp or sp == -1): continue
        turns.append((sp, w['s']))
    main = max(set(t[0] for t in turns), key=lambda x: sum(1 for t in turns if t[0] == x)) if turns else -1
    out.append({'seg': k, 'start': a['start'], 'end': a['end'], 'speaker': NAMES.get(main, '?'), 'turns': [(NAMES.get(sp, '?'), round(t, 2)) for sp, t in turns],
                'clean': s['clean'], 'verbatim': s['verbatim'], 'uncertain': s.get('uncertain', [])})
json.dump(out, open('/home/user/work/analysis/transcricao_final.json', 'w'), ensure_ascii=False, indent=1)
def ts(t): return f'{int(t // 60):02d}:{t % 60:05.2f}'
with open('/home/user/work/analysis/transcricao_final.md', 'w') as f:
    f.write('# Transcrição revisada — tempos do arquivo bruto\n\nTexto limpo (como nas legendas). Indira = esquerda (blazer azul); Hellen = direita (blusa bege).\n\n')
    for o in out:
        who = o['speaker'] if len(set(t[0] for t in o['turns'])) <= 1 else ' / '.join(dict.fromkeys(t[0] for t in o['turns']))
        f.write(f"**[{ts(o['start'])}] {who}:** {o['clean']}\n\n")
print(len(out), 'segments')
