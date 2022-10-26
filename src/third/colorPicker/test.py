from PIL import Image
import numpy as np
a = np.full((1, 1), 256)
im = Image.fromarray(a, mode="L")
im.getpixel((0, 0))  # 44
im = Image.fromarray(a, mode="RGB")
im.getpixel((0, 0))  # (44, 1, 0)

if __name__ == '__main__':
    pass