import cv2
import requests
import numpy as np
import os

def download_image(source):
    """Download image from URL or load from local path."""
    source = source.strip().strip('"').strip("'")

    if source.startswith("http://") or source.startswith("https://"):
        try:
            headers = {
                "User-Agent": "ImageDownloader/1.0 (https://example.com/contact)"
            }
            response = requests.get(source, headers=headers, stream=True, timeout=15)
            response.raise_for_status()
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError("Downloaded data is not a valid image")
            return image
        except Exception as e:
            return None
    else:
        if os.path.exists(source):
            return cv2.imread(source)
        return None

def resize_to_screen(img, max_width=1280, max_height=720):
    """Resize image to fit on screen, keeping aspect ratio and centering it."""
    h, w = img.shape[:2]
    scale = min(max_width / w, max_height / h, 1)
    new_w, new_h = int(w * scale), int(h * scale)

    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    canvas = np.zeros((max_height, max_width, 3), dtype=np.uint8)
    x_offset = (max_width - new_w) // 2
    y_offset = (max_height - new_h) // 2
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized

    return canvas
