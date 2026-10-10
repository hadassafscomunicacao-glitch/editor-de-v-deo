"""ASR with token-level timestamps: Silero VAD segmentation + NeMo Parakeet-TDT v3 (sherpa-onnx, local models).
Output: analysis/asr_parakeet.json  {segments:[{start,end,text,words:[{w,s,e}]}]}"""
import sherpa_onnx, soundfile as sf, numpy as np, json, time, sys
SR = 16000
x, sr = sf.read('audio/mono16k.wav', dtype='float32'); assert sr == SR
cfg = sherpa_onnx.VadModelConfig()
cfg.silero_vad.model = 'models/sherpa/silero_vad.onnx'
cfg.silero_vad.min_silence_duration = 0.30
cfg.silero_vad.min_speech_duration = 0.12
cfg.silero_vad.threshold = 0.4
cfg.silero_vad.max_speech_duration = 18
cfg.sample_rate = SR
vad = sherpa_onnx.VoiceActivityDetector(cfg, buffer_size_in_seconds=60)
segs = []
w = cfg.silero_vad.window_size
for i in range(0, len(x), w):
    vad.accept_waveform(x[i:i + w])
    while not vad.empty():
        s = vad.front; segs.append((s.start, s.start + len(s.samples))); vad.pop()
vad.flush()
while not vad.empty():
    s = vad.front; segs.append((s.start, s.start + len(s.samples))); vad.pop()
print('vad segments', len(segs), 'speech sec', sum(b - a for a, b in segs) / SR, flush=True)
json.dump([[a / SR, b / SR] for a, b in segs], open('analysis/vad_segments.json', 'w'))
d = 'models/sherpa/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8/'
rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=d + 'encoder.int8.onnx', decoder=d + 'decoder.int8.onnx', joiner=d + 'joiner.int8.onnx',
                                                    tokens=d + 'tokens.txt', num_threads=int(sys.argv[1]) if len(sys.argv) > 1 else 2, model_type='nemo_transducer')
PAD = int(0.12 * SR)
out = []; t0 = time.time()
for k, (a, b) in enumerate(segs):
    a0 = max(0, a - PAD); b0 = min(len(x), b + PAD)
    st = rec.create_stream(); st.accept_waveform(SR, x[a0:b0]); rec.decode_stream(st); r = st.result
    off = a0 / SR
    toks = [{'t': tk, 's': round(off + ts, 3), 'd': round(du, 3)} for tk, ts, du in zip(r.tokens, r.timestamps, r.durations)]
    words = []
    for tk in toks:
        if tk['t'].startswith(' ') or not words:
            words.append({'w': tk['t'].strip(), 's': tk['s'], 'e': round(tk['s'] + tk['d'], 3)})
        else:
            words[-1]['w'] += tk['t']; words[-1]['e'] = round(tk['s'] + tk['d'], 3)
    out.append({'start': a / SR, 'end': b / SR, 'text': r.text.strip(), 'tokens': toks, 'words': words})
    if k % 20 == 0: print(k, f'{a/SR:7.1f}', r.text[:90], flush=True)
json.dump({'segments': out}, open('analysis/asr_parakeet.json', 'w'), ensure_ascii=False, indent=0)
print('done', time.time() - t0)
