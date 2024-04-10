

import cv2
import numpy as np
import matplotlib.pyplot as plt

img_original : np.ndarray = cv2.imread('../img/lenna.png')     # read in BGR by default

# -----------------------------------------------------------------------------
# Brightness
# -----------------------------------------------------------------------------

img_original = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
print(img_original)
plt.imshow(img_original, cmap='gray')
plt.show()

img_brightness = cv2.add(img_original, -250).astype(np.uint8)

print(img_brightness)
plt.imshow(img_brightness, cmap='gray')
plt.show()


def on_change(val):
    return cv2.add(img_original, val).astype(np.uint8)


cv2.imshow('Brightness', img_original)
cv2.createTrackbar('slider', 'Brightness', -127, 127, on_change)
cv2.waitKey(0)
cv2.destroyAllWindows()

# -----------------------------------------------------------------------------
# Contrast
# -----------------------------------------------------------------------------

plt.hist(img_original.ravel(), 256, [0, 256])
plt.show()

"""
Contrast is the variation of color

The bigger is the variation of color the easier we notice the difference


The range is the maximum value minus the minimum value

(i - min)/(max - min) * 255
"""

img_contrast = cv2.normalize(img_original, None, 0, 255, cv2.NORM_MINMAX)
