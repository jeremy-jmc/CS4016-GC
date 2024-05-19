"""
Write a function that receives a list of vertices of a polygon, given by its coordinates, and decides if the polygon convex or not.

IDEA: sort the vertices by the angle they form with the first vertex. Then, check if the polygon is convex by checking the sign of the cross product of the vectors formed by the sorted vertices.

To check the convexity of a polygon, you can think about it like this: 
    If you move along the sides of the polygon and you just have to move to the left or the right, then it is convex. 
    If you have to change the direction at least once, then it is not convex. 
    In this way it doesn't matter if you walk along the sides in clockwise or counterclockwise direction.

INPUT:
    A polygon that consists of n vertices (x_1,y_1), (x_2,y_2), ... ,(x_n,y_n). 
    The vertices (x_i, y_i) and (x_{i+1}, y_{i+1}) are adjacent for i=1, 2, .., n-1, 
    and the vertices (x_1, y_1) and (x_n, y_n) are also adjacent in counterclockwise order.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_polygon(polygon: np.ndarray, result: bool) -> None:
    """Plot a polygon in 2D space"""
    n = len(polygon)

    plt.figure(figsize=(5, 5))
    for i in range(n):
        plt.plot(*polygon[i], 'o', color='blue')
        plt.plot([polygon[i][0], polygon[(i + 1) % n][0]],
                 [polygon[i][1], polygon[(i + 1) % n][1]], linestyle='-', color='red')
        plt.text(polygon[i][0] + 0.1, polygon[i][1], f'{i + 1}',
                 fontsize=12, color='black', ha='right')

    title = f'Convex: {result}'
    plt.title(title)
    plt.show()


# -----------------------------------------------------------------------------
# Algorithm solution
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


def is_convex(polygon: np.ndarray) -> bool:
    """Check if a polygon is convex or not
    """

    # ensure that the points are in the correct format (counter-clockwise order)
    pivot = min(polygon, key=lambda p: (p[0], p[1]))

    def slope_wrt_pivot(idx: np.ndarray) -> np.ndarray:
        delta_y = polygon[idx][:, 1] - pivot[1]
        delta_x = polygon[idx][:, 0] - pivot[0]

        slopes = np.zeros(delta_y.shape)
        mask_zero = delta_x == 0
        slopes[mask_zero] = np.inf
        slopes[~mask_zero] = np.divide(delta_y[~mask_zero], 
                                       delta_x[~mask_zero])

        return slopes

    indices = np.array(range(len(polygon)))
    predicate = slope_wrt_pivot(indices)
    order = np.argsort(predicate)
    polygon = polygon[order]

    # check convexity
    n = len(polygon)
    z_components = [
        orientation(polygon[(i + 2) % n], polygon[(i + 1) % n], polygon[i])
        for i in range(n)
    ]
    result = all(z == LEFT for z in z_components)
    return result

# -----------------------------------------------------------------------------
# Test
# -----------------------------------------------------------------------------


def test(polygon, expected: bool) -> None:
    result = is_convex(polygon)
    if result != expected:
        print(f'Expected: {expected}, got: {result}')
        plot_polygon(polygon, result)
    else:
        print('Test passed')


convex_hexagon = np.array([[0, 0], [1, 0], [2, 1], [1, 2], [0, 2], [-1, 1]])
test(convex_hexagon, True)
concave_hexagon = np.array([[0, 0], [1, 0], [2, 1], [1, 2], [0, 2], [-1, 1], [0, 1]])
test(concave_hexagon, False)