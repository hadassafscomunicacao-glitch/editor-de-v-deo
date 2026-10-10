"""Two-speaker diarization: sliding-window speaker embeddings (WeSpeaker ResNet34, sherpa-onnx) + 2-cluster k-means.
Writes analysis/diar_windows.npy (t_center, label, margin)."""
import sherpa_onnx, soundfile as sf, numpy as np, json
x, sr = sf.read('audio/mono16k.wav', dtype='float32')
cfg = sherpa_onnx.SpeakerEmbeddingExtractorConfig(model='models/sherpa/wespeaker_en_voxceleb_resnet34.onnx', num_threads=2)
ex = sherpa_onnx.SpeakerEmbeddingExtractor(cfg)
vad = json.load(open('analysis/vad_segments.json'))
WIN, HOP = 1.5, 0.25
embs, cents = [], []
for a, b in vad:
    t = a
    while t + 0.6 <= b:
        s, e = t, min(t + WIN, b)
        st = ex.create_stream(); st.accept_waveform(sr, x[int(s * sr):int(e * sr)]); st.input_finished()
        if ex.is_ready(st):
            v = np.array(ex.compute(st)); embs.append(v / np.linalg.norm(v)); cents.append((s + e) / 2)
        t += HOP
E = np.array(embs); C = np.array(cents)
print('windows', len(E))
# k-means (cosine) with 2 clusters, several restarts
best = None
rng = np.random.default_rng(0)
for rep in range(8):
    c = E[rng.choice(len(E), 2, replace=False)]
    for it in range(50):
        sim = E @ c.T; lab = sim.argmax(1)
        nc = np.array([E[lab == k].mean(0) for k in range(2)]); nc /= np.linalg.norm(nc, axis=1, keepdims=True)
        if np.allclose(nc, c): break
        c = nc
    score = np.mean(np.max(E @ c.T, 1))
    if best is None or score > best[0]: best = (score, c, lab)
_, c, lab = best
sim = E @ c.T
margin = sim[np.arange(len(E)), lab] - sim[np.arange(len(E)), 1 - lab]
print('cluster sizes', np.bincount(lab), 'centroid sim', float(c[0] @ c[1]))
np.save('analysis/diar_windows.npy', np.stack([C, lab, margin], 1))
np.save('analysis/diar_centroids.npy', c)
