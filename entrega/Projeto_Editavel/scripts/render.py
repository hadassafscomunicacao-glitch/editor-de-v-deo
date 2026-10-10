"""Final compositor.
Stage 1 (ffmpeg, multithreaded): decode source -> keep EDL frames -> colour grade with person matte (two 3D LUTs + local contrast) -> raw RGB.
Stage 2 (python/OpenCV): per output frame: reframing (punch-in / push-in / split-screen), vignette, motion-graphics overlays (RGBA PNG sequences).
Stage 3 (ffmpeg): encode the clean master (no subtitles) and, in parallel, the subtitled version (libass).
Usage: python project/render.py plan.json OUT_PREFIX [--from F --to F] [--preview]"""
import json, sys, subprocess, numpy as np, cv2, os, math, argparse
cv2.setNumThreads(1)   # OpenCV worker pool otherwise competes with ffmpeg threads and stalls the pipe
ap = argparse.ArgumentParser(); ap.add_argument('plan'); ap.add_argument('out'); ap.add_argument('--from', dest='f0', type=int, default=0)
ap.add_argument('--to', dest='f1', type=int, default=None); ap.add_argument('--preview', action='store_true'); ap.add_argument('--nosubs', action='store_true')
ap.add_argument('--crf', type=float, default=17); ap.add_argument('--only', choices=['clean', 'subs'], default=None); ap.add_argument('--preset', default='slow')
A = ap.parse_args()
P = json.load(open(A.plan))
W, H, FPS = 1080, 1920, 30
SRC = P['source']
segs = P['edl']                       # [[src_frame_in, src_frame_out_exclusive], ...]
out_to_src = np.concatenate([np.arange(a, b) for a, b in segs])
NOUT = len(out_to_src)
f0, f1 = A.f0, (A.f1 if A.f1 is not None else NOUT)
sel_frames = out_to_src[f0:f1]

# ---------- stage 1: ffmpeg decode + grade ----------
def ranges(fr):
    r = []; s = fr[0]; p = fr[0]
    for x in fr[1:]:
        if x != p + 1: r.append((s, p)); s = x
        p = x
    r.append((s, p)); return r
rs = ranges(out_to_src[f0:])
start_src = rs[0][0]
seek = max(0, start_src - 90) / FPS          # input seek a bit before; select uses absolute frame numbers via copyts
sel_expr = '+'.join(f'between(n,{a - int(round(seek * FPS))},{b - int(round(seek * FPS))})' for a, b in rs)
with open(A.out + '_select.txt', 'w') as f: f.write(sel_expr)
cl = P.get('clarity', 0.38)
graph = (f"[0:v]select='{sel_expr}',settb=1/{FPS},setpts=N,format=yuv420p,split[s1][s2];"
         f"[1:v]select='{sel_expr}',settb=1/{FPS},setpts=N,scale={W}:{H}:flags=bicubic,format=gbrp[m];"
         f"[s1]split[ya][yb];[yb]gblur=sigma=16:steps=2:planes=1[bl];[ya][bl]lut2=c0='clip(x+{cl}*(x-y),0,255)':c1='x':c2='x',format=gbrp,lut3d={P['lut_fg']}[fg];"
         f"[s2]format=gbrp,lut3d={P['lut_bg']}[bg];[bg][fg][m]maskedmerge,format=rgb24[out]")
with open(A.out + '_graph.txt', 'w') as f: f.write(graph)
dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-nostdin', '-ss', f'{seek:.4f}', '-i', SRC, '-ss', f'{seek:.4f}', '-i', P['matte'],
                        '-filter_complex_script', A.out + '_graph.txt', '-map', '[out]', '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       stdout=subprocess.PIPE, bufsize=W * H * 3 * 2)

# ---------- framing ----------
FR = P['framing']        # list of {f0,f1,z0,z1,cx0,cy0,cx1,cy1,ease, split0, split1}
def framing_at(i):
    for s in FR:
        if s['f0'] <= i < s['f1']:
            k = (i - s['f0']) / max(1, s['f1'] - s['f0'] - 1)
            e = s.get('ease', 'io')
            k = k if e == 'lin' else (k * k * (3 - 2 * k))
            g = lambda a, b: s[a] + (s.get(b, s[a]) - s[a]) * k
            return g('z0', 'z1'), g('cx0', 'cx1'), g('cy0', 'cy1'), s.get('split', 0.0)
    return 1.0, W / 2, H / 2, 0.0
SPLIT = P.get('split', {'src_y0': 560, 'dst_y0': 1150})
def split_at(i):
    for s in P.get('splits', []):
        if s['f0'] - s['tin'] <= i < s['f1'] + s['tout']:
            if i < s['f0']: k = 1 - (s['f0'] - i) / s['tin']
            elif i >= s['f1']: k = 1 - (i - s['f1'] + 1) / s['tout']
            else: k = 1.0
            k = max(0.0, min(1.0, k)); return k * k * (3 - 2 * k) if k < 1 else 1.0
    return 0.0
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.sqrt(((xx - W * .5) / (W * .62)) ** 2 + ((yy - H * .42) / (H * .58)) ** 2)
VIG = (1 - P.get('vignette', 0.18) * np.clip((r - .55) / .6, 0, 1) ** 2).astype(np.float32)
VIG8 = cv2.merge([np.round(VIG * 255).astype(np.uint8)] * 3)

