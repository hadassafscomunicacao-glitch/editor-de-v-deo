"""Inspect a short audio window as an editor would 'listen' to it:
   python project/probe_audio.py START END [--whisper]
Prints Parakeet tokens with times, optional Whisper text, and a 20 ms energy profile (dBFS) so pauses / breaths / restarts are visible."""
import sys, numpy as np, soundfile as sf, sherpa_onnx
a, b = float(sys.argv[1]), float(sys.argv[2])
x, sr = sf.read('/home/user/work/audio/mono16k.wav', dtype='float32')
seg = x[int(a * sr):int(b * sr)]
d = '/home/user/work/models/sherpa/sherpa-onnx-nemo-parakeet-tdt-0.6b-v3-int8/'
rec = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=d + 'encoder.int8.onnx', decoder=d + 'decoder.int8.onnx', joiner=d + 'joiner.int8.onnx', tokens=d + 'tokens.txt', num_threads=1, model_type='nemo_transducer')
st = rec.create_stream(); st.accept_waveform(sr, seg); rec.decode_stream(st); r = st.result
print('PARAKEET:', r.text)
print('tokens:', ' '.join(f'{t!r}@{a+s:.2f}' for t, s in zip(r.tokens, r.timestamps)))
if '--whisper' in sys.argv:
    w = '/home/user/work/models/sherpa/sherpa-onnx-whisper-large-v3/'
    wr = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=w + 'large-v3-encoder.int8.onnx', decoder=w + 'large-v3-decoder.int8.onnx', tokens=w + 'large-v3-tokens.txt', language='pt', num_threads=1)
    s2 = wr.create_stream(); s2.accept_waveform(sr, seg); wr.decode_stream(s2); print('WHISPER:', s2.result.text)
hop = int(0.02 * sr)
e = [20 * np.log10(np.sqrt(np.mean(seg[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(seg) - hop, hop)]
print('energy dBFS per 20ms from', a, ':')
for i in range(0, len(e), 25):
    print(f'{a + i * 0.02:8.2f} ' + ' '.join(f'{v:4.0f}' for v in e[i:i + 25]))
