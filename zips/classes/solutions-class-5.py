import cv2
import numpy as np


# img: grayscale image
# contrast: real value in [0, 1] that specifies how much to stretch the range of
# the image from [color_min, color_max] to [0, 255].
# The range will be mapped to:
# [color_min - contrast * color_min, color_max + contrast * (255 - color_max)]
def change_contrast(img, contrast):
    ret = img.copy().astype(np.float64)

    color_min = img.min()
    color_max = img.max()
    mapped_min = color_min - int(contrast * color_min)
    mapped_max = color_max + int(contrast * (255 - color_max))

    ret -= color_min
    ret *= (mapped_max - mapped_min) / (color_max - color_min)
    ret += mapped_min
    ret = ret.astype(np.uint8)

    return ret


# img: grayscale image
# brightness: integer value in [-127, 128] that specifies how much to increase the
# value of the pixels.
def change_brighness(img, brightness):
    ret = img.copy()

    if brightness > 0:
        np.clip(ret, 0, 255 - brightness, ret)
        ret = ret + brightness

    else:
        np.clip(ret, -1 * brightness, 255, ret)
        abs_brightness = -brightness
        ret = ret - abs_brightness

    return ret


# FILENAME = "lenna.png"
FILENAME = "lowcontrast.png"
glob_brigthness = 0
glob_contrast = 0

img_original = cv2.imread(FILENAME, cv2.IMREAD_GRAYSCALE)
img_brightness = change_brighness(img_original, glob_brigthness)
img_contrast = change_contrast(img_original, glob_contrast)

cv2.imshow("original", img_original)
cv2.imshow("brightness", img_brightness)
cv2.imshow("contrast", img_contrast)


## GUI
def on_change_brightness(val):
    global glob_brigthness, img_original
    glob_brigthness = val - 127
    img_brightness = change_brighness(img_original, glob_brigthness)
    cv2.imshow("brightness", img_brightness)


def on_change_contrast(val):
    global glob_contrast, img_original
    glob_contrast = float(val) / 255.0
    img_contrast = change_contrast(img_original, glob_contrast)
    cv2.imshow("contrast", img_contrast)


cv2.createTrackbar("brightness", "brightness", 127, 255, on_change_brightness)
cv2.createTrackbar("contrast", "contrast", 0, 255, on_change_contrast)

cv2.waitKey(0)
cv2.destroyAllWindows()
