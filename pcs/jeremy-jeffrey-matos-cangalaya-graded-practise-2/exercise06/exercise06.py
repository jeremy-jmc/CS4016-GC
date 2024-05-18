"""
Implement the Jarvis march and the Graham scan, with and without interior points elimination.

TODO: Akl-Toussaint heuristic
https://cses.fi/problemset/task/2195
https://medium.com/@harshitsikchi/convex-hulls-explained-baab662c4e94
https://www.geeksforgeeks.org/convex-hull-using-jarvis-algorithm-or-wrapping/
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

random.seed(123)

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------


def random_point(start: int, end: int) -> tuple:
    """Generate a random point given a range"""
    x = random.randint(start, end) + random.uniform(-end, end)
    y = random.randint(start, end) + random.uniform(-end, end)
    return np.array([x, y])


def generate_points(n_points: int = 50, start: int = -50, end: int = 50) -> list:
    """Generate a list of random points given a range"""
    # print(f'Generated {len(set(point_list))} points')

    # plt.figure(figsize=(5, 5))
    # for p in point_list:
    #     plt.plot(p[0], p[1], 'o', color='black', markersize=3)
    # plt.show()
    return np.array([random_point(start, end) for _ in range(n_points)])


def measure_runtime(algorithm, points) -> float:
    start_time = time.time()
    algorithm(points)
    end_time = time.time()
    return end_time - start_time


def plot_convex_hull(point_list: list, c_hull: list, bbox: list = [], triangle_vectors: list = []) -> None:
    """Visualize the convex hull of a set of points"""

    # plot points
    plt.figure(figsize=(5, 5))
    for p in tqdm(point_list, desc='Plotting points', total=len(point_list)):
        plt.plot(p[0], p[1], 'o', color='black', markersize=5, alpha=0.5)

    # plot convex hull
    for i, p in tqdm(enumerate(c_hull), total=len(c_hull), desc='Plotting convex hull'):
        plt.plot(p[0], p[1], 'o', color='blue', markersize=5)
        plt.plot([p[0], c_hull[(i + 1) % len(c_hull)][0]],
                 [p[1], c_hull[(i + 1) % len(c_hull)][1]], color='green', linestyle='--')
        plt.text(p[0], p[1], f'  {i}', fontsize=12, color='black', ha='left')

    # plot bounding box
    if bbox:
        x1, y1, x2, y2 = bbox
        plt.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1],
                 color='red', linestyle='-', linewidth=1, alpha=0.5)

    # plot triangle vectors for Akl-Toussaint heuristic and interior point elimination result
    if triangle_vectors:
        for i, pair in enumerate(triangle_vectors):
            from_, to_ = pair
            plt.plot(*from_, 'o', color='blue', markersize=10)
            plt.plot(*to_, 'o', color='blue', markersize=10)
            plt.plot([from_[0], to_[0]], [from_[1], to_[1]],
                     color='purple', linestyle='-', linewidth=2)

        point_elimination = interior_point_elimination(point_list)
        for p in point_elimination:
            plt.plot(p[0], p[1], 'o', color='orange',
                     markersize=5, label='Interior point')

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


def sign_of_cross_product(a: np.ndarray, b: np.ndarray) -> float:
    """Calculate the cross product between two vectors a and b centered at the origin"""
    j = a[0] * b[1]
    k = a[1] * b[0]
    if j > k:
        return LEFT
    elif j < k:
        return RIGHT
    return COLLINEAR


def orientation(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> int:
    """Check the orientation of 3 points a, b, c 
    calculating the cross product between vectors ab and cb

    Returns:
        int: 1 if counterclockwise, -1 if clockwise, 0 if collinear
    """
    ab = (a[0] - b[0], a[1] - b[1])
    cb = (c[0] - b[0], c[1] - b[1])
    return sign_of_cross_product(ab, cb)


def get_bbox_triangles(point_list: list) -> tuple:
    triangle_vectors = [
        # max_y-min_x min_x-max_y
        (max(point_list, key=lambda p: (p[1], -p[0])),
         min(point_list, key=lambda p: (p[0], -p[1]))),
        # min_x-min_y min_y-min_x
        (min(point_list, key=lambda p: (p[0], p[1])),
         min(point_list, key=lambda p: (p[1], p[0]))),
        # min_y-max_x max_x-min_y
        (min(point_list, key=lambda p: (p[1], -p[0])),
         max(point_list, key=lambda p: (p[0], -p[1]))),
        # max_x-max_y max_y-max_x
        (max(point_list, key=lambda p: (p[0], p[1])),
         max(point_list, key=lambda p: (p[1], p[0]))),
    ]   # complexity: O(8*n)

    # x1, y1, x2, y2. complexity: O(4*n)
    bbox = [min(point_list, key=lambda p: p[0])[0], min(point_list, key=lambda p: p[1])[1],
            max(point_list, key=lambda p: p[0])[0], max(point_list, key=lambda p: p[1])[1]]

    return bbox, triangle_vectors


# TODO: vectorize
def interior_point_elimination(point_list: np.ndarray) -> list:
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

    def slope_wrt_pivot(idx: np.ndarray) -> np.ndarray:
        # Calcula las diferencias en y y x
        delta_y = point_list[idx][:, 1] - pivot[1]
        delta_x = point_list[idx][:, 0] - pivot[0]

        slopes = np.zeros(delta_y.shape)
        mask_zero = delta_x == 0
        slopes[mask_zero] = np.inf
        slopes[~mask_zero] = np.divide(
            delta_y[~mask_zero], delta_x[~mask_zero])

        return slopes  # np.divide(delta_y, delta_x)

    print('sorting')
    # sort the points based on the polar angle with respect to the pivot, else by distance to pivot
    indices = np.array(range(len(point_list)))
    predicate = slope_wrt_pivot(indices)
    order = np.argsort(predicate)
    point_list = point_list[order]  # [point_list[i] for i in order]

    print('graham scan')
    stack = deque()
    stack.append(pivot)

    for p in point_list:
        while len(stack) > 1 and \
                orientation(stack[-2], stack[-1], p) != RIGHT:
            stack.pop()
        stack.append(p)

    return stack


def jarvis_march(point_list: list) -> list:
    pass


"""
n = int(5*1e6)
print('input started')
point_list = generate_points(n, -n, n)  # //8 //8
bbox, triangle_vectors = get_bbox_triangles(point_list)
print('input done')
# TODO: cProfile tree
cProfile.run('graham_scan_convex_hull = graham_scan(point_list, False)')    # , 'restats'
# runtime, 
# print('runtime:', runtime)
# plot_convex_hull(point_list, graham_scan_convex_hull, bbox, triangle_vectors)
"""

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

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def generate_points_circle(n: int) -> np.ndarray:
    """Generate points in a circle"""
    radius = n // 2
    r = np.sqrt(np.random.rand(n)) * radius
    theta = np.random.rand(n) * 2 * np.pi
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return np.column_stack((x, y))


def generate_points_circle_border(n: int) -> np.ndarray:
    """Generate points in a circle border"""
    theta = np.random.rand(n) * 2 * np.pi
    x = np.cos(theta) * n
    y = np.sin(theta) * n
    return np.column_stack((x, y))


def generate_points_rectangle(n: int) -> np.ndarray:
    """Generate points in a rectangle"""
    width = n // 2
    height = n // 8
    x = np.random.rand(n) * width
    y = np.random.rand(n) * height
    return np.column_stack((x, y))


def generate_points_rectangle_border(n, width=1.0, height=1.0) -> np.ndarray:
    """Generate points in rectangle border"""
    sides = np.random.randint(0, 4, n)
    x = np.empty(n)
    y = np.empty(n)

    x[sides == 0] = np.random.rand(np.sum(sides == 0)) * width
    y[sides == 0] = 0

    x[sides == 1] = np.random.rand(np.sum(sides == 1)) * width
    y[sides == 1] = height

    x[sides == 2] = 0
    y[sides == 2] = np.random.rand(np.sum(sides == 2)) * height

    x[sides == 3] = width
    y[sides == 3] = np.random.rand(np.sum(sides == 3)) * height

    return np.column_stack((x, y))


def generate_points_parabola_border(n, a=1, b=0, c=0) -> np.ndarray:
    x = np.random.rand(n) * 10 - 5
    y = a * x**2 + b * x + c
    return np.column_stack((x, y))


def benchmark(algorithms: list, sizes: list) -> pd.DataFrame:
    distributions = {
        'Circle': generate_points_circle,
        'Circle Border': generate_points_circle_border,
        'Rectangle': generate_points_rectangle,
        'Rectangle Border': generate_points_rectangle_border,
        # 'Parabola': ,
        'Parabola Border': generate_points_parabola_border
    }

    results = []
    for size in sizes:
        for name, generator in distributions.items():
            points = generator(int(size))
            bbox, triangle_vector = get_bbox_triangles(points)
            plot_convex_hull(points, [], [], triangle_vector)
            # for algorithm_name, algorithm in algorithms.items():
            #     runtime = measure_runtime(algorithm, points)
            #     results.append({
            #         'Algorithm': algorithm_name,
            #         'Distribution': name,
            #         'Points': size,
            #         'Runtime': runtime
            #     })

    df = pd.DataFrame(results)
    return df


algorithms = [graham_scan]  # , jarvis_march
point_number = [1e3]   # , 1e4, 1e5, 1e6, 2*1e6, 5*1e6

benchmark(algorithms, point_number)