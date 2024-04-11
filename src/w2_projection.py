import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import random

img : np.ndarray = cv2.imread('../img/lenna.png')     # read in BGR by default
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def generate_random_rgb_mask(img_input: np.array, 
                             tiles: int = 10) -> np.array:
    """Generate a table with tiles of different RGB colors

    Args:
        img_input (np.array): input image
        tiles (int, optional): tile number in width and height. Defaults to 10.

    Returns:
        np.array: projection mask
    """
    w, h = img_input.shape[:2]

    random_mask = np.full((w, h, 3), 0, dtype='float64')
    available_colors = [[0, 0, 255], [255, 0, 0], [0, 255, 0], [255, 255, 255], [255, 255, 0]]

    width_range, height_range = w // tiles, h // tiles

    for i in range(0, w, width_range):
        for j in range(0, h, height_range):
            random_mask[i:i+width_range, j:j+height_range, :] = \
                random.choice(available_colors)

    return random_mask


def project_colors(img_input: np.array, 
                   vector_to_project: list = [255, 255, 255]
                   ):
    """Project each pixel (color) of the image to a vector e.g. achromatic line

    Args:
        img_input (np.array): input image
        vector_to_project (list, optional): Vector to calculate the projection of each color. Defaults to the achromatic line.
    """
    w, h = img_input.shape[:2]
    vector_to_project = np.array(vector_to_project)

    # generate projection mask
    mask = np.zeros((w, h, 3))
    if vector_to_project.ndim == 1:
        mask[:, :, :] = vector_to_project
    else:
        assert vector_to_project.shape == img_input.shape, \
            "projecting mask does not have the same shape of img_input"
        mask = vector_to_project.copy()

    # do projections
    new_img = np.zeros((w, h, 3))
    for i in range(w):
        for j in range(h):
            u, v = img_input[i, j], mask[i, j]
            new_img[i, j] = v * np.dot(u, v) / np.dot(v, v)

    plt.imshow(new_img.astype(np.uint8))
    plt.axis('off')
    plt.show()


plt.imshow(img_rgb)
plt.axis('off')
plt.show()

project_colors(img_rgb)
project_colors(img_rgb, [255, 0, 0])  # R
project_colors(img_rgb, [0, 0, 255])  # G
project_colors(img_rgb, [0, 255, 0])  # B
mask = generate_random_rgb_mask(img_rgb, 8)
plt.imshow(mask)
plt.axis('off')
plt.show()
project_colors(img_rgb, mask)

"""
input 2 images(image, masks)
"""