def transform(img, z, cx, cy, sp):
    # zoom about (cx,cy) keeping output centre on (cx,cy) clamped so no borders appear
    if z <= 1.0001 and sp <= 0: return img
    hw, hh = W / (2 * z), H / (2 * z)
    cx = min(max(cx, hw), W - hw); cy = min(max(cy, hh), H - hh)
    M = np.array([[z, 0, W / 2 - z * cx], [0, z, H / 2 - z * cy]], np.float32)
    if sp > 0:  # split-screen: push picture down so source row src_y0 lands at dst_y0
        M[1, 2] += sp * (SPLIT['dst_y0'] - (z * SPLIT['src_y0'] + M[1, 2]))
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))

# ---------- overlays ----------
OV = P.get('overlays', [])  # {dir, f0, n, z}
class OvCache:
    def __init__(self): self.c = {}
    def get(self, path):
        if path not in self.c:
            if len(self.c) > 8: self.c.pop(next(iter(self.c)))
            im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            self.c[path] = im
        return self.c[path]
cache = OvCache()
def overlays_at(i):
    res = []
    for o in OV:
        if o['f0'] <= i < o['f0'] + o['n']:
            p = os.path.join(o['dir'], f"{i - o['f0']:05d}.png")
            if os.path.exists(p): res.append((o.get('z', 0), p))
    return [p for _, p in sorted(res)]
def over(dst, rgba):
    alpha = rgba[..., 3]
    x0, y0, w, h = cv2.boundingRect(alpha)
    if w == 0 or h == 0: return dst
    a = alpha[y0:y0 + h, x0:x0 + w].astype(np.float32) * (1 / 255)
    src = np.ascontiguousarray(rgba[y0:y0 + h, x0:x0 + w, 2::-1])   # BGRA -> RGB
    d = np.ascontiguousarray(dst[y0:y0 + h, x0:x0 + w])
    dst[y0:y0 + h, x0:x0 + w] = cv2.blendLinear(src, d, a, 1 - a)
    return dst

# ---------- encoders ----------
def enc_cmd(path, subs=None):
    vf = ['format=yuv420p'] if not subs else [f"ass={subs}:fontsdir={P['fontsdir']}", 'format=yuv420p']
    return ['ffmpeg', '-v', 'error', '-nostdin', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
            '-vf', ','.join(vf), '-c:v', 'libx264', '-preset', A.preset, '-crf', str(A.crf), '-profile:v', 'high', '-pix_fmt', 'yuv420p',
            '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-movflags', '+faststart', '-threads', str(P.get('enc_threads', 3)), '-y', path]
encs = [] if A.only == 'subs' else [subprocess.Popen(enc_cmd(A.out + '_clean.mp4'), stdin=subprocess.PIPE)]
if not A.nosubs and P.get('subs') and A.only != 'clean':
    sub_file = P['subs']
    if f0:  # shift subtitles for partial renders
        sub_file = A.out + '_subs.ass'
        import re as _re
        def _t2s(x): h, m, s_ = x.split(':'); return int(h) * 3600 + int(m) * 60 + float(s_)
        def _s2t(v): v = max(0.0, v); cs = int(round(v * 100)); return f'{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}'
        off = f0 / FPS; out_lines = []
        for ln in open(P['subs'], encoding='utf-8').read().split('\n'):
            m_ = _re.match(r'^(Dialogue: \d+,)([^,]+),([^,]+),(.*)$', ln)
            if m_:
                a_, b_ = _t2s(m_.group(2)) - off, _t2s(m_.group(3)) - off
                if b_ <= 0: continue
                ln = f'{m_.group(1)}{_s2t(a_)},{_s2t(b_)},{m_.group(4)}'
            out_lines.append(ln)
        open(sub_file, 'w', encoding='utf-8').write('\n'.join(out_lines))
    encs.append(subprocess.Popen(enc_cmd(A.out + '_subs.mp4', sub_file), stdin=subprocess.PIPE))

import time as _t
TT = {'read': 0.0, 'proc': 0.0, 'write': 0.0}
n = 0; FB = W * H * 3
for i in range(f0, f1):
    _a = _t.time()
    b = dec.stdout.read(FB)
    TT['read'] += _t.time() - _a; _a = _t.time()
    if len(b) < FB: print('decoder ended early at', i, file=sys.stderr); break
    img = np.frombuffer(b, np.uint8).reshape(H, W, 3).copy()
    z, cx, cy, _ = framing_at(i)
    sp = split_at(i)
    img = transform(img, z, cx, cy, sp)
    img = cv2.multiply(img, VIG8, scale=1 / 255)
    for p in overlays_at(i):
        img = over(img, cache.get(p))
    data = img.tobytes()
    TT['proc'] += _t.time() - _a; _a = _t.time()
    for e in encs: e.stdin.write(data)
    TT['write'] += _t.time() - _a
    n += 1
    if n % 300 == 0: print(f'{i}/{f1}', flush=True)
for e in encs: e.stdin.close(); e.wait()
dec.terminate()
print('rendered', n, 'frames', {k: round(v, 1) for k, v in TT.items()})
