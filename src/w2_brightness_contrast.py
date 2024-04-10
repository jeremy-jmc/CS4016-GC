

import cv2
import numpy as np
import matplotlib.pyplot as plt

img : np.ndarray = cv2.imread('../img/lowcontrast.png')     # read in BGR by default

# -----------------------------------------------------------------------------
# Brightness
# -----------------------------------------------------------------------------

# img_original = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
# # print(img_original)
# # plt.imshow(img_original, cmap='gray')
# # plt.show()

# # img_brightness = cv2.add(img_original.copy(), -250).astype(np.uint8)

# # print(img_brightness)
# # plt.imshow(img_brightness, cmap='gray')
# # plt.show()

# def on_change(val):
#     new_img_to_show = cv2.add(img_original.copy(), val).astype(np.uint8)
#     cv2.imshow('Brightness', new_img_to_show)

# cv2.imshow('Brightness', img_original)
# cv2.createTrackbar('Brightness', 'Brightness', 0, 127, on_change)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# -----------------------------------------------------------------------------
# Contrast
# -----------------------------------------------------------------------------

# plt.hist(img_original.ravel(), 256, [0, 256])
# plt.show()

"""
Contrast is the variation of color

The bigger is the variation of color the easier we notice the difference


The range is the maximum value minus the minimum value

(i - min)/(max - min) * 255
"""

img_original = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# print(img_original)
# plt.imshow(img_original)
# cv2.imshow('original', img_original)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

min_val, max_val = 0, 255

def on_change_min(val):
    global min_val, max_val
    min_val = val
    # if (min_val > max_val):
    #     min_val, max_val = max_val, min_val

    img_contrast = cv2.normalize(img_original, None, min_val, max_val, cv2.NORM_MINMAX)
    cv2.imshow('contrast', img_contrast)

def on_change_max(val):
    global min_val, max_val
    max_val = val

    # if (max_val < min_val):
    #     max_val, min_val = min_val, max_val

    img_contrast = cv2.normalize(img_original, None, min_val, max_val, cv2.NORM_MINMAX)
    cv2.imshow('contrast', img_contrast)

cv2.namedWindow('contrast')
cv2.createTrackbar('Min Value', 'contrast', 0, 255, on_change_min)
cv2.createTrackbar('Max Value', 'contrast', 255, 255, on_change_max)
cv2.waitKey(0)
cv2.destroyAllWindows()

# TODO: definir una estrategia para 1 solo slider
