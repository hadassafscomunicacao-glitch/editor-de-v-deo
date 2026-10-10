"""Person matte using MediaPipe multiclass selfie segmenter (local model)."""
import numpy as np, cv2, mediapipe as mp
from mediapipe.tasks import python as mpp
from mediapipe.tasks.python import vision

CROP_Y0, CROP_Y1 = 380, 1640   # band that contains both participants (camera is locked)
SEG_SIZE = 512

class Segmenter:
    def __init__(self, model='models/selfie_multiclass_256x256.tflite'):
        o = vision.ImageSegmenterOptions(base_options=mpp.BaseOptions(model_asset_path=model),
                                         output_category_mask=False, output_confidence_masks=True)
        self.seg = vision.ImageSegmenter.create_from_options(o)

    def person_prob(self, rgb_u8):
        """rgb_u8 full frame HxWx3 uint8 -> low-res person probability for the crop band (SEG_SIZE x SEG_SIZE)."""
        crop = rgb_u8[CROP_Y0:CROP_Y1]
        small = cv2.resize(crop, (SEG_SIZE, SEG_SIZE), interpolation=cv2.INTER_AREA)
        r = self.seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(small)))
        bg = np.squeeze(r.confidence_masks[0].numpy_view())
        return (1.0 - bg).astype(np.float32)

def expand_matte(prob_small, H=1920, W=1080, erode_px=3, feather=5.0):
    """low-res prob -> full-res soft matte with slight choke (avoids bright fringe/halo) and feather."""
    band = cv2.resize(prob_small, (W, CROP_Y1 - CROP_Y0), interpolation=cv2.INTER_CUBIC)
    m = np.zeros((H, W), np.float32)
    m[CROP_Y0:CROP_Y1] = np.clip(band, 0, 1)
    # fade the band edges so no seam can appear
    ramp = 40
    m[CROP_Y0:CROP_Y0 + ramp] *= np.linspace(0, 1, ramp)[:, None]
    m[CROP_Y1 - ramp:CROP_Y1] *= np.linspace(1, 0, ramp)[:, None]
    m = np.clip((m - 0.5) * 2.2 + 0.5, 0, 1)        # sharpen soft model output
    if erode_px:
        m = cv2.erode(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * erode_px + 1,) * 2))
    m = cv2.GaussianBlur(m, (0, 0), feather)
    return m
