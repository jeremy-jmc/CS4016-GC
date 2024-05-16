"""
Implement the Jarvis march and the Graham scan, with and without interior points elimination.

TODO: Akl-Toussaint heuristic
https://cses.fi/problemset/task/2195
"""

from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import time
import gc

def random_point(start: int = 1, end: int = 3) -> np.ndarray:
    """Generate a random point given a range"""
    return np.array([random.randint(start, end) + random.uniform(-end, end),
                     random.randint(start, end) + random.uniform(-end, end)])


def generate_points(n_points: int = 50, start: int = 1, end: int = 20) -> list:
    """Generate a list of random points given a range"""
    point_list = []
    while len(point_list) < n_points:
        new_point = random_point(start, end)
        # if not any((new_point == p).all() for p in point_list): 
        point_list.append(new_point)

    # print(f'Generated {len(set(point_list))} points')

    # plt.figure(figsize=(5, 5))
    # for p in point_list:
    #     plt.plot(p[0], p[1], 'o', color='black', markersize=3)
    # plt.show()
    return point_list


def measure_runtime(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        runtime = end_time - start_time
        # print(f"Runtime of {func.__name__}: {runtime} seconds")
        return runtime, result
    return wrapper


def plot_convex_hull(point_list: list, convex_hull: list, bbox: list = [], convex_quad: list = []) -> None:
    plt.figure(figsize=(5, 5))
    for p in point_list:
        plt.plot(p[0], p[1], 'o', color='black', markersize=5)

    for i, p in enumerate(convex_hull):
        plt.plot(p[0], p[1], 'o', color='blue', markersize=5)
        plt.plot([p[0], convex_hull[(i + 1) % len(convex_hull)][0]], 
                [p[1], convex_hull[(i + 1) % len(convex_hull)][1]], color='green', linestyle='--')
    
    if bbox:
        x1, y1, x2, y2 = bbox
        plt.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], color='red', linestyle='-', linewidth=1)

    if convex_quad:
        for i, current in enumerate(convex_quad):
            next_ = convex_quad[(i + 1) % len(convex_quad)]
            plt.plot([current[0], next_[0]], 
                     [current[1], next_[1]], color='purple', linestyle='--')
            
        for p in point_list:
            if point_inside_polygon(p, convex_quad):
                plt.plot(p[0], p[1], 'o', color='orange', markersize=5, label='Interior point')
    # plt.xticks([])
    # plt.yticks([])
    plt.show()


# -----------------------------------------------------------------------------
# Algorithm utilities
# -----------------------------------------------------------------------------

def orientation(first: np.ndarray, second: np.ndarray, third: np.ndarray) -> int:
    """Determine the orientation of the triplet (first, second, third)

    Logic:
        Slope of first-second
            first.x - second.x / first.y - second.y
        Slope of second-third
            second.x - third.x / second.y - third.y

        Comparing
            (first.x - second.x) * (second.y - third.y) - (first.y - second.y) * (second.x - third.x)

    -1: clockwise
    0: collinear
    1: counterclockwise

    Source:
        https://www.geeksforgeeks.org/orientation-3-ordered-points/
    """
    val = (first[0] - second[0]) * (second[1] - third[1]) - (first[1] - second[1]) * (second[0] - third[0])
    if val == 0:
        return 0
    return 1 if val > 0 else -1


def point_inside_polygon(point: np.ndarray, polygon: list) -> bool:
    # TODO: replace with the exercise 4
    n = len(polygon)
    z_components = [
        np.sign(np.cross(polygon[(i + 1) % n] - polygon[i], point - polygon[i]))
        for i in range(n)
    ]
    result = all(z == z_components[0] for z in z_components)
    return result


def get_bbox_convexquad(point_list: list) -> tuple:
    convex_quadrilateral = [
        # juego de minimos con maximos para reducir el area del bbox
        min(point_list, key=lambda p: (p[0], -p[1])), max(point_list, key=lambda p: (p[0], -p[1])),
        min(point_list, key=lambda p: (p[1], p[0])), max(point_list, key=lambda p: (p[1], p[0]))
    ]   # complexity: O(4*n)
    point_min_x, point_max_x, point_min_y, point_max_y = convex_quadrilateral

    bbox = [point_min_x[0], point_min_y[1],
            point_max_x[0], point_max_y[1]]   # x1, y1, x2, y2
    
    # TODO: check correctness: How can I draw the quadrilateral with the correct order?
    convex_quadrilateral = sorted(convex_quadrilateral, key=lambda p: (np.arctan2(p[1], p[0]) * 180 / np.pi))
    return bbox, convex_quadrilateral


def interior_point_elimination(point_list: list) -> list:
    _, convex_quad = get_bbox_convexquad(point_list)
    return [p for p in point_list if not point_inside_polygon(p, convex_quad)]

# -----------------------------------------------------------------------------
# Convex Hull algorithms
# -----------------------------------------------------------------------------

@measure_runtime
def graham_scan(point_list: list, point_elimination: bool = False) -> list:
    """Graham's scan algorithm to find the convex hull of a set of points

    Returns:
        list: list of points that form the convex hull
    """
    if point_elimination:
        print(f'\tReducing {len(point_list)} points to ', end='')
        point_list = interior_point_elimination(point_list)
        print(f'{len(point_list)} points')

    point_list = sorted(point_list, key=lambda p: (p[1], p[0]))
    pivot = point_list[0]#.pop(0)

    # sort the points based on the polar angle
    comparer = lambda p: (np.arctan2(p[1] - pivot[1], p[0] - pivot[0]) * 180 / np.pi,
                          np.sqrt((p[0] - pivot[0]) ** 2 + (p[1] - pivot[1]) ** 2))
    point_list.sort(key=comparer)

    stack = [pivot]
    for p in point_list:
        while len(stack) > 1 and \
            orientation(stack[-2], stack[-1], p) != 1:  #  == -1
            stack.pop()
        stack.append(p)

    return stack


@measure_runtime
def jarvis_march(point_list: list) -> list:
    pass

# TODO: metrics to pandas DataFrame
for n in [1e3, 1e4, 1e5, 1e6, 2*1e6, 5*1e6]:
    point_list = generate_points(n, -n, n)
    runtime, graham_scan_convex_hull = graham_scan(point_list, True)
    print(f'Graham scan runtime for {int(n)} points: {runtime} seconds')
    # plot_convex_hull(point_list, graham_scan_convex_hull)
    # runtime, jarvis_march_convex_hull = jarvis_march(point_list)
    # print(f'Jarvis march runtime for {int(n)} points: {runtime} seconds')
    gc.collect()


# point_list = generate_points(100, -10, 10)
# bbox, convex_quadrilateral = get_bbox_convexquad(point_list)

# runtime, graham_scan_convex_hull = graham_scan(point_list, True)
# plot_convex_hull(point_list, graham_scan_convex_hull, [], convex_quadrilateral)

# jarvis_march_convex_hull = jarvis_march(point_list)
