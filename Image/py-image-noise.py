import noise
import numpy as np
from PIL import Image

w, h = 800, 600
scale = 100.0

array = np.zeros((h, w, 3), dtype=np.uint8)
for y in range(h):
    for x in range(w):
        val = noise.pnoise2(x/scale, y/scale, octaves=6)
        gray = int((val + 0.2) * 255)
        array[y, x] = (gray, gray, gray)

img = Image.fromarray(array)
img.show()
