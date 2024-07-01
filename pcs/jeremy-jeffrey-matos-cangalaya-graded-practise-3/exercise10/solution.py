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

N_SAMPLING = 1000
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
        new_line = [([x_min, y_mid], [x_mid, y_max]), 
                    ([x_mid, y_min], [x_max, y_mid])]
    elif case == 6 or case == 9:
        new_line = ([x_mid, y_min], [x_mid, y_max])
    elif case == 7 or case == 8:
        new_line = ([x_min, y_mid], [x_mid, y_max])
    elif case == 10:
        new_line = [([x_min, y_mid], [x_mid, y_min]), 
                    ([x_mid, y_max], [x_max, y_mid])]

    if isinstance(new_line, list):
        MARCHING_SQUARES_RESULT.extend(new_line)
    if isinstance(new_line, tuple):
        MARCHING_SQUARES_RESULT.append(new_line)


def m_squares(f: Callable | list, bbox: tuple, depth: int = 0, precision: float = 0.025):
    if depth == 0:
        MARCHING_SQUARES_RESULT.clear()
    
    x_min, y_min, x_max, y_max = bbox
    p_sampling = generate_random_points(N_SAMPLING, (x_min, x_max), (y_min, y_max))
    
    eval_points = f(p_sampling[:, 0], p_sampling[:, 1])

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
    m_squares(f, (x_min, y_mid, x_mid, y_max), depth + 1)
    # upper right
    m_squares(f, (x_mid, y_mid, x_max, y_max), depth + 1)
    # lower left
    m_squares(f, (x_min, y_min, x_mid, y_mid), depth + 1)
    # lower right
    m_squares(f, (x_mid, y_min, x_max, y_mid), depth + 1)


def draw_curve(output_filename: str = './image.eps', 
              min_x: int = -1, min_y: int = -1, max_x: int = 1, max_y: int = 1
              ):
    global MARCHING_SQUARES_RESULT
    # Plot and save
    fig = plt.figure(figsize=(10, 10))
    for line in MARCHING_SQUARES_RESULT:
        first, second = zip(*line)
        plt.plot(first, second, 'k-')
        plt.fill(first, second, 'b', alpha=0.5)
        # plt.scatter(first, second, color='r', s=10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(min_x - 0.1, max_x + 0.1)
    plt.ylim(min_y - 0.1, max_y + 0.1)
    fig.savefig(output_filename, format='eps')
    plt.close(fig)  # Close the figure to avoid displaying an empty canvas


def transform_functions_to_lambdas(node):
    if 'function' in node and node['function']:
        node['function'] = eval(f"lambda x, y: {node['function'].replace('^', '**')}")
    if 'childs' in node and node['childs']:
        for child in node['childs']:
            transform_functions_to_lambdas(child)


def eval_obj(json_obj: dict, x: int, y: int) -> np.ndarray:
    if json_obj['op'] == 'union':
        # result_childs = np.array([eval_obj(child, x, y) for child in json_obj['childs']])
        
        result_childs = []
        for child in json_obj['childs']:
            result_childs.append(eval_obj(child, x, y))
        
        n_neg = np.sum(np.array(result_childs) < 0, axis=0)
        n_zeros = np.sum(np.array(result_childs) == 0, axis=0)
        result = np.where(n_neg > 0, -1, np.where(n_zeros > 0, 0, 1))

        return result

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
    elif json_obj['op'] == 'intersection':
        # TODO: implementar
        pass
    elif json_obj['op'] == 'difference':
        # TODO: implementar
        pass
    elif json_obj['op'] == '':
        # cuando es 1 funcion
        return json_obj['function'](x=x, y=y)
        # return eval(json_obj['function'], {'x': x, 'y': y})


def marching_squares(json_object_describing_curve: dict,
                     output_filename: str,
                     x_min: float, y_min: float, x_max: float, y_max: float,
                     precision: float):
    global MARCHING_SQUARES_RESULT
    MARCHING_SQUARES_RESULT.clear()
    transform_functions_to_lambdas(json_object_describing_curve)

    m_squares(lambda x, y: eval_obj(json_object_describing_curve, x, y), (x_min, y_min, x_max, y_max), precision=precision)

    draw_curve(output_filename, x_min, y_min, x_max, y_max)


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
        example_json, './example-marching-squares-1.eps', 
        -5, 
        -5, 
        6, 
        6, 
        0.1
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
