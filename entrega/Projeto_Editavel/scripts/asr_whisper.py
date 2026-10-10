"""Second-opinion transcription (Whisper large-v3, sherpa-onnx int8) over the same VAD segments, for text cross-checking."""
import sherpa_onnx, soundfile as sf, json, time
d = 'models/sherpa/sherpa-onnx-whisper-large-v3/'
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=d + 'large-v3-encoder.int8.onnx', decoder=d + 'large-v3-decoder.int8.onnx',
                                                 tokens=d + 'large-v3-tokens.txt', language='pt', task='transcribe', num_threads=2)
x, sr = sf.read('audio/mono16k.wav', dtype='float32')
segs = json.load(open('analysis/asr_parakeet.json'))['segments']
out = []; t0 = time.time()
for k, s in enumerate(segs):
    a = max(0, int((s['start'] - .12) * sr)); b = min(len(x), int((s['end'] + .12) * sr))
    st = rec.create_stream(); st.accept_waveform(sr, x[a:b]); rec.decode_stream(st)
    out.append({'start': s['start'], 'end': s['end'], 'text': st.result.text.strip()})
    print(k, f"{s['start']:7.1f}", st.result.text.strip()[:100], flush=True)
    json.dump(out, open('analysis/asr_whisper.json', 'w'), ensure_ascii=False, indent=0)
print('done', time.time() - t0)
