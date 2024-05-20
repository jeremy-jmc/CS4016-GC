"""
Given a non-crossed polygonal region P and a points A, 
write a function to decide if A ∈ P .

IDEA:
    Sum the angles between the point and the sides of the polygon.
    If the sum is 2π, the point is inside the polygon.
    If the sum is 0, the point is outside the polygon.

https://www.eecs.umich.edu/courses/eecs380/HANDOUTS/PROJ2/InsidePoly.html
https://www.reddit.com/r/gamemaker/comments/14nsit6/check_if_a_pointclick_is_inside_a_polygon/
https://codeforces.com/blog/entry/48868
https://acm.timus.ru/problem.aspx?space=1&num=1599
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_point_polygon(polygon: np.ndarray, point: np.ndarray, result: bool) -> None:
    """Plot a polygon and a point in 2D space"""
    n = len(polygon)

    plt.figure(figsize=(5, 5))
    plt.plot(*point, 'o', color='black')
    plt.text(point[0] + 0.1, point[1], 'P', color='black', ha='right')
    for i in range(n):
        plt.plot(*polygon[i], 'o', color='blue')
        plt.plot([polygon[i][0], polygon[(i + 1) % n][0]],
                 [polygon[i][1], polygon[(i + 1) % n][1]], linestyle='-', color='red')
        plt.text(polygon[i][0] + 0.1, polygon[i][1],
                 f'{i + 1}', fontsize=12, color='black', ha='right')

    title = 'Result: ' + \
        str('Point in triangle' if result else 'Point outside triangle')
    plt.title(title)
    plt.show()



def point_inside_polygon(point: np.ndarray, polygon: np.ndarray) -> bool:

    def angle(a, b, c) -> float:
        v1 = a - b
        v2 = c - b
        return np.arctan2(np.cross(v1, v2), np.dot(v1, v2)) * 180 / np.pi

    n = len(polygon)
    angles = [angle(polygon[i], point, polygon[(i + 1) % n]) for i in range(n)]
    
    return sum(angles) == 360

def test(*args, expected: bool):
    result = point_inside_polygon(*args)
    if result == expected:
        print('Test passed')
    else:
        print(f'Test failed: expected {expected} but got {result}')
        plot_point_polygon(args[1], args[0], result)


triangle = np.array([[0, 0], [2, 0], [1, 2]])
point_inside = np.array([1, 1])
point_outside = np.array([3, 1])

test(point_inside, triangle, expected=True)
test(point_outside, triangle, expected=False)

concave_polygon = np.array([[0, 0], [4, 0], [2, 1], [4, 4], [0, 4]])
point_inside_concave = np.array([2, 2])
point_outside_concave = np.array([2, -1])
test(point_inside_concave, concave_polygon, expected=True)
test(point_outside_concave, concave_polygon, expected=False)