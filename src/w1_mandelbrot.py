"""
https://en.wikipedia.org/wiki/Mandelbrot_set

complex plane
fractal curve
    Un fractal es un objeto geométrico cuya estructura básica, fragmentada o aparentemente irregular, se repite a diferentes escalas.
    https://en.wikipedia.org/wiki/Fractal_curve
"""

import cv2
import cmath
import math
import colorsys
import numpy as np
import matplotlib.pyplot as plt


def generate_mandelbrot(N: int = 1000, max_iter: int = 50, save: bool = False) -> np.ndarray:
    """An implementation of naive "scape time algorithm" 
    Reference: https://en.wikipedia.org/wiki/Mandelbrot_set

    Args:
        N (int, optional): image width/height. Defaults to 1000.
        max_iter (int, optional): max iterations to check if complex number diverges. Defaults to 50.
        save (bool, optional): flag to save the file. Defaults to False.

    Returns:
        np.ndarray: mandelbrot set image
    """

    img: np.ndarray = np.full((N, N), 255, dtype='uint8')

    for i in range(N):
        for j in range(N):
            x0 = -2.00 + j * (0.47 - (-2.00)) / N
            y0 = -1.12 + i * (1.12 - (-1.12)) / N

            x, y = 0, 0

            it = 0
            while (x**2 + y**2 <= 4 and it < max_iter):
                x_temp = x**2 - y**2 + x0
                y = 2*x*y + y0
                x = x_temp

                it += 1
            img[i, j] -= it

    # save numpy array
    if save:
        np.save('mandelbrot.npy', img)

    return img


def visualize_array(array: np.ndarray, library: str = 'matplotlib') -> None:
    if library == 'matplotlib':
        plt.figure(figsize=(12, 12))
        plt.imshow(array, cmap='plasma')
        plt.axis('off')
        plt.show()
    elif library == 'opencv':
        normalized_array = cv2.normalize(array, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        color_mapped_image = cv2.applyColorMap(normalized_array, cv2.COLORMAP_PLASMA)
        cv2.namedWindow('Mandelbrot Set', cv2.WINDOW_NORMAL)
        cv2.imshow('Mandelbrot Set', color_mapped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        raise ValueError(
            f'Function visualize_array: library "{library}" not supported')

# print(plt.colormaps())
img = np.load('./mandelbrot.npy').astype('uint8')
# generate_mandelbrot()

visualize_array(img, library='matplotlib')
# visualize_array(img, library='opencv')


"""
DONE: Wikipedia pseudocode

DONE: https://medium.com/swlh/visualizing-the-mandelbrot-set-using-python-50-lines-f6aa5a05cf0f
    TODO: https://nextjournal.com/lazarus/aggregating-values-to-the-mandelbrot-and-julia-sets
TODO: https://levelup.gitconnected.com/mandelbrot-set-with-python-983e9fc47f56
TODO: https://medium.com/@hfahmida/intriguing-visualizations-of-mandelbrot-set-using-matplotlib-library-python-d3f56450841e
TODO: https://medium.com/@krzysztof.pieranski/mandelbrot-set-with-pytorch-d006827fb887
"""
