"""
Write a function that computes the area of the intersection of two convex polygons.

https://stackoverflow.com/questions/13101288/intersection-of-two-convex-polygons
https://www.science.smith.edu/~jorourke/books/cgc-toc.html
"""

import matplotlib.pyplot as plt
import numpy as np
from collections import deque


def plot_polygons(polygons: np.ndarray, result: float) -> None:
    """Plot a polygon in 2D space"""

    plt.figure()
    for polygon, color in zip(polygons, ['red', 'green']):
        n = len(polygon)

        for i in range(n):
            plt.plot(*polygon[i], 'o', color='blue')
            plt.plot([polygon[i][0], polygon[(i + 1) % n][0]],
                     [polygon[i][1], polygon[(i + 1) % n][1]], linestyle='-', color=color)
            plt.text(polygon[i][0] + 0.1, polygon[i][1], f'{i + 1}',
                     fontsize=12, color='black', ha='right')

    title = f'Area: {result}'
    plt.title(title)
    plt.show()


LEFT = 1
RIGHT = -1
COLLINEAR = 0


def cross_product_2d(a: np.ndarray, b: np.ndarray) -> float:
    """Return the cross product of two 2D vectors a and b"""
    return a[0] * b[1] - a[1] * b[0]


def sign_of_cross_product(a: np.ndarray, b: np.ndarray) -> float:
    """Return the sign of the cross product between vectors a and b centered at the origin"""
    return np.sign(cross_product_2d(a, b))


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


def area_convex_polygon(polygon: np.ndarray) -> float:
    """Return the area of a convex polygon"""
    n = len(polygon)
    parallelogram_areas = [cross_product_2d(polygon[i] - polygon[0], polygon[(i + 1) % n] - polygon[0])
                           for i in range(1, n)]
    area = abs(sum(parallelogram_areas)) / 2
    return area


def point_intersection(A: np.ndarray, B: np.ndarray,
                       C: np.ndarray, D: np.ndarray) -> tuple:
    """Return the intersection point of two line segments AB and CD"""
    x1, y1 = A
    x2, y2 = B
    x3, y3 = C
    x4, y4 = D

    ABx = x2 - x1
    ABy = y2 - y1
    CDx = x4 - x3
    CDy = y4 - y3

    denominator = CDx * ABy - CDy * ABx
    if denominator == 0:
        return None

    a = CDx * (y3 - y1) - CDy * (x3 - x1)
    b = denominator
    c = ABx * (y3 - y1) - ABy * (x3 - x1)

    alpha = a / b
    beta = c / b

    if 0 <= alpha <= 1 and 0 <= beta <= 1:
        x0 = x1 + alpha * ABx
        y0 = y1 + alpha * ABy
        return (x0, y0)
    else:
        return None


def area_of_intersection_two_convex_polygons(polygon_1: np.ndarray,
                                             polygon_2: np.ndarray) -> float:
    point_1_in_2 = []
    point_2_in_1 = []

    for idx, point in enumerate(polygon_1):
        if inside_polygon(polygon_2, point):
            point_1_in_2.append(idx)

    for idx, point in enumerate(polygon_2):
        if inside_polygon(polygon_1, point):
            point_2_in_1.append(idx)

    new_point_list = deque()
    for point_1 in point_1_in_2:
        for point_2 in point_2_in_1:
            for sides in [(1, 1), (-1, -1), (-1, 1), (1, -1)]:
                pad_1, pad_2 = sides
                new_point = point_intersection(polygon_1[point_1], polygon_1[(point_1 + pad_1) % len(polygon_1)],
                                               polygon_2[point_2], polygon_2[(point_2 + pad_2) % len(polygon_2)])
                if new_point:
                    new_point_list.append(tuple(new_point))

    for idx in point_1_in_2:
        new_point_list.append(tuple(polygon_1[idx]))
    for idx in point_2_in_1:
        new_point_list.append(tuple(polygon_2[idx]))

    new_points = np.array([np.array(point) for point in set(new_point_list)])

    centroid = np.mean(new_points, axis=0)
    new_points = sorted(new_points, key=lambda x: -np.arctan2(x[0] - centroid[0], x[1] - centroid[1]))

    return area_convex_polygon(np.array(new_points))


def test_area_of_intersection_two_convex_polygons(p1, p2, expected: float):
    result = area_of_intersection_two_convex_polygons(p1, p2)
    if np.isclose(result, expected):
        print('Test passed')
    else:
        print(f'Error: {result} != {expected}')
        plot_polygons([polygon_1, polygon_2], result)


polygon_1 = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
polygon_2 = np.array([[0.5, 0.5], [1.5, 0.5], [1.5, 1.5], [0.5, 1.5]])
area = area_of_intersection_two_convex_polygons(polygon_1, polygon_2)
# plot_polygons([polygon_1, polygon_2], area)
test_area_of_intersection_two_convex_polygons(polygon_1, polygon_2, 0.25)

hexagon = np.array([[0, 0], [1, 0], [1.5, 0.5], [1, 1], [0, 1], [-0.5, 0.5]])
nonagon = np.array([[1.0, 0.0], [1.5, 0.5], [2, 1], [1.5, 1.5], [0.5, 1.5], [0, 1], [0, 0.5], [0.5, 0]])
area = area_of_intersection_two_convex_polygons(hexagon, nonagon)
# plot_polygons([hexagon, nonagon], area)
test_area_of_intersection_two_convex_polygons(hexagon, nonagon, 1.125)
