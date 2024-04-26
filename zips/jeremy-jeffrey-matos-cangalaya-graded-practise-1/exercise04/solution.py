import numpy as np
import cv2
import matplotlib.pyplot as plt
from numba import jit, prange
import os

def projection(img: np.ndarray, mask: np.ndarray) -> np.ndarray:
    w, h = img.shape[:2]
    new_img = np.zeros((w, h, 3))
    for i in range(w):
        for j in range(h):
            u, v = img[i, j], mask[i, j]
            new_img[i, j] = v * np.dot(u, v) / np.dot(v, v)
    
    return new_img.astype(np.uint8)


@jit(nopython=True)
def mask(img: np.ndarray) -> np.ndarray:
    height, width, _ = img.shape

    filter_array = np.full(img.shape, 255, dtype=np.uint8)

    radius = min(height, width) // 2
    center = (width // 2, height // 2)

    for i in prange(height):
        for j in prange(width):
            if np.sqrt((i - center[1])**2 + (j - center[0])**2) < radius:
                filter_array[i, j] = [0, 0, 255]
    
    return filter_array


if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)

    img : np.ndarray = cv2.imread('./lenna.png')     # read in BGR by default
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    projected_img = projection(img_rgb, mask(img_rgb))

    cv2.imwrite('output/lenna-colorscale.png', 
                cv2.cvtColor(projected_img, cv2.COLOR_RGB2BGR))


"""
plt.imshow(mask(img))
plt.xticks([]), plt.yticks([])
plt.show()


plt.imshow(img_rgb)
plt.xticks([]), plt.yticks([])
plt.show()

plt.imshow(projected_img)
plt.xticks([]), plt.yticks([])
plt.show()
"""