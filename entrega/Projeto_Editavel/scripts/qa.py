"""Automated QC of a rendered master.
 - container/stream checks, duration A/V match
 - black frames (blackdetect) and frozen video (freezedetect)
 - loudness / true peak (ebur128)
 - splice integrity: re-transcribe +-1.6 s around every audio splice with Parakeet and compare to the expected words
Usage: python project/qa.py video.mp4 plan.json [out_words.json]"""
import sys, json, subprocess, re, numpy as np, soundfile as sf, unicodedata, difflib
V, PLAN = sys.argv[1], json.load(open(sys.argv[2]))
WORDS = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else None
rep = {}
pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', V], capture_output=True, text=True).stdout)
vs = [s for s in pr['streams'] if s['codec_type'] == 'video'][0]; aus = [s for s in pr['streams'] if s['codec_type'] == 'audio']
rep['video'] = {k: vs.get(k) for k in ['codec_name', 'width', 'height', 'r_frame_rate', 'nb_frames', 'duration', 'pix_fmt']}
rep['audio'] = {k: aus[0].get(k) for k in ['codec_name', 'sample_rate', 'channels', 'duration', 'bit_rate']} if aus else None
rep['expected_frames'] = PLAN['nout']
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', V, '-vf', 'blackdetect=d=0.08:pix_th=0.06,freezedetect=n=0.0015:d=0.6', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True)
err = r.stderr
rep['black'] = re.findall(r'black_start:([\d.]+) black_end:([\d.]+)', err)
rep['freeze'] = re.findall(r'freeze_start: ([\d.]+)', err)
m = re.search(r'Integrated loudness:\s+I:\s+([-\d.]+) LUFS.*?LRA:\s+([-\d.]+) LU.*?Peak:\s+([-\d.]+) dBFS', err, re.S)
rep['loudness'] = {'I': float(m.group(1)), 'LRA': float(m.group(2)), 'TP': float(m.group(3))} if m else None
if WORDS:
    import sherpa_onnx
    d = '/home/user/work/models/sherpa/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8/'
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=d + 'encoder.int8.onnx', decoder=d + 'decoder.int8.onnx', joiner=d + 'joiner.int8.onnx', tokens=d + 'tokens.txt', num_threads=3, model_type='nemo_transducer')
    subprocess.run(['ffmpeg', '-v', 'error', '-i', V, '-ac', '1', '-ar', '16000', '-y', '/tmp/qa16k.wav'], check=True)
    x, sr = sf.read('/tmp/qa16k.wav', dtype='float32')
    def n(w):
        w = unicodedata.normalize('NFD', w.lower()); w = ''.join(c for c in w if unicodedata.category(c) != 'Mn'); return re.sub(r'[^a-z0-9]', '', w)
    starts = np.cumsum([0] + [b - a for a, b in PLAN['edl']])[1:-1] / 30
    bad = []
    for t in starts:
        a, b = max(0, t - 1.6), t + 1.6
        st = rec.create_stream(); st.accept_waveform(sr, x[int(a * sr):int(b * sr)]); rec.decode_stream(st)
        got = [n(w) for w in st.result.text.split() if n(w)]
        exp = [n(w['w']) for w in WORDS if w['s'] >= a + 0.25 and w['e'] <= b - 0.25 and n(w['w'])]
        ratio = difflib.SequenceMatcher(None, ' '.join(exp), ' '.join(got)).ratio() if exp else 1
        if ratio < 0.8: bad.append({'t': round(float(t), 2), 'ratio': round(ratio, 2), 'expected': ' '.join(exp), 'heard': st.result.text})
    rep['splices_checked'] = len(starts); rep['splices_suspect'] = bad
print(json.dumps(rep, ensure_ascii=False, indent=1))
