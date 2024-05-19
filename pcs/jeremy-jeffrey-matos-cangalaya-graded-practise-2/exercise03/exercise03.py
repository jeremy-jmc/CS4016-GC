"""
Given a line L, specified by one point L1 ∈ P and one direction d = (dx, dy, dz), 
compute the distance from a point P = (Px, Py, Pz) to L.

IDEA:
    Compute the parallelogram area formed by the vectors origin-P and origin-direction.
    The height of the parallelogram is the distance from P to L.
    With the area and the base, we can compute the height.

https://www.geeksforgeeks.org/minimum-distance-from-a-point-to-the-line-segment-using-vectors/
https://math.stackexchange.com/questions/2353288/point-to-line-distance-in-3d-using-cross-product
https://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
https://www.geeksforgeeks.org/shortest-distance-between-a-line-and-a-point-in-a-3-d-plane/
https://brilliant.org/wiki/dot-product-distance-between-point-and-a-line/
"""

import numpy as np


# -----------------------------------------------------------------------------
# Algorithm solution
# -----------------------------------------------------------------------------

def distance_point_line(point: np.ndarray, line_origin: np.ndarray, direction: np.ndarray) -> float:
    # base del paralelogramo
    dir_origin = direction - line_origin
    # lado del paralelogramo
    point_origin = point - line_origin

    parallelogram_area = np.linalg.norm(np.cross(dir_origin, point_origin))
    parallelogram_height = parallelogram_area / np.linalg.norm(dir_origin)

    return parallelogram_height

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test(*args, expected: float):
    result = distance_point_line(*args)
    if np.isclose(result, expected):
        print('Test passed')
    else:
        print(f'Test failed: expected {expected} but got {result}')


test(np.array([1, 2, 3]), np.array([0, 0, 0]), np.array([1, 1, 1]), expected=1.414213)
test(np.array([10, 35, 89]), np.array([0, 0, 0]), np.array([20, 12, 18]), expected=59.6480)
test(np.array([1, 2, 3]), np.array([0, 0, 0]), np.array([-3, -4, -8]), expected=0.48575)