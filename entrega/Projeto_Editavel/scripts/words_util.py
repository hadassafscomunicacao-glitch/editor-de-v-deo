"""Helpers to locate spoken phrases in the ASR word list (source timeline)."""
import json, re, unicodedata
WORDS = json.load(open('/home/user/work/analysis/words.json'))
def _n(w):
    w = unicodedata.normalize('NFD', w.lower()); w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9%]', '', w)
NORM = [_n(w['w']) for w in WORDS]
def find(phrase, near=None, window=40.0, after=None):
    """Return (start_time, end_time, first_idx, last_idx) of the phrase occurrence closest to `near` (seconds)."""
    toks = [_n(t) for t in phrase.split() if _n(t)]
    best = None
    for i in range(len(WORDS) - len(toks) + 1):
        if all(NORM[i + k] == toks[k] for k in range(len(toks))):
            s = WORDS[i]['s']
            if after is not None and s < after: continue
            d = abs(s - near) if near is not None else 0
            if near is not None and d > window: continue
            if best is None or d < best[0]: best = (d, i)
    if best is None: raise KeyError(f'phrase not found: {phrase!r} near {near}')
    i = best[1]; j = i + len(toks) - 1
    return WORDS[i]['s'], WORDS[j]['e'], i, j
def ws(phrase, near=None, **k): return find(phrase, near, **k)[0]
def we(phrase, near=None, **k): return find(phrase, near, **k)[1]
