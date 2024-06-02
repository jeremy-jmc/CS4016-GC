import numpy as np

MAX_DEPTH = 10
N_SAMPLING = 10000

def f(x: float, y: float, radius: int = 10) -> float:
    return x**2 + y**2 - radius**2


def generate_random_points(n: int, x_range: tuple, y_range: tuple) -> np.ndarray:
    p_sampling = []
    for _ in range(n):
        x = np.random.uniform(*x_range)
        y = np.random.uniform(*y_range)
        p_sampling.append((x, y))
    return np.array(p_sampling)


def marching_squares(f, x_range: tuple, y_range: tuple, depth: int = 1):
    if depth > MAX_DEPTH:
        return
    p_sampling = generate_random_points(N_SAMPLING, x_range, y_range)
    eval_points = np.array([f(*point) for point in p_sampling])
    # print(eval_points)
    
    # * contar (+) (-) (0)
    n_positives = len(eval_points[eval_points > 0])#.shape[0]
    n_negatives = len(eval_points[eval_points < 0])#.shape[0]
    n_zeros = len(eval_points[eval_points == 0])#.shape[0]

    print(n_positives, n_negatives, n_zeros)

    if n_positives > 0 and n_negatives > 0:
        # do division
        pass


    

marching_squares(f, (-20, 20), (-20, 20))
