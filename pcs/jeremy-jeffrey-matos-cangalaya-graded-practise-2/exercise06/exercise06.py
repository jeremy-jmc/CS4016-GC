"""
Implement the Jarvis march and the Graham scan, with and without interior points elimination.

TODO: Akl-Toussaint heuristic
https://cses.fi/problemset/task/2195
https://medium.com/@harshitsikchi/convex-hulls-explained-baab662c4e94
https://www.geeksforgeeks.org/convex-hull-using-jarvis-algorithm-or-wrapping/
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import time
import gc
from tqdm import tqdm
from collections import deque
from IPython.display import display
from functools import cmp_to_key
import cProfile
import time
import os
import cProfile

os.makedirs('img', exist_ok=True)

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


def measure_runtime(algorithm, points, point_elimination) -> float:
    start_time = time.time()
    _ = algorithm(points, point_elimination)
    end_time = time.time()
    return end_time - start_time


def plot_convex_hull(point_list: list, c_hull: list, bbox: list = [], triangle_vectors: list = []) -> None:
    """Visualize the convex hull of a set of points"""

    n = len(point_list)
    # plot points
    fig = plt.figure(figsize=(10, 10))
    for p in tqdm(point_list, desc='Plotting points', total=n):
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
    if n < 10000:
        fig.savefig(f'img/convex_hull_{n}.png')
    plt.show()


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
    # TODO: linearize
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


def get_triangle_vectors(point_list: list) -> tuple:
    max_y_min_x = min_x_max_y = min_x_min_y = min_y_min_x = point_list[0]
    min_y_max_x = max_x_min_y = max_x_max_y = max_y_max_x = point_list[0]

    for p in point_list:
        if (p[1], -p[0]) > (max_y_min_x[1], -max_y_min_x[0]):
            max_y_min_x = p
        if (p[0], -p[1]) < (min_x_max_y[0], -min_x_max_y[1]):
            min_x_max_y = p
        if (p[0], p[1]) < (min_x_min_y[0], min_x_min_y[1]):
            min_x_min_y = p
        if (p[1], p[0]) < (min_y_min_x[1], min_y_min_x[0]):
            min_y_min_x = p
        if (p[1], -p[0]) < (min_y_max_x[1], -min_y_max_x[0]):
            min_y_max_x = p
        if (p[0], -p[1]) > (max_x_min_y[0], -max_x_min_y[1]):
            max_x_min_y = p
        if (p[0], p[1]) > (max_x_max_y[0], max_x_max_y[1]):
            max_x_max_y = p
        if (p[1], p[0]) > (max_y_max_x[1], max_y_max_x[0]):
            max_y_max_x = p

    triangle_vectors = [
        (max_y_min_x, min_x_max_y),
        (min_x_min_y, min_y_min_x),
        (min_y_max_x, max_x_min_y),
        (max_x_max_y, max_y_max_x),
    ]

    return triangle_vectors


def orientation_vectorized(a: np.ndarray, b: np.ndarray, points: np.ndarray) -> np.ndarray:
    ab = np.array([a - b])
    cb = points - b
    cross_product = ab[:, 0] * cb[:, 1] - ab[:, 1] * cb[:, 0]
    
    result = np.full(points.shape[0], COLLINEAR, dtype=int)
    result[cross_product > 0] = LEFT
    result[cross_product < 0] = RIGHT
    
    return result


def points_outside_convex_quad(points: np.ndarray, convex_quad: list) -> np.ndarray:
    # print(convex_quad)
    outside = np.full(points.shape[0], False, dtype=bool)
    for vector in convex_quad:
        # print('\t', vector)
        axis, direction = vector
        if np.array_equal(axis, direction):
            continue
        orientation_result = orientation_vectorized(direction, axis, points)
        # it is sufficient that a point is collinear or to the right of a vector 
        # for it not to belong to the quadrilateral.
        # print('\t', orientation_result)
        outside |= (orientation_result != LEFT)
        # print(outside)
    
    return outside


def interior_point_elimination(point_list: np.ndarray) -> np.ndarray:
    triangle_vectors = get_triangle_vectors(point_list)
    point_outside = points_outside_convex_quad(point_list, triangle_vectors)
    # print(f'Eliminated {np.sum((point_outside == False))} points')
    return point_list[point_outside]


# -----------------------------------------------------------------------------
# Convex Hull algorithms
# -----------------------------------------------------------------------------


def graham_scan(point_list: list, point_elimination: bool = False) -> list:
    """Graham's scan algorithm to find the convex hull of a set of points

    Returns:
        list: list of points that form the convex hull
    """
    if point_elimination:
        # print(f'\tReducing {len(point_list)} points to ', end='')
        point_list = interior_point_elimination(point_list)
        # print(f'{len(point_list)} points')

    # print('finding pivot')
    pivot = min(point_list, key=lambda p: (p[0], p[1]))

    def slope_wrt_pivot(idx: np.ndarray) -> np.ndarray:
        # Calcula las diferencias en y y x
        delta_y = point_list[idx][:, 1] - pivot[1]
        delta_x = point_list[idx][:, 0] - pivot[0]

        slopes = np.zeros(delta_y.shape)
        mask_zero = delta_x == 0
        slopes[mask_zero] = np.inf
        slopes[~mask_zero] = np.divide(delta_y[~mask_zero], 
                                       delta_x[~mask_zero])

        return slopes  # np.divide(delta_y, delta_x)

    # print('sorting')

    # sort the points based on the polar angle with respect to the pivot, else by distance to pivot
    indices = np.array(range(len(point_list)))
    predicate = slope_wrt_pivot(indices)
    order = np.argsort(predicate)
    point_list = point_list[order]  # [point_list[i] for i in order]

    # print('graham scan')
    stack = deque()
    stack.append(pivot)

    for p in point_list:
        while len(stack) > 1 and \
                orientation(stack[-2], stack[-1], p) != RIGHT:
            stack.pop()
        stack.append(p)

    return stack


def jarvis_march(point_list: list, point_elimination: bool = False) -> list:
    """Jarvis march algorithm to find the convex hull of a set of points"""

    if point_elimination:
        point_list = interior_point_elimination(point_list)
    
    n = len(point_list)
    pivot_index = min(range(n), key=lambda i: (point_list[i][0], point_list[i][1]))
    hull = deque()

    while True:
        hull.append(point_list[pivot_index])
        q = (pivot_index - 1) % n
        # print('\t', point_list[pivot_index])
        for other_idx in range(n):
            if orientation(point_list[other_idx], point_list[q], point_list[pivot_index]) == LEFT:
                # print(point_list[pivot_index], point_list[q], point_list[other_idx])
                q = other_idx
        
        pivot_index = q
        if np.array_equal(point_list[pivot_index], hull[0]):
            break
        # plot_convex_hull(point_list, hull)
        # time.sleep(1)
    return hull



# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def generate_points_circle(n: int) -> np.ndarray:
    """Generate points in a circle"""
    radius = 2 * n
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
    width = n
    height = n
    x = np.random.rand(n) * width
    y = np.random.rand(n) * height
    return np.column_stack((x, y))


def generate_points_rectangle_border(n) -> np.ndarray:
    """Generate points in rectangle border"""

    width = n
    height = n
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


def generate_points_above_parabola(n, a=3, b=2, c=1, x_range=(-5, 5), y_max=None) -> np.ndarray:
    """Generate points above a parabola"""
    x = np.random.rand(n) * (x_range[1] - x_range[0]) + x_range[0]
    parabola_y = a * x**2 + b * x + c

    if y_max is None:
        y_max = np.max(parabola_y) + 5
    y = np.random.rand(n) * (y_max - parabola_y) + parabola_y
    return np.column_stack((x, y))


def generate_points_under_parabola(n, a=3, b=2, c=1, x_range=(-5, 5)) -> np.ndarray:
    """Generate points under a parabola"""

    x = np.random.rand(n) * (x_range[1] - x_range[0]) + x_range[0]
    parabola_y = a * x**2 + b * x + c

    y_min = np.min([0, np.min(parabola_y)])
    y = np.random.rand(n) * (parabola_y - y_min) + y_min
    return np.column_stack((x, y))


def generate_points_parabola_border(n, a=3, b=2, c=1) -> np.ndarray:
    """Generate points in parabola border"""
    x = np.random.rand(n) * 10 - 5
    y = a * x**2 + b * x + c
    return np.column_stack((x, y))

# -----------------------------------------------------------------------------
# Benchmark
# -----------------------------------------------------------------------------


def benchmark(algorithms: list, sizes: list) -> pd.DataFrame:
    distributions = {
        'Circle': generate_points_circle,
        'Circle Border': generate_points_circle_border,
        'Rectangle': generate_points_rectangle,
        'Rectangle Border': generate_points_rectangle_border,
        'Parabola': generate_points_above_parabola,
        'Parabola Border': generate_points_parabola_border,
        'Random case': generate_points
    }

    results = []
    for size in sizes:
        for name, generator in tqdm(distributions.items(), desc='Distributions', total=len(distributions)):
            points = generator(int(size))
            for algorithm_name, algorithm in algorithms.items():
                for point_elimination in [False, True]:
                    runtime = measure_runtime(algorithm, points, point_elimination)
                    results.append({
                        'Algorithm': algorithm_name,
                        'Distribution': name,
                        'Points': size,
                        'Point Elimination': point_elimination,
                        'Runtime': runtime
                    })
                gc.collect()
            gc.collect()
        gc.collect()

    df = pd.DataFrame(results)
    return df


# -----------------------------------------------------------------------------
# Profiling
# -----------------------------------------------------------------------------

n = int(1e3)
print('input started')
point_list = generate_points_above_parabola(n, n*4, n*2)
bbox, _ = get_bbox_triangles(point_list)
triangle_vectors = get_triangle_vectors(point_list)
print('input done')

# c_hull = jarvis_march(point_list, False)
cProfile.run('c_hull = jarvis_march(point_list, True)', sort='tottime')

plot_convex_hull(point_list, c_hull, bbox, triangle_vectors)


"""
algorithms = {'graham_scan': graham_scan, 'jarvis_march': jarvis_march}
point_number = [1000, 10000, 100000, 1000000, 2000000, 5000000]

df = benchmark(algorithms, point_number)
df.to_csv('./benchmark.csv')

print(df)
"""