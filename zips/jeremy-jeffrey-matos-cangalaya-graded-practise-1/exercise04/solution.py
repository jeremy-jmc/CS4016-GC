import numpy as np
import cv2
import matplotlib.pyplot as plt
from numba import jit, prange

@jit(nopython=True)
def mask(img: np.array) -> np.array:
    height, width, _ = img.shape

    filter_array = np.full(img.shape, 255, dtype=np.uint8)

    radius = min(height, width) // 2
    center = (width // 2, height // 2)

    for i in prange(height):
        for j in prange(width):
            if np.sqrt((i - center[1])**2 + (j - center[0])**2) < radius:
                filter_array[i, j] = [0, 0, 255]
    
    return filter_array


img : np.ndarray = cv2.imread('../lenna.png')     # read in BGR by default

plt.imshow(mask(img))
plt.axis('off')
plt.show()

print(img.shape)