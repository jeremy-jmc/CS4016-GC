"""
Given a triangle T (given by its vertices) and an input point P, decide if P ∈ T.

IDEA 1:
    Sum the area of all triangles formed by the point and 2 consecutive points of the triangle
    If the sum of the areas is equal to the area of the original triangle, then the point is inside the triangle

IDEA 2:
    For each triangle side, check if the point is to the left with cross product

INPUT:
    The polygon/triangle consists of n vertices (x_1,y_1),(x_2,y_2), ... ,(x_n,y_n). 
    The vertices (x_i,y_i) and (x_{i+1},y_{i+1}) are adjacent for i=1, 2, .., n-1, 
    and the vertices (x_1,y_1) and (x_n,y_n) are also adjacent in counterclockwise order.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_point_polygon(polygon: np.ndarray, point: np.ndarray, result: bool) -> None:
    """Plot a polygon and a point in 2D space"""
    n = len(polygon)

    plt.figure(figsize=(5, 5))
    plt.plot(*point, 'o', color='black')
    plt.text(point[0] + 0.1, point[1], 'P', color='black', ha='right')
    for i in range(n):
        plt.plot(*polygon[i], 'o', color='blue')
        plt.plot([polygon[i][0], polygon[(i + 1) % n][0]],
                 [polygon[i][1], polygon[(i + 1) % n][1]], linestyle='-', color='red')
        plt.text(polygon[i][0] + 0.1, polygon[i][1],
                 f'{i + 1}', fontsize=12, color='black', ha='right')

    title = 'Result: ' + \
        str('Point in triangle' if result else 'Point outside triangle')
    plt.title(title)
    plt.show()


# -----------------------------------------------------------------------------
# Solution
# -----------------------------------------------------------------------------

LEFT = 1
RIGHT = -1
COLLINEAR = 0


def sign_of_cross_product(a: np.ndarray, b: np.ndarray) -> float:
    """Return the sign of the cross product between vectors a and b centered at the origin"""
    return np.sign(a[0] * b[1] - a[1] * b[0])


def orientation(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> int:
    """Check the orientation of 3 points a, b, c 
    calculating the cross product between vectors ab and bc

    Returns:
        int: 1 if counterclockwise, -1 if clockwise, 0 if collinear
    """
    s = sign_of_cross_product(a - b, c - b)
    if s > 0:
        return LEFT
    elif s < 0:
        return RIGHT
    return COLLINEAR


def inside_polygon(polygon: np.ndarray, point: np.ndarray) -> bool:
    """Check if a point is inside a polygon using the orientation of the point 
    with respect to the polygon edges
    """
    n = len(polygon)
    z_components = [
        orientation(polygon[(i + 1) % n], polygon[i], point)
        for i in range(n)
    ]
    # print(z_components)

    result = all(z != RIGHT for z in z_components)
    return result


# -----------------------------------------------------------------------------
# Test cases
# -----------------------------------------------------------------------------

def test(polygon, point, expected: bool) -> None:
    result = inside_polygon(polygon, point)
    if result != expected:
        print(f'Expected: {expected}, got: {result}')
        plot_point_polygon(polygon, point, result)
    else:
        print('Test passed')


triangle = np.array([[0, 0], [2, 0], [1, 2]])
point_inside = np.array([1, 1])
point_outside = np.array([3, 1])
point_on_edge = np.array([1, 0])
point_on_vertex = np.array([0, 0])
point_outside_collinear = np.array([3, 0])

test(triangle, point_inside, True)
test(triangle, point_outside, False)
test(triangle, point_on_edge, True)
test(triangle, point_on_vertex, True)
test(triangle, point_outside_collinear, False)
