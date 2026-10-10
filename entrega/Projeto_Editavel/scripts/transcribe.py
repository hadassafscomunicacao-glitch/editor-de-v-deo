"""Verbatim-leaning transcription with word timestamps (faster-whisper, CPU int8)."""
import sys, json, time
from faster_whisper import WhisperModel
model_name = sys.argv[1] if len(sys.argv) > 1 else 'large-v3'
audio = sys.argv[2] if len(sys.argv) > 2 else 'audio/mono16k.wav'
out = sys.argv[3] if len(sys.argv) > 3 else f'analysis/transcript_{model_name}.json'
m = WhisperModel(model_name, device='cpu', compute_type='int8', cpu_threads=4)
# prompt nudges Whisper to keep hesitations, false starts and repetitions instead of cleaning them up
prompt = ("Hellen e Indira conversam sobre conflito, liderança, RH e o elevador do conflito. "
          "Transcrição literal, com hesitações: é... é, né, tipo, ahn, eu, eu acho que, o ele... elevador, a gen... a gente.")
t0 = time.time()
segs, info = m.transcribe(audio, language='pt', beam_size=5, word_timestamps=True, vad_filter=False,
                          condition_on_previous_text=False, initial_prompt=prompt, temperature=[0.0, 0.2, 0.4],
                          no_speech_threshold=0.5, compression_ratio_threshold=2.4)
res = []
for s in segs:
    res.append({'start': s.start, 'end': s.end, 'text': s.text, 'avg_logprob': s.avg_logprob, 'no_speech_prob': s.no_speech_prob,
                'words': [{'w': w.word, 's': w.start, 'e': w.end, 'p': w.probability} for w in (s.words or [])]})
    print(f'[{s.start:8.2f} {s.end:8.2f}] {s.text}', flush=True)
json.dump({'model': model_name, 'duration': info.duration, 'segments': res}, open(out, 'w'), ensure_ascii=False, indent=1)
print('done', time.time() - t0)
