
import cv2
import numpy as np
import matplotlib.pyplot as plt


min_val, max_val = 0, 255

img : np.ndarray = cv2.imread('./lenna.png')     # read in BGR by default

img_original = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

contrast_range = 127

def on_change(val):
    center = 127.5
    min_val = max(0, int(center - val))
    max_val = min(255, int(center + val))

    # perform min-max normalization
    normalized_img = (img_original - np.min(img_original)) / (np.max(img_original) - np.min(img_original))
    # adjust the contrast of the image
    normalized_img = normalized_img * (max_val - min_val) + min_val

    normalized_img = np.uint8(normalized_img)
    cv2.imshow('Contrast', normalized_img)

cv2.imshow('Contrast', img_original)
cv2.createTrackbar('Contrast Range', 'Contrast', 0, contrast_range, on_change)
while True:
    key = cv2.waitKey(1)
    if key == ord('q') or cv2.getWindowProperty('Contrast', cv2.WND_PROP_VISIBLE) < 1:
        break
cv2.destroyAllWindows()
