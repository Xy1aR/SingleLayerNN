import numpy as np
import cv2


def pic_upscale(pixels):
    pixels = np.asarray(pixels)
    pixels[pixels == 0] = 1
    pixels[pixels == 255] = 0
    pic = np.reshape(pixels, (28, 28))
    pic = pic[~np.all(pic == 0, axis=1)]
    pic = pic[:, ~np.all(pic == 0, axis=0)]
    row, col = pic.shape

    if row > col:
        while row > col:
            pic = np.insert(pic, 0, np.zeros(row, dtype=int), axis=1)
            pic = np.append(pic, np.zeros((row, 1), dtype=int), axis=1)
            col += 2
            if row < col:
                pic = np.vstack([pic, np.zeros(col, dtype=int)])
    elif row < col:
        while row < col:
            pic = np.insert(pic, 0, np.zeros(col, dtype=int), axis=0)
            pic = np.vstack([pic, np.zeros(col, dtype=int)])
            row += 2
            if row > col:
                pic = np.append(pic, np.zeros((row, 1), dtype=int), axis=1)

    resized = cv2.resize(pic, (28, 28), interpolation=0)
    return list(np.reshape(resized, -1))
