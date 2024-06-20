"""
10. (7 points) Marching squares.

marching_squares(
    json_object_describing_curve,
    output_filename,
    x_min, y_min, x_max, y_max,
    precision)
"""

import numpy as np
from typing import Callable
import matplotlib.pyplot as plt

N_SAMPLING = 100000
MARCHING_SQUARES_RESULT = []


def generate_random_points(n: int, x_range: tuple, y_range: tuple) -> np.ndarray:
    x_points = np.random.uniform(x_range[0], x_range[1], n)
    y_points = np.random.uniform(y_range[0], y_range[1], n)
    return np.column_stack((x_points, y_points))


def add_line(f: Callable | list, bbox: tuple):
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



def eval_obj(json_obj: dict, x: int, y: int):
    if json_obj['op'] == 'union':
        n_zeros, n_pos, n_neg = 0, 0, 0

        for child in json_obj['childs']:
            result_eval = eval_obj(child, x, y)
            if result_eval == 0:
                n_zeros = n_zeros + 1
            elif result_eval > 0:
                n_pos = n_pos + 1
            else:
                n_neg = n_neg + 1
        # dentro
        if n_neg > 0: 
            return -1
        # borde
        if n_zeros > 0:
            return 0
        # fuera
        return 1
    elif json_obj['op'] == '':
        # cuando es 1 funcion
        return eval(json_obj['function'], {'x': x, 'y': y})


def marching_squares(json_object_describing_curve: dict,
                     output_filename: str,
                     x_min: float, y_min: float, x_max: float, y_max: float,
                     precision: float, depth: int = 0):
    if depth == 0:
        MARCHING_SQUARES_RESULT.clear()
    
    p_sampling = generate_random_points(N_SAMPLING, (x_min, x_max), (y_min, y_max))


example_json = {
    'op': 'union',
    'function': '',
    'childs': [
        {'op': '', 'function': '(x-2)^2 + (y-3)^2 - 4^2', 'childs': []},
        {'op': '', 'function': '(x+1)^2 + (y-3)^2 - 4^2', 'childs': []},
    ],
}


if __name__ == '__main__':
    marching_squares(
        example_json, './example-marching-squares-1.eps', -5, -5, 6, 6, 0.1
    )

    marching_squares(
        # one circle of radius 1 centered at (2, 2)
        {'op': '', 'function': '(x-2)^2+(y-2)^2-1', 'childs': []},
        './example-marching-squares-2.eps',
        -5,
        -5,
        6,
        6,
        0.1,
    )

    marching_squares(
        {
            'op': 'union',
            'function': '',
            'childs': [
                # circles of radius 1 centered at (2, 2) and (4, 2)
                {'op': '', 'function': '(x-2)^2+(y-2)^2-1', 'childs': []},
                {'op': '', 'function': '(x-4)^2+(y-2)^2-1', 'childs': []},
            ],
        },
        './example-marching-squares-3.eps',
        -5,
        -5,
        6,
        6,
        0.1,
    )
