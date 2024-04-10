"""
https://en.wikipedia.org/wiki/Mandelbrot_set

complex plane
fractal curve
    Un fractal es un objeto geométrico cuya estructura básica, fragmentada o aparentemente irregular, se repite a diferentes escalas.
    https://en.wikipedia.org/wiki/Fractal_curve
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

N = 100
img: np.ndarray = np.full((N, N), 255)


"""
for each pixel (Px, Py) on the screen do
    x0 := scaled x coordinate of pixel (scaled to lie in the Mandelbrot X scale (-2.00, 0.47))
    y0 := scaled y coordinate of pixel (scaled to lie in the Mandelbrot Y scale (-1.12, 1.12))
    x := 0.0
    y := 0.0
    iteration := 0
    max_iteration := 1000
    while (x^2 + y^2 ≤ 2^2 AND iteration < max_iteration) do
        xtemp := x^2 - y^2 + x0
        y := 2*x*y + y0
        x := xtemp
        iteration := iteration + 1
    color := palette[iteration]
    plot(Px, Py, color)


https://medium.com/swlh/visualizing-the-mandelbrot-set-using-python-50-lines-f6aa5a05cf0f    
https://levelup.gitconnected.com/mandelbrot-set-with-python-983e9fc47f56
https://medium.com/@hfahmida/intriguing-visualizations-of-mandelbrot-set-using-matplotlib-library-python-d3f56450841e
https://medium.com/@krzysztof.pieranski/mandelbrot-set-with-pytorch-d006827fb887
"""

