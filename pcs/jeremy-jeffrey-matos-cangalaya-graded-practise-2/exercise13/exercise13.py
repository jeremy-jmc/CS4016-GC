"""
Implement Douglas-Peucker

INPUT:
    A polyline P in the form of a list of points, where each point is a tuple (x, y)
    A tolerance value ε
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import deque


def distance_point_line(point: np.ndarray, line_origin: np.ndarray,
                        direction: np.ndarray) -> float:
    """Compute the distance from point to line"""
    dir_origin = direction - line_origin
    point_origin = point - line_origin

    dir_origin_3d = np.append(dir_origin, 0)
    point_origin_3d = np.append(point_origin, 0)

    parallelogram_area = np.linalg.norm(
        np.cross(dir_origin_3d, point_origin_3d))
    parallelogram_height = parallelogram_area / np.linalg.norm(dir_origin)

    return parallelogram_height


def plot_polyline(polyline: np.ndarray, simplified: np.ndarray, tolerance: float, slices: np.ndarray):
    plt.figure(figsize=(15, 5))
    x, y = polyline.T
    plt.plot(x, y, 'o-', label='Original')
    for i, (x, y) in enumerate(polyline):
        plt.text(x, y, f'{i}', ha='right', va='bottom')

    if len(simplified) > 0:
        x, y = simplified.T
        plt.plot(x, y, 'o-', label='Simplified')

    for start, max_index, end in slices:
        init_point = polyline[start]
        end_point = polyline[end]
        max_point = polyline[max_index]

        plt.plot([init_point[0], end_point[0]], [
                 init_point[1], end_point[1]], 'k--')
        plt.plot(max_point[0], max_point[1], 'ro', markersize=7.5)
    plt.title('Douglas Peucker')
    plt.legend()
    plt.show()


def douglas_peucker(polyline: np.ndarray, tolerance: float = 1e-10):
    slices = deque()
    distances = [0] * len(polyline)

    def dp_recursive(start: int, end: int) -> list:
        if start >= end:
            return [start]

        max_dist, max_index = 0, start
        for i in range(start + 1, end):
            dist = distance_point_line(polyline[i], polyline[start], polyline[end])
            distances[i] = round(dist, 4)

            if dist > max_dist:
                max_dist = dist
                max_index = i

        if max_dist > tolerance:
            slices.append((start, max_index, end))
            left = dp_recursive(start, max_index)
            right = dp_recursive(max_index, end)
            return left + right
        else:
            return [start, end]

    n = len(polyline)
    simplified = dp_recursive(0, n - 1)
    print(slices)
    print(distances)
    return slices, polyline[simplified]


tolerance = 1.25
polyline = np.array([[1, 1], [3, -2], [5, -2], [7, 1],[9, 3], [11, 2.5], [13, -1], [15, 1.5]])
slices, simplified = douglas_peucker(polyline, tolerance)

plot_polyline(polyline, simplified, tolerance, [])
