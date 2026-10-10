"""Subtitles for the FINAL edit: the reviewed clean text supplies spelling/punctuation, the ASR words that survived the cuts
supply timing (output timeline). Words removed by cuts never appear; words the reviewers dropped but which stayed in the
audio (a rejected cut) are kept, so subtitles always match what is heard."""
import json, sys, difflib, re
sys.path.insert(0, '/home/user/work/project')
from subtitles import build_cues, write, norm
words = json.load(open('/home/user/work/analysis/words.json'))
seg_of = {w['i']: w['seg'] for w in words}
ow = json.load(open('/home/user/work/build/out_words.json'))          # kept words with output times
plan = json.load(open('/home/user/work/build/plan.json'))
splice_t = set(round(x / 30, 3) for x in __import__('numpy').cumsum([0] + [b - a for a, b in plan['edl']])[1:-1])
T = {o['seg']: o for o in json.load(open('/home/user/work/analysis/transcricao_final.json'))}
by_seg = {}
for w in ow: by_seg.setdefault(seg_of[w['i']], []).append(w)
final = []
for k in sorted(by_seg):
    aw = by_seg[k]
    clean = T[k]['clean'].split() if k in T else [w['w'] for w in aw]
    A = [norm(w['w']) for w in aw]; B = [norm(t) for t in clean]
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    for tag, a0, a1, b0, b1 in sm.get_opcodes():
        if tag == 'equal':
            for i in range(a1 - a0): final.append({'w': clean[b0 + i], 's': aw[a0 + i]['s'], 'e': aw[a0 + i]['e']})
        elif tag == 'replace':
            s, e = aw[a0]['s'], aw[a1 - 1]['e']; n = b1 - b0
            for i in range(n): final.append({'w': clean[b0 + i], 's': s + (e - s) * i / n, 'e': s + (e - s) * (i + 1) / n})
        elif tag == 'delete':
            for i in range(a0, a1):
                # ASR-only words absent from the reviewed text: keep substantive words (rejected cuts stay audible),
                # drop short function-word stutters the reviewers removed after listening (checked one by one)
                if A[i] and len(A[i]) > 3: final.append({'w': aw[i]['w'], 's': aw[i]['s'], 'e': aw[i]['e'], 'raw': True})
        elif tag == 'insert':
            prev = aw[a0 - 1]['e'] if a0 > 0 else aw[0]['s']; nxt = aw[a0]['s'] if a0 < len(aw) else prev + 0.3
            if any(prev - 0.02 <= t <= nxt + 0.02 for t in splice_t): continue   # never subtitle words that sit on a cut
            n = b1 - b0
            for i in range(n): final.append({'w': clean[b0 + i], 's': prev + (nxt - prev) * i / n, 'e': prev + (nxt - prev) * (i + 1) / n})
final.sort(key=lambda w: w['s'])
# capitalise after sentence ends when a raw ASR word starts a sentence
for i, w in enumerate(final):
    if i == 0 or re.search(r'[.!?]$', final[i - 1]['w']): w['w'] = w['w'][:1].upper() + w['w'][1:]
cues = build_cues(final)
write(cues, '/home/user/work/build/Legendas.srt', '/home/user/work/build/subs.ass', emphasis=())
json.dump(final, open('/home/user/work/build/sub_words.json', 'w'), ensure_ascii=False)
print(len(final), 'words,', len(cues), 'cues;', sum(1 for w in final if w.get('raw')), 'raw ASR words kept')
