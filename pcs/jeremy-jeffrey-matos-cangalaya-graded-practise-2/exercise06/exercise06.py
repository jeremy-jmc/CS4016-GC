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
from tqdm import tqdm
from collections import deque
from functools import cmp_to_key
import cProfile

def random_point(start: int = 1, end: int = 3) -> tuple:
    """Generate a random point given a range"""
    return (random.randint(start, end) + random.uniform(-end, end),
            random.randint(start, end) + random.uniform(-end, end))


def generate_points(n_points: int = 50, start: int = 1, end: int = 20) -> list:
    """Generate a list of random points given a range"""
    # print(f'Generated {len(set(point_list))} points')

    # plt.figure(figsize=(5, 5))
    # for p in point_list:
    #     plt.plot(p[0], p[1], 'o', color='black', markersize=3)
    # plt.show()
    return [random_point(start, end) for _ in range(n_points)]


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

        # for p in point_list:
        #     if point_inside_polygon(p, convex_quad):
        #         plt.plot(p[0], p[1], 'o', color='orange', markersize=5, label='Interior point')
    # plt.xticks([])
    # plt.yticks([])
    plt.show()


# -----------------------------------------------------------------------------
# Algorithm utilities
# -----------------------------------------------------------------------------
LEFT = 1
COLLINEAR = 0
RIGHT = -1

def sign_of_cross_product(a: np.array, b: np.array) -> float:
    j = a[0] * b[1]
    k = a[1] * b[0]
    if j > k:
        return 1
    elif j < k:
        return -1
    return 0

def orientation(a: np.array, b: np.array, c: np.array) -> int:
    """Check the orientation of 3 points a, b, c 
    calculating the cross product between vectors ab and bc
    
    Returns:
        int: 1 if counterclockwise, -1 if clockwise, 0 if collinear
    """
    s = sign_of_cross_product((a[0] - b[0], a[1] - b[1]), (c[0] - b[0], c[1] - b[1]))
    if s > 0:
        return LEFT
    elif s < 0:
        return RIGHT
    return COLLINEAR

def get_bbox_triangles(point_list: list) -> tuple:
    triangle_vectors = [
        # juego de minimos con maximos para reducir el area del bbox
        min(point_list, key=lambda p: (p[0], -p[1])), max(point_list, key=lambda p: (p[0], -p[1])),
        min(point_list, key=lambda p: (p[1], p[0])), max(point_list, key=lambda p: (p[1], p[0]))
    ]   # complexity: O(8*n)

    # x1, y1, x2, y2. complexity: O(4*n)
    bbox = [min(point_list, key=lambda p: p[0])[0], min(point_list, key=lambda p: p[1])[1],
            max(point_list, key=lambda p: p[0])[0], max(point_list, key=lambda p: p[1])[1]]

    return bbox, triangle_vectors


def interior_point_elimination(point_list: list) -> list:
    _, convex_quad = get_bbox_triangles(point_list)
    # return [p for p in point_list if not point_inside_polygon(p, convex_quad)]
    return point_list

# -----------------------------------------------------------------------------
# Convex Hull algorithms
# -----------------------------------------------------------------------------



# @measure_runtime
def graham_scan(point_list: list, point_elimination: bool = False) -> list:
    """Graham's scan algorithm to find the convex hull of a set of points

    Returns:
        list: list of points that form the convex hull
    """
    if point_elimination:
        print(f'\tReducing {len(point_list)} points to ', end='')
        point_list = interior_point_elimination(point_list)
        print(f'{len(point_list)} points')
    
    print('calculando pivot')
    pivot = min(point_list, key=lambda p: (p[1], p[0]))
    
    # dict_distance = {
    #     p: (np.arctan2(p[1] - pivot[1], p[0] - pivot[0]) * 180 / np.pi, 
    #                np.sqrt((p[0] - pivot[0]) ** 2 + (p[1] - pivot[1]) ** 2)) for p in point_list}
    
    def cmp(item1, item2):
        delta_x1 = point_list[item1][0] - pivot[0]
        delta_y1 = point_list[item1][1] - pivot[1]
        delta_x2 = point_list[item2][0] - pivot[0]
        delta_y2 = point_list[item2][1] - pivot[1]
        return delta_y2 * delta_x1 - delta_x2 * delta_y1

    def pendiente1(x):
        return (x[1] - pivot[1]) / (x[0] - pivot[0] + 1e-6)
    
    print('ordenando puntos con respecto a pivot')
    # sort the points based on the polar angle with respect to the pivot, else by distance to pivot
    indices = np.array(range(len(point_list)))
    predicate = pendiente1(indices)
    order = np.argsort(predicate)
    point_list = [point_list[i] for i in order]

    print('graham scan')
    stack = deque()
    stack.append(pivot)
    # i = 0
    for p in point_list:    # tqdm(point_list, total=len(point_list))
        while len(stack) > 1 and \
            orientation(stack[-2], stack[-1], p) != RIGHT:
            stack.pop()
        stack.append(p)
        # print(f'punto: {i} de {len(point_list)}')
        # i = i + 1
    print('final')
    return stack

@measure_runtime
def jarvis_march(point_list: list) -> list:
    pass

n = 5000000
print('input started')
point_list = generate_points(n, -n, n)
print('input done')
# TODO: cProfile tree
cProfile.run('graham_scan(point_list, False)')

"""
# TODO: metrics to pandas DataFrame
for n in [5000000]:   # 1e3, 1e4, 1e5, 1e6, 2*1e6, 
    print('input started')
    point_list = generate_points(n, -n, n)
    print('input done')
    runtime, graham_scan_convex_hull = graham_scan(point_list, False)
    print(f'Graham scan runtime for {int(n)} points: {runtime} seconds')
    # plot_convex_hull(point_list, graham_scan_convex_hull)
    # runtime, jarvis_march_convex_hull = jarvis_march(point_list)
    # print(f'Jarvis march runtime for {int(n)} points: {runtime} seconds')
    gc.collect()
"""

# point_list = generate_points(100, -10, 10)
# bbox, convex_quadrilateral = get_bbox_triangles(point_list)

# runtime, graham_scan_convex_hull = graham_scan(point_list, True)
# plot_convex_hull(point_list, graham_scan_convex_hull, bbox, [])

# jarvis_march_convex_hull = jarvis_march(point_list)
