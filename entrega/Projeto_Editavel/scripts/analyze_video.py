"""Single decode pass over the source:
 - person matte (MediaPipe multiclass selfie) every 2nd frame -> mattes.npy (uint8 256x256 per sample)
 - face boxes for left/right participant every 2nd frame -> faces.npy
 - mouth-region motion energy for both participants every frame -> mouth_energy.npy
"""
import sys, subprocess, numpy as np, cv2, time
sys.path.insert(0, 'project')
from matte import Segmenter
import mediapipe as mp
from mediapipe.tasks import python as mpp
from mediapipe.tasks.python import vision

SRC = 'src/IMG_0623.MOV'; W, H = 1080, 1920; N = 37357
STEP = 2
seg = Segmenter()
det = vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(
    base_options=mpp.BaseOptions(model_asset_path='models/blaze_face_short_range.tflite'), min_detection_confidence=0.4))
mattes = np.lib.format.open_memmap('analysis/mattes.npy', mode='w+', dtype=np.uint8, shape=((N + STEP - 1) // STEP, 256, 256))
faces = np.full(((N + STEP - 1) // STEP, 2, 6), np.nan, np.float32)  # x,y,w,h,mouth_x,mouth_y
mouth_e = np.zeros((N, 2), np.float32)
HALVES = [(0, 560), (520, 1080)]
mouth_c = [(318, 915), (818, 870)]  # initial guesses, updated from detections
prev_m = [None, None]
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-threads', '3', '-i', SRC, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE, bufsize=W * H * 3 * 4)
i = 0; t0 = time.time()
while True:
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    fr = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    if i % STEP == 0:
        k = i // STEP
        prob = seg.person_prob(fr)
        mattes[k] = (cv2.resize(prob, (256, 256), interpolation=cv2.INTER_AREA) * 255 + .5).astype(np.uint8)
        for s, (x0, x1) in enumerate(HALVES):
            crop = np.ascontiguousarray(fr[500:1150, x0:x1])
            r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=crop))
            if r.detections:
                d = max(r.detections, key=lambda d: d.categories[0].score)
                bb = d.bounding_box; kp = d.keypoints
                mx, my = kp[3].x * crop.shape[1] + x0, kp[3].y * crop.shape[0] + 500
                faces[k, s] = [bb.origin_x + x0, bb.origin_y + 500, bb.width, bb.height, mx, my]
                mouth_c[s] = (int(mx), int(my))
    g = cv2.cvtColor(fr, cv2.COLOR_RGB2GRAY)
    for s in range(2):
        mx, my = mouth_c[s]
        c = g[max(0, my - 30):my + 40, max(0, mx - 50):mx + 50].astype(np.float32)
        if prev_m[s] is not None and prev_m[s].shape == c.shape:
            mouth_e[i, s] = np.mean(np.abs(c - prev_m[s]))
        prev_m[s] = c
    i += 1
    if i % 1500 == 0:
        print(i, f'{(time.time()-t0)/i*1000:.0f} ms/frame', flush=True)
mattes.flush(); np.save('analysis/faces.npy', faces); np.save('analysis/mouth_energy.npy', mouth_e[:i])
print('done', i, time.time() - t0)
