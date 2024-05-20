"""
Implement a function that compute the 2 closest points in a given set of N points, 
with 1 ≤ N ≤ 1000000.

http://staff.ustc.edu.cn/~csli/graduate/algorithms/book6/chap35.htm
http://serverbob.3x.ro/IA/DDU0221.html
"""

import numpy as np
from collections import deque

def closest_pair_points_dc(px: list, py: list, n: int) -> tuple:    
    if n <= 3:
        # base case
        min_dist = float('inf')
        pair = None

        for i in range(n):
            for j in range(i + 1, n):
                dist = np.linalg.norm(np.array(px[i]) - np.array(px[j]))
                if dist < min_dist:
                    min_dist = dist
                    pair = (px[i], px[j])

        return (min_dist, pair)
    # divide
    mid = n // 2
    mid_point = px[mid]

    py_l = [None] * mid
    py_r = [None] * (n - mid)

    li, ri = 0, 0
    for i in range(n):
        if (py[i][0] <= mid_point[0] or (py[i][0] == mid_point[0] and py[i][1] <= mid_point[1])) and li < mid:
            py_l[li] = py[i]
            li += 1
        else:
            py_r[ri] = py[i]
            ri += 1

    # conquer
    d_l, pair_l = closest_pair_points_dc(px[:mid], py_l, mid)
    d_r, pair_r = closest_pair_points_dc(px[mid:], py_r, n - mid)

    # combine
    min_dist = min(d_l, d_r)
    if min_dist == d_l:
        pair = pair_l
    else:
        pair = pair_r

    strip = deque()
    for i in range(n):
        if abs(py[i][0] - mid_point[0]) < min_dist:
            strip.append(py[i])

    sz = len(strip)
    for i in range(sz):
        for j in range(i+1, sz):
            if strip[j][1] - strip[i][1] >= min_dist:
                break

            dist = np.linalg.norm(np.array(strip[i]) - np.array(strip[j]))
            if dist < min_dist:
                min_dist = dist
                pair = (strip[i], strip[j])

    return (min_dist, pair)

def closest_pair_points(point_list: list) -> tuple:
    """Compute the 2 closest points in a given set of N points. in O(N log N) time complexity."""
    p_x = sorted(point_list, key=lambda x: x[0])
    p_y = sorted(point_list, key=lambda x: x[1])

    return closest_pair_points_dc(p_x, p_y, len(point_list))


# test cases
print(closest_pair_points([(0, 0), (1, 1), (3, 3), (4, 4), (5, 5)]))
print(closest_pair_points([(1, 1), (1, 1), (2, 2), (3, 3)]))
print(closest_pair_points([(0, 0), (1, 1), (2, 2), (0.1, 0.1), (2.1, 2.1)]))