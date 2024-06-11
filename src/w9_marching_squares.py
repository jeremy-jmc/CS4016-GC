import numpy as np
from typing import Callable
import matplotlib.pyplot as plt


MAX_DEPTH = 10
N_SAMPLING = 100000
MARCHING_SQUARES_RESULT = []

def generate_random_points(n: int, x_range: tuple, y_range: tuple) -> np.ndarray:
    # p_sampling = []
    # for _ in range(n):
    #     x = np.random.uniform(*x_range)
    #     y = np.random.uniform(*y_range)
    #     p_sampling.append((x, y))
    # return np.array(p_sampling)
    x_points = np.random.uniform(x_range[0], x_range[1], n)
    y_points = np.random.uniform(y_range[0], y_range[1], n)
    return np.column_stack((x_points, y_points))


def add_line(f: Callable, bbox: tuple):
    x_min, y_min, x_max, y_max = bbox
    x_mid = (x_max + x_min) / 2
    y_mid = (y_max + y_min) / 2

    bitstring = f'{int(f(x_min, y_max) > 0)}{int(f(x_max, y_max) > 0)}{int(f(x_max, y_min) > 0)}{int(f(x_min, y_min) > 0)}'
    case = int(bitstring, 2)
    # print(f'{bitstring} -> {case}')
    
    new_line = None
    if case == 0 or case == 15:
        return
    elif case == 1 or case == 14:
        new_line = ([x_min, y_mid], [x_mid, y_min])
    elif case == 2 or case == 13:
        new_line = ([x_mid, y_min], [x_max, y_mid])
    elif case == 3 or case == 12:
        new_line = ([x_min, y_mid], [x_max, y_mid])
    elif case == 4 or case == 11:
        new_line = ([x_max, y_mid], [x_mid, y_max])
    elif case == 5:
        # TODO: solving ambiguity
        new_line = [([x_min, y_mid], [x_mid, y_max]), 
                    ([x_mid, y_min], [x_max, y_mid])]
    elif case == 6 or case == 9:
        new_line = ([x_mid, y_min], [x_mid, y_max])
    elif case == 7 or case == 8:
        new_line = ([x_min, y_mid], [x_mid, y_max])
    elif case == 10:
        # TODO: solving ambiguity
        new_line = [([x_min, y_mid], [x_mid, y_min]), 
                    ([x_mid, y_max], [x_max, y_mid])]

    if isinstance(new_line, list):
        MARCHING_SQUARES_RESULT.extend(new_line)
    if isinstance(new_line, tuple):
        MARCHING_SQUARES_RESULT.append(new_line)


def marching_squares(f: Callable, bbox: tuple, depth: int = 0, precision: float = 0.05):
    if depth == 0:
        MARCHING_SQUARES_RESULT.clear()
    
    x_min, y_min, x_max, y_max = bbox
    p_sampling = generate_random_points(N_SAMPLING, (x_min, x_max), (y_min, y_max))
    eval_points = f(p_sampling[:, 0], p_sampling[:, 1]) # np.array([f(*point) for point in p_sampling])
    
    # * contar (+) (-) (0)
    n_positives = len(eval_points[eval_points > 0])       # outside: todos -> afuera
    n_negatives = len(eval_points[eval_points < 0])       # inside: todos -> adentro
    n_zeros = len(eval_points[eval_points == 0])          # border

    if n_zeros == 0:
        if n_negatives > 0 and n_positives == 0:
            # cuadrado esta adentro
            return
        if n_positives > 0 and n_negatives == 0:
            # cuadrado esta afuera
            return
    
    # print(' ' * depth * 2, bbox, n_positives, n_negatives, n_zeros, x_max - x_min, y_max - y_min)
    
    if x_max - x_min < precision and y_max - y_min < precision:
        add_line(f, bbox)
        return
    
    # do subdivision
    x_mid = (x_max + x_min) / 2
    y_mid = (y_max + y_min) / 2

    # upper left
    marching_squares(f, (x_min, y_mid, x_mid, y_max), depth + 1)
    # upper right
    marching_squares(f, (x_mid, y_mid, x_max, y_max), depth + 1)
    # lower left
    marching_squares(f, (x_min, y_min, x_mid, y_mid), depth + 1)
    # lower right
    marching_squares(f, (x_mid, y_min, x_max, y_mid), depth + 1)


def draw_curve(f: Callable, output_file: str = './image.eps', 
              min_x: int = -1, min_y: int = -1, max_x: int = 1, max_y: int = 1, 
              precision: float =  0.05):
    global MARCHING_SQUARES_RESULT
    MARCHING_SQUARES_RESULT = []

    BBOX = (min_x, min_y, max_x, max_y)
    marching_squares(f, BBOX, precision=precision)

    # Plot and save
    x = np.linspace(min_x, max_x, 100)
    y = np.linspace(min_y, max_y, 100)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    fig = plt.figure(figsize=(10, 10))
    plt.contour(X, Y, Z, levels=[0], colors='black', linestyles='dashed')
    for line in MARCHING_SQUARES_RESULT:
        first, second = zip(*line)
        plt.plot(first, second, 'r')
        # plt.scatter(first, second, color='r', s=10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(min_x - 0.1, max_x + 0.1)
    plt.ylim(min_y - 0.1, max_y + 0.1)  # Fixed typo: min_y instead of min_y
    fig.savefig(output_file, format='eps')
    plt.close(fig)  # Close the figure to avoid displaying an empty canvas

# -----------------------------------------------------------------------------
# * Main    
# -----------------------------------------------------------------------------
RADIUS = 3

def f_circle(x: float, y: float, radius: int = RADIUS) -> float:
    return x**2 + y**2 - radius**2

def f_example(x, y):
    return 0.004 + 0.110 * x - 0.177 * y - 0.174 * x**2 + 0.224 * x * y - 0.303 * y**2 - 0.168 * x**3 + 0.327 * x**2 * y - 0.087 * x * y**2 - 0.013 * y**3 + 0.235 * x**4 - 0.667 * x**3 * y + 0.745 * x**2 * y**2 - 0.029 * x * y**3 + 0.072 * y**4

f = f_example

X_MIN, Y_MIN, X_MAX, Y_MAX = -RADIUS, -RADIUS, RADIUS, RADIUS
BBOX = (X_MIN, Y_MIN, X_MAX, Y_MAX)

draw_curve(f, './image.eps', X_MIN, Y_MIN, X_MAX, Y_MAX, 0.1)

# # -----------------------------------------------------------------------------
# # * Plotting
# # -----------------------------------------------------------------------------
# marching_squares(f, BBOX)
# print(MARCHING_SQUARES_RESULT)

# x = np.linspace(X_MIN, X_MAX, 100)
# y = np.linspace(Y_MIN, Y_MAX, 100)
# X, Y = np.meshgrid(x, y)
# Z = f(X, Y)

# fig = plt.figure(figsize=(10, 10))
# plt.contour(X, Y, Z, levels=[0], colors='black', linestyles='dashed')
# for line in MARCHING_SQUARES_RESULT:
#     first, second = zip(*line)
#     plt.plot(first, second, 'r')
#     # plt.scatter(first, second, color='r', s=10)
# plt.xlabel('x')
# plt.ylabel('y')
# plt.xlim(X_MIN - 0.1, X_MAX + 0.1)
# plt.ylim(Y_MIN - 0.1, Y_MAX + 0.1)
# fig.savefig('marching_squares.eps', format='eps')
# plt.show()