import numpy as np
import cv2
import matplotlib.pyplot as plt
from numba import jit, prange
from tqdm import tqdm
import os

from fractions import Fraction
np.set_printoptions(formatter={'all': lambda x: str(Fraction(x).limit_denominator())})


# -----------------------------------------------------------------------------
# Filter functions
# -----------------------------------------------------------------------------
def pascal_line(n: int) -> np.ndarray:
    line = np.zeros(n)
    line[0] = 1
    for i in range(1, n):
        line[i] = line[i-1] * (n - i) // i
    return line


def bartlett_line(order: int) -> np.ndarray:    
    line = np.zeros((1, order))[0]
    line[order//2] = order//2 + 1
    l = order//2 - 1
    r = order//2 + 1
    while l >= 0 or r < order:
        line[l] = line[r] = l + 1
        l -= 1
        r += 1
    return line


def get_filter(filter_type: str, order: int = 3) -> np.ndarray:
    kernel = None

    if filter_type == 'box':
        kernel = np.ones((order, order)) / order**2
    elif filter_type == 'bartlett':
        line = bartlett_line(order)
        
        kernel = (line * line.reshape(-1, 1)).astype(np.float64)
        kernel /= np.sum(kernel)

    elif filter_type == 'gaussian':
        line = pascal_line(order)
        
        kernel = line * line.reshape(-1, 1)
        kernel /= np.sum(kernel)
    elif filter_type == 'laplacian':
        if order == 3:
            mat = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
            return mat
        elif order == 5:
            mat = np.array([[0, 0, 1, 0, 0], 
                             [0, 1, 2, 1, 0], 
                             [1, 2, -16, 2, 1], 
                             [0, 1, 2, 1, 0], 
                             [0, 0, 1, 0, 0]])
            return mat
        else:
            raise ValueError('Invalid order for laplacian filter')
    else:
        raise ValueError('Invalid filter_type name. Options: ["box", "bartlett", "gaussian"]')
    
    return kernel


# -----------------------------------------------------------------------------
# Convolution operation from scratch
# -----------------------------------------------------------------------------


@jit(nopython=True)
def convolution(image: np.array, kernel: np.array) -> np.array:
    height, width, channels = image.shape
    kernel_height, kernel_width = kernel.shape

    new_image = np.zeros((height, width, channels))
    for i in prange(height):
        for j in prange(width):
            for c in prange(channels):
                kernel_window = np.zeros((kernel_height, kernel_width))
                kernel_window[:min(kernel_height, height-i), :min(kernel_width, width-j)] = \
                    image[i:i+kernel_height, j:j+kernel_width, c]

                new_image[i, j, c] = np.sum(kernel_window * kernel)

    return new_image.astype(np.uint8)


if __name__ == '__main__':
    workdir = os.path.join(os.getcwd(), 'output', 'img')
    os.makedirs(workdir, exist_ok=True)

    img : np.ndarray = cv2.imread('../lenna.png')     # read in BGR by default
    cv2.imwrite(os.path.join(workdir, 'original.png'), img)
    cv2.imwrite(os.path.join(workdir, 'original_grayscale.png'), cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

    img_grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)[:, :, np.newaxis]
    img_bgr = img.copy()

    order_scales = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]

    for folder, img in zip(['grayscale', 'rgb'], [img_grayscale, img_bgr]):
        for kernel_type in ['box', 'bartlett', 'gaussian', 'laplacian']:
            for order in order_scales:
                if kernel_type == 'laplacian' and order > 5:
                    continue
                kernel = get_filter(kernel_type, order)
                filtered_img = convolution(img, kernel)

                file_name = os.path.join(workdir, f'{kernel_type}_{folder}_{order}.png')
                cv2.imwrite(file_name, filtered_img)

        