"""Visual QC: contact sheets of the final video at every overlay (entry, middle) and right after every splice."""
import sys, json, subprocess, numpy as np, cv2
V, P = sys.argv[1], json.load(open(sys.argv[2]))
FPS = 30
pts = []
for o in P['overlays']:
    pts += [(o['f0'] + 12, o['id'] + ' in'), (o['f0'] + o['n'] // 2, o['id'] + ' mid')]
starts = np.cumsum([0] + [b - a for a, b in P['edl']])[1:-1]
pts += [(int(s) + 2, f'splice {s / FPS:.1f}s') for s in starts]
pts.sort()
tiles = []
for f, lab in pts:
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{f / FPS:.3f}', '-i', V, '-frames:v', '1', '-vf', 'scale=270:480', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True).stdout
    if len(raw) < 270 * 480 * 3: continue
    im = np.frombuffer(raw, np.uint8).reshape(480, 270, 3).copy()
    cv2.putText(im, f'{int(f / FPS // 60):02d}:{f / FPS % 60:04.1f} {lab}'[:34], (3, 472), cv2.FONT_HERSHEY_SIMPLEX, .33, (0, 255, 255), 1)
    tiles.append(im)
cols = 10
for s in range(0, len(tiles), cols * 3):
    ch = tiles[s:s + cols * 3]
    while len(ch) % cols: ch.append(np.zeros_like(tiles[0]))
    rows = [np.concatenate(ch[i:i + cols], 1) for i in range(0, len(ch), cols)]
    cv2.imwrite(f'/home/user/work/analysis/qa_sheet_{s // (cols * 3):02d}.jpg', np.concatenate(rows, 0), [cv2.IMWRITE_JPEG_QUALITY, 85])
print(len(tiles), 'frames on', (len(tiles) + cols * 3 - 1) // (cols * 3), 'sheets')
