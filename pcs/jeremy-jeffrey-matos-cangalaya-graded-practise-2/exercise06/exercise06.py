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
    return np.array([random.randint(start, end), # + random.uniform(-end, end), 
                     random.randint(start, end)# + random.uniform(-end, end)
                     ])


def generate_points(n_points: int = 50, start: int = 1, end: int = 20) -> list:
    """Generate a list of random points given a range"""
    # print(f'Generated {len(set(point_list))} points')

    # plt.figure(figsize=(5, 5))
    # for p in point_list:
    #     plt.plot(p[0], p[1], 'o', color='black', markersize=3)
    # plt.show()
    return np.array([random_point(start, end) for _ in range(n_points)])


def measure_runtime(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        runtime = end_time - start_time
        # print(f"Runtime of {func.__name__}: {runtime} seconds")
        return runtime, result
    return wrapper


def plot_convex_hull(point_list: list, convex_hull: list, bbox: list = [], triangle_vectors: list = []) -> None:
    plt.figure(figsize=(10, 10))
    for p in tqdm(point_list, desc='Plotting points', total=len(point_list)):
        plt.plot(p[0], p[1], 'o', color='black', markersize=5, alpha=0.5)

    for i, p in tqdm(enumerate(convex_hull), total=len(convex_hull), desc='Plotting convex hull'):
        plt.plot(p[0], p[1], 'o', color='blue', markersize=5)
        plt.plot([p[0], convex_hull[(i + 1) % len(convex_hull)][0]], 
                [p[1], convex_hull[(i + 1) % len(convex_hull)][1]], color='green', linestyle='--')
        plt.text(p[0], p[1], f'  {i}', fontsize=12, color='black', ha='left')
    
    if bbox:
        x1, y1, x2, y2 = bbox
        plt.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], color='red', linestyle='-', linewidth=1, alpha=0.5)

    if triangle_vectors:
        print(triangle_vectors)
        for i, pair in enumerate(triangle_vectors):
            from_, to_ = pair
            # plt.plot(*from_, 'o', color='purple', markersize=10)
            # plt.plot(*to_, 'o', color='purple', markersize=10)
            plt.plot([from_[0], to_[0]], [from_[1], to_[1]], color='purple', linestyle='-', linewidth=2)

        point_elimination = interior_point_elimination(point_list)
        for p in point_elimination:
            plt.plot(p[0], p[1], 'o', color='orange', markersize=5, label='Interior point')
    # plt.xticks([])
    # plt.yticks([])
    plt.show()
    plt.savefig(f'convex_hull_{len(point_list)}.png')


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
        return LEFT
    elif j < k:
        return RIGHT
    return COLLINEAR

def orientation(a: np.array, b: np.array, c: np.array) -> int:
    """Check the orientation of 3 points a, b, c 
    calculating the cross product between vectors ab and bc
    
    Returns:
        int: 1 if counterclockwise, -1 if clockwise, 0 if collinear
    """
    s = sign_of_cross_product((a[0] - b[0], a[1] - b[1]), (c[0] - b[0], c[1] - b[1]))
    return s

def get_bbox_triangles(point_list: list) -> tuple:
    triangle_vectors = [
        # max_y-min_x min_x-max_y
        (max(point_list, key=lambda p: (p[1], -p[0])), min(point_list, key=lambda p: (p[0], -p[1]))),
        # min_x-min_y min_y-min_x
        (min(point_list, key=lambda p: (p[0], p[1])), min(point_list, key=lambda p: (p[1], p[0]))),
        # min_y-max_x max_x-min_y
        (min(point_list, key=lambda p: (p[1], -p[0])), max(point_list, key=lambda p: (p[0], -p[1]))),
        # max_x-max_y max_y-max_x
        (max(point_list, key=lambda p: (p[0], p[1])), max(point_list, key=lambda p: (p[1], p[0]))),
    ]   # complexity: O(8*n)

    # x1, y1, x2, y2. complexity: O(4*n)
    bbox = [min(point_list, key=lambda p: p[0])[0], min(point_list, key=lambda p: p[1])[1],
            max(point_list, key=lambda p: p[0])[0], max(point_list, key=lambda p: p[1])[1]]

    return bbox, triangle_vectors


def interior_point_elimination(point_list: list) -> list:
    _, triangle_vectors = get_bbox_triangles(point_list)

    def point_outside_convex_quad(point, convex_quad) -> bool:
        for vector in convex_quad:
            if orientation(vector[1], vector[0], point) != LEFT:
                return True
        return False

    return np.array([p for p in point_list if point_outside_convex_quad(p, triangle_vectors)])
    # return point_list

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
    
    print('finding pivot')
    pivot = min(point_list, key=lambda p: (p[0], p[1]))

    def slope_wrt_pivot(idx):
        # Calcula las diferencias en y y x
        delta_y = point_list[idx][:, 1] - pivot[1]
        delta_x = point_list[idx][:, 0] - pivot[0]
        
        slopes = np.zeros(delta_y.shape)
        mask_zero = delta_x == 0
        slopes[mask_zero] = np.inf
        slopes[~mask_zero] = np.divide(delta_y[~mask_zero], delta_x[~mask_zero])

        return slopes # np.divide(delta_y, delta_x)
    
    print('sorting')
    # sort the points based on the polar angle with respect to the pivot, else by distance to pivot
    indices = np.array(range(len(point_list)))
    predicate = slope_wrt_pivot(indices)
    order = np.argsort(predicate)
    point_list = [point_list[i] for i in order]

    print('graham scan')
    stack = deque()
    stack.append(pivot)
    
    for p in point_list:
        while len(stack) > 1 and \
            orientation(stack[-2], stack[-1], p) != RIGHT:
            stack.pop()
        stack.append(p)
    
    return stack

@measure_runtime
def jarvis_march(point_list: list) -> list:
    pass

# random.seed(123)
n = int(1000)
print('input started')
point_list = generate_points(n, -n//8, n//8)
bbox, triangle_vectors = get_bbox_triangles(point_list)
print('input done')
# TODO: cProfile tree
cProfile.run('runtime, graham_scan_convex_hull = graham_scan(point_list, True)')
print('runtime:', runtime)
plot_convex_hull(point_list, graham_scan_convex_hull, bbox, triangle_vectors)


"""
# TODO: metrics to pandas DataFrame
for n in [1e3, 1e4, 1e5, 1e6, 2*1e6, 5*1e6]:
    n = int(n) 
    print('input started')
    point_list = generate_points(n, -n, n)
    print('input done')
    runtime, graham_scan_convex_hull = graham_scan(point_list, False)
    print(f'Graham scan runtime for {int(n)} points: {runtime:.5f} seconds')
    # plot_convex_hull(point_list, graham_scan_convex_hull)
    # runtime, jarvis_march_convex_hull = jarvis_march(point_list)
    # print(f'Jarvis march runtime for {int(n)} points: {runtime} seconds')
    gc.collect()
"""

# point_list = generate_points(1000000, -10, 10)
# bbox, convex_quadrilateral = get_bbox_triangles(point_list)

# runtime, graham_scan_convex_hull = graham_scan(point_list, True)
# plot_convex_hull(point_list, graham_scan_convex_hull, bbox, [])
# print(runtime)

# jarvis_march_convex_hull = jarvis_march(point_list)
