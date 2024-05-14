import random
import cv2
import numpy as np

White = (255, 255, 255)
Red = (0, 0, 255)
Green = (0, 255, 0)
Blue = (255, 0, 0)
Yellow = (0, 255, 255)


# height_pixels: number of pixels in height
# width_pixels: number of pixels in width
# height_rectangles: number of rectangles in height
# width_rectangles: number of rectangles in width
# colors: list of colors to be used
# strategy: either 'random' or 'sequential'.
def create_board(height_pixels, width_pixels, height_rectangles, width_rectangles, colors, strategy):
    img = np.zeros((height_pixels, width_pixels, 3), dtype=np.uint8)
    rectangle_height = int(height_pixels / height_rectangles)
    rectangle_width = int(width_pixels / width_rectangles)
    for r in range(height_rectangles):
        for c in range(width_rectangles):

            if strategy == "random":
                col = random.choice(colors)
            else:
                col = colors[(r + c) % len(colors)]

            r_from = r * rectangle_height
            r_to = (r + 1) * rectangle_height
            c_from = c * rectangle_width
            c_to = (c + 1) * rectangle_width

            img[r_from:r_to, c_from:c_to, :] = col

    return img


def main():
    colors = [White, Red, Green, Blue, Yellow]
    img1 = create_board(100, 200, 10, 10, colors, "random")
    img2 = create_board(100, 200, 10, 10, colors, "sequential")

    cv2.imshow("img1", img1)
    cv2.imshow("img2", img2)

    cv2.waitKey(0)


if __name__ == "__main__":
    main()
