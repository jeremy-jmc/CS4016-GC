import cv2
import numpy as np
from aux import *


# This approach solves the problem mentioned.
def change_colorscale_of_one_pixel(color_from, color_to):
    if color_to[0] == 0 and color_to[1] == 0 and color_to[2] == 0:
        color_to = [1, 1, 1]

    max_color_from = float(max(color_from))
    max_color_to = float(max(color_to))

    return [int(float(x) * max_color_from / max_color_to) for x in color_to]


def change_scale_of_all_pixels_to_fixed_colorscale(img, colorscale):
    h, w, _ = img.shape
    ret = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(w):
        for j in range(h):
            ret[j, i] = change_colorscale_of_one_pixel(img[j, i], colorscale)

    return ret


def change_scale_of_all_pixels_to_variable_colorscale(img, img_colorscales):
    h, w, _ = img.shape
    ret = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(w):
        for j in range(h):
            ret[j, i] = change_colorscale_of_one_pixel(img[j, i], img_colorscales[j, i])

    return ret


img_input = cv2.imread("lenna.png")
h, w, _ = img_input.shape

output_red = change_scale_of_all_pixels_to_fixed_colorscale(img_input, Red)
output_green = change_scale_of_all_pixels_to_fixed_colorscale(img_input, Green)
output_blue = change_scale_of_all_pixels_to_fixed_colorscale(img_input, Blue)
output_black = change_scale_of_all_pixels_to_fixed_colorscale(img_input, White)

board_10x10 = create_board(height_pixels=h, width_pixels=w, height_rectangles=10, width_rectangles=10, colors=[Red, Green, Blue, White, Yellow], strategy="random")
board_2x2 = create_board(height_pixels=h, width_pixels=w, height_rectangles=2, width_rectangles=2, colors=[Red, Green, Blue, White, Yellow], strategy="sequential")

output_10x10 = change_scale_of_all_pixels_to_variable_colorscale(img_input, board_10x10)
output_2x2 = change_scale_of_all_pixels_to_variable_colorscale(img_input, board_2x2)

cv2.imwrite("output/red.png", output_red)
cv2.imwrite("output/green.png", output_green)
cv2.imwrite("output/blue.png", output_blue)
cv2.imwrite("output/black.png", output_black)
cv2.imwrite("output/10x10.png", output_10x10)
cv2.imwrite("output/2x2.png", output_2x2)
cv2.imwrite("output/board_10x10.png", board_10x10)
cv2.imwrite("output/board_2x2.png", board_2x2)
