"""
Write a function that computes the area of a convex polygon.

IDEA:
   Cross product of two vectors gives the area of the parallelogram formed by the two vectors.
   The area of a triangle is half of the area of the parallelogram formed by the two vectors.
   The area of a convex polygon is the sum of the areas of the triangles formed by the first vertex and two consecutive vertices.
INPUT:
    A polygon that consists of n vertices (x_1,y_1), (x_2,y_2), ... , (x_n,y_n). 
    The vertices (x_i,y_i) and (x_{i+1},y_{i+1}) are adjacent for i=1, 2, .., n-1, 
    and the vertices (x_1,y_1) and (x_n,y_n) are also adjacent in counterclockwise order.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_polygon(polygon: np.ndarray, result: float) -> None:
    """Plot a polygon in 2D space"""
    n = len(polygon)

    plt.figure(figsize=(5, 5))
    for i in range(n):
        plt.plot(*polygon[i], 'o', color='blue')
        plt.plot([polygon[i][0], polygon[(i + 1) % n][0]],
                 [polygon[i][1], polygon[(i + 1) % n][1]], linestyle='-', color='red')
        plt.text(polygon[i][0] + 0.1, polygon[i][1], f'{i + 1}',
                 fontsize=12, color='black', ha='right')

    title = f'Area: {result}'
    plt.title(title)
    plt.show()

# -----------------------------------------------------------------------------
# Algorithm solution
# -----------------------------------------------------------------------------


def cross_product_2d(a: np.ndarray, b: np.ndarray) -> float:
    """Return the cross product of two 2D vectors a and b"""
    return a[0] * b[1] - a[1] * b[0]


def area_convex_polygon(polygon: np.ndarray) -> float:
    """Return the area of a convex polygon"""
    n = len(polygon)
    parallelogram_areas = [cross_product_2d(polygon[i] - polygon[0], polygon[(i + 1) % n] - polygon[0]) 
                           for i in range(1, n)]
    area = abs(sum(parallelogram_areas)) / 2
    return area

# -----------------------------------------------------------------------------
# Test
# -----------------------------------------------------------------------------


def test(polygon: np.ndarray, expected: float):
    result = area_convex_polygon(polygon)
    if np.isclose(result, expected):
        print('Test passed')
    else:
        print(f'Test failed: expected {expected} but got {result}')
        plot_polygon(polygon, result)


square = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
test(square, 1.0)

triangle = np.array([[0, 0], [1, 0], [0, 1]])
test(triangle, 0.5)

pentagon = np.array([[0, 0], [1, 0], [1, 1], [0.5, 1.5], [0, 1]])
test(pentagon, 1.25)

hexagon = np.array([[0, 0], [1, 0], [1.5, 0.5], [1, 1], [0, 1], [-0.5, 0.5]])
test(hexagon, 1.5)
