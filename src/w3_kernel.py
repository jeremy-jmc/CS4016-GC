import numpy as np
import cv2
import matplotlib.pyplot as plt
from numba import jit, prange
from tqdm import tqdm

from fractions import Fraction
np.set_printoptions(formatter={'all': lambda x: str(Fraction(x).limit_denominator())})

img : np.ndarray = cv2.imread('../img/lenna.png')     # read in BGR by default
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
if img_rgb.ndim == 2:
    img_rgb = img_rgb[:, :, np.newaxis]


# -----------------------------------------------------------------------------
# Filter functions
# -----------------------------------------------------------------------------
def pascal_line(n):
    line = np.zeros(n)
    line[0] = 1
    for i in range(1, n):
        line[i] = line[i-1] * (n - i) // i
    return line

def get_filter(filter_type: str, order: int = 3):
    if filter_type == 'box':
        return np.ones((order, order)) / order**2
    elif filter_type == 'bartlett':
        # TODO: see np.bartlett
        filter = np.zeros((1, order))[0]
        filter[order//2] = order//2 + 1
        l = order//2 - 1
        r = order//2 + 1
        while l >= 0 or r < order:
            filter[l] = filter[r] = l + 1
            l -= 1
            r += 1
        
        kernel = (filter * filter.reshape(-1, 1)).astype(np.float64)
        kernel /= np.sum(kernel)
        return kernel
    elif filter_type == 'gaussian':
        filter = pascal_line(order)
        
        kernel = filter * filter.reshape(-1, 1)
        kernel /= np.sum(kernel)

        return kernel
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
            return np.nan # ValueError('Invalid order for laplacian filter')
    # elif filter_type == 'highpass':
    #     pass
    else:
        raise ValueError('Invalid filter type')


# print(get_filter('box', 5))
# print(get_filter('bartlett', 3))
# print(get_filter('gaussian', 5))
# print(get_filter('laplacian', 5))
# print(get_filter('highpass', 5))


# -----------------------------------------------------------------------------
# Convolution operation from scratch
# -----------------------------------------------------------------------------


@jit(nopython=True)
def convolution(image, kernel):
    height, width, channels = image.shape
    kernel_height, kernel_width = kernel.shape

    new_image = np.zeros((height, width, channels))
    for i in prange(height):
        for j in prange(width):
            for c in prange(channels):
                mat_base = np.zeros((kernel_height, kernel_width))
                mat_base[:min(kernel_height, height-i), :min(kernel_width, width-j)] = \
                    image[i:i+kernel_height, j:j+kernel_width, c]

                new_image[i, j, c] = np.sum(mat_base * kernel)

    return new_image.astype(np.uint8)

# -----------------------------------------------------------------------------
# Test
# -----------------------------------------------------------------------------

order_list = [3, 5, 7, 11, 19]
for filter in ['box', 'bartlett', 'gaussian', 'laplacian']:
    fig, ax = plt.subplots(1, len(order_list) + 1, figsize=(30, 6))
    print(filter)
    ax[0].imshow(img_rgb, cmap='gray')
    ax[0].axis('off')
    ax[0].set_title('Original')
    
    results = []
    for idx, order in enumerate(order_list):
        ax[idx + 1].axis('off')
        kernel = get_filter(filter, order)
        # print(kernel, np.sum(kernel))
        try:
            img_conv = convolution(img_rgb.copy(), kernel)
            results.append(img_conv)

            ax[idx + 1].imshow(img_conv, cmap='gray')
            ax[idx + 1].set_title(f'{filter} filter with order {order}')
        except Exception as e:
            continue
    plt.show()


    if filter in ['box', 'bartlett', 'gaussian', 'laplacian']:
        sz = min(len(results), len(order_list)) + 1
        fig, ax = plt.subplots(1, sz, figsize=(30, 6))

        ax[0].imshow(img_rgb, cmap='gray')
        ax[0].axis('off')
        ax[0].set_title('Original')

        for idx, tup in enumerate(zip(order_list, results)):
            order, img_conv = tup
            ax[idx + 1].axis('off')
            img_diff = img_rgb - img_conv
            ax[idx + 1].imshow(img_diff, cmap='gray')
            ax[idx + 1].set_title(f'inverted {filter} filter with order {order}')
        plt.show()
