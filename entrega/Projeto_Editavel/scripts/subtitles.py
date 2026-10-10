"""Build subtitle cues from the corrected ("clean") text, timed by aligning it to the ASR words kept in the edit.
Outputs .srt and a styled .ass (libass) for burn-in."""
import json, re, unicodedata, difflib, sys

def norm(w):
    w = unicodedata.normalize('NFD', w.lower()); w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9%]', '', w)

def align_segment(clean_text, asr_words):
    """asr_words: [{'w','s','e'}] already on the OUTPUT timeline (cut words removed). Returns [{'w','s','e'}] for clean tokens."""
    toks = clean_text.split()
    if not toks: return []
    if not asr_words: return []
    A = [norm(w['w']) for w in asr_words]; B = [norm(t) for t in toks]
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    times = [None] * len(toks)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            aw = asr_words[blk.a + k]; times[blk.b + k] = (aw['s'], aw['e'])
    # opcodes 'replace' with equal-ish length: map proportionally
    for tag, a0, a1, b0, b1 in sm.get_opcodes():
        if tag == 'replace':
            s, e = asr_words[a0]['s'], asr_words[a1 - 1]['e']
            for k in range(b0, b1):
                f0 = (k - b0) / (b1 - b0); f1 = (k - b0 + 1) / (b1 - b0)
                times[k] = (s + (e - s) * f0, s + (e - s) * f1)
    # interpolate remaining gaps
    s0, e0 = asr_words[0]['s'], asr_words[-1]['e']
    for k in range(len(toks)):
        if times[k] is None:
            prev = next((times[j][1] for j in range(k - 1, -1, -1) if times[j]), s0)
            nxt = next((times[j][0] for j in range(k + 1, len(toks)) if times[j]), e0)
            n_missing = 1; times[k] = (prev, max(prev + 0.05, min(nxt, prev + 0.35)))
    return [{'w': t, 's': a, 'e': b} for t, (a, b) in zip(toks, times)]

FUNC = set('a o as os de da do das dos e em na no nas nos um uma que se para pra com por ao à é ou mas nem'.split())
def build_cues(words, max_line=30, max_chars=60, max_dur=4.6, min_dur=0.8):
    """Sentence-aware cues: never glue the end of one sentence to the start of the next, avoid ending a cue on a function word."""
    cues = []; cur = []
    def text(ws): return ' '.join(x['w'] for x in ws)
    def flush():
        if cur: cues.append(list(cur)); cur.clear()
    for i, w in enumerate(words):
        if cur:
            gap = w['s'] - cur[-1]['e']
            too_long = len(text(cur + [w])) > max_chars or (w['e'] - cur[0]['s']) > max_dur
            if too_long or gap > 0.55:
                carry = []
                if too_long and gap <= 0.55:
                    # prefer splitting after the last comma (keeps phrases together), else move trailing function words
                    ci = max([k for k in range(1, len(cur) - 1) if re.search(r'[,;:]$', cur[k]['w'])] or [-1])
                    if ci >= 1 and len(text(cur[:ci + 1])) >= 14:
                        carry = cur[ci + 1:]; del cur[ci + 1:]
                while len(cur) > 2 and norm_plain(cur[-1]['w']) in FUNC and not re.search(r'[,.!?;:]$', cur[-1]['w']):
                    carry.insert(0, cur.pop())
                flush(); cur.extend(carry)
        cur.append(w)
        clen = len(text(cur))
        nxt_gap = (words[i + 1]['s'] - w['e']) if i + 1 < len(words) else 9
        if re.search(r'[.!?]["”]?$', w['w']):
            flush()
        elif re.search(r'[,;:]$', w['w']) and clen > 36:
            flush()
        elif nxt_gap > 0.4 and clen > 14:
            flush()
    flush()
    # merge tiny cues (1-2 words, <0.6 s) into a neighbour when it fits
    merged = []
    for c in cues:
        if merged and (len(text(c)) <= 12 or c[-1]['e'] - c[0]['s'] < 0.5) and len(text(merged[-1] + c)) <= max_chars \
                and not re.search(r'[.!?]$', merged[-1][-1]['w']) and c[0]['s'] - merged[-1][-1]['e'] < 0.4:
            merged[-1] = merged[-1] + c
        else:
            merged.append(c)
    out = [{'s': c[0]['s'], 'e': c[-1]['e'], 'text': text(c)} for c in merged]
    for k, c in enumerate(out):
        nxt = out[k + 1]['s'] if k + 1 < len(out) else c['e'] + 2
        c['e'] = max(c['e'] + 0.15, c['s'] + min_dur)
        if nxt - c['e'] < 0.3: c['e'] = nxt - 0.02
        c['e'] = min(c['e'], nxt - 0.02)
    return out

def norm_plain(w): return re.sub(r'[^\wà-ú]', '', w.lower())

def wrap(text, max_line=30):
    if len(text) <= max_line: return text
    words = text.split(); best = None
    for k in range(1, len(words)):
        a, b = ' '.join(words[:k]), ' '.join(words[k:])
        score = abs(len(a) - len(b)) + (0 if not re.search(r'^(de|da|do|e|a|o|que|em|na|no|um|uma|para|pra|com)$', words[k - 1]) else 8)
        if best is None or score < best[0]: best = (score, a, b)
    return best[1] + '\\N' + best[2]

def ts_srt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
def ts_ass(t):
    cs = int(round(t * 100)); h, cs = divmod(cs, 360000); m, cs = divmod(cs, 6000); s, cs = divmod(cs, 100)
    return f'{h}:{m:02d}:{s:02d}.{cs:02d}'

ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter Tight SemiBold,56,&H00FFFFFF,&H000000FF,&H5A0B1420,&H8C000000,0,0,0,0,100,100,0,0,1,2.6,1.6,2,90,90,{marginv},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def write(cues, srt_path, ass_path, marginv=290, emphasis=()):
    with open(srt_path, 'w', encoding='utf-8') as f:
        for k, c in enumerate(cues, 1):
            f.write(f"{k}\n{ts_srt(c['s'])} --> {ts_srt(c['e'])}\n{wrap(c['text']).replace(chr(92) + 'N', chr(10))}\n\n")
    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(ASS_HEAD.format(marginv=marginv))
        for c in cues:
            txt = wrap(c['text'])
            for e in emphasis:
                txt = re.sub(rf'(?<![\w]){re.escape(e)}(?![\w])', r'{\\c&H8FC8E2&}' + e + r'{\\c&HFFFFFF&}', txt)
            mv = c.get('marginv')
            f.write(f"Dialogue: 0,{ts_ass(c['s'])},{ts_ass(c['e'])},Sub,,0,0,{mv if mv else 0},,{{\\blur1.2\\fad(70,50)}}{txt}\n")
