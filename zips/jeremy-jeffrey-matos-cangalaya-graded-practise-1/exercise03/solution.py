
import cv2
import numpy as np
import matplotlib.pyplot as plt


min_val, max_val = 0, 255

img : np.ndarray = cv2.imread('../lenna.png')     # read in BGR by default

img_original = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

contrast_range = 127

def on_change(val):
    center = 127.5
    min_val = max(0, int(center - val))
    max_val = min(255, int(center + val))

    new_img_to_show = cv2.normalize(img_original, None, min_val, max_val, cv2.NORM_MINMAX)
    cv2.imshow('Contrast', new_img_to_show)

cv2.imshow('Contrast', img_original)
cv2.createTrackbar('Contrast Range', 'Contrast', 0, contrast_range, on_change)
cv2.waitKey(0)
cv2.destroyAllWindows()
