# -----------------------------------------------------------------------------
# PROBLEM 1: Convex hull algorithms
# -----------------------------------------------------------------------------
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
import random

class Point:
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def to_numpy(self):
        return np.array([self.x, self.y, self.z])
    
    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'
    
    def __eq__(self, other):
        if isinstance(other, Point):
            return all(getattr(self, attr) == getattr(other, attr) for attr in ['x', 'y', 'z'])
        return False
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))

def random_point(start: int = -10, end: int = 10) -> Point:
    return Point(random.randint(start, end), random.randint(start, end))


def orientation(first: Point, second: Point, third: Point) -> int:
    """Determine the orientation of the triplet (first, second, third)

    Logic:
        Slope of first-second
            first.x - second.x / first.y - second.y
        Slope of second-third
            second.x - third.x / second.y - third.y

        Comparing
            (first.x - second.x) * (second.y - third.y) - (first.y - second.y) * (second.x - third.x)

    -1: clockwise
    0: collinear
    1: counterclockwise

    Source:
        https://www.geeksforgeeks.org/orientation-3-ordered-points/
    """
    val = (first.x - second.x) * (second.y - third.y) - (first.y - second.y) * (second.x - third.x)
    if val == 0:
        return 0
    return 1 if val > 0 else -1


def generate_points(n_points: int = 50) -> list:
    point_list = [random_point(1, 20) for _ in range(n_points)]
    print(f'Generated {len(point_list)} points')
    point_list = list(set(point_list))
    print(f'Unique points: {len(point_list)}')

    plt.figure(figsize=(4, 4))
    for p in point_list:
        plt.plot(p.x, p.y, 'o', color='black', markersize=3)
    plt.show()
    return point_list

# -----------------------------------------------------------------------------
# PROBLEM 1: Convex hull algorithms
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Jarvis March
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# * Graham's scan
# -----------------------------------------------------------------------------

point_list = generate_points()
print(point_list)

pivot = min(point_list, key=lambda p: (p.y, p.x))
print(f'pivot: {pivot}')
point_list.remove(pivot)
# sort the points based on the polar angle
comparer = lambda p: (np.arctan2(p.y - pivot.y, p.x - pivot.x) * 180 / np.pi, np.sqrt((p.x - pivot.x) ** 2 + (p.y - pivot.y) ** 2))
point_list.sort(key=comparer)
print(point_list)

# # plot points with their idx
# plt.figure(figsize=(10, 10))
# plt.plot(pivot.x, pivot.y, 'o', color='red', markersize=3)
# for idx, p in enumerate(point_list):
#     plt.plot(p.x, p.y, 'o', color='black', markersize=3)
#     angle = np.arctan2(p.y - pivot.y, p.x - pivot.x) * 180 / np.pi
#     plt.text(p.x, p.y, f'{angle:.2f}', fontsize=10, ha='right')
# plt.show()

stack = [pivot]
for p in point_list:
    while len(stack) > 1 and orientation(stack[-2], stack[-1], p) == -1:
        stack.pop()
    stack.append(p)

plt.figure(figsize=(10, 10))
for p in point_list:
    plt.plot(p.x, p.y, 'o', color='black', markersize=5)

for idx, p in enumerate(stack):
    plt.plot(p.x, p.y, 'o', color='blue', markersize=5)
    angle = np.arctan2(p.y - pivot.y, p.x - pivot.x) * 180 / np.pi
    # plt.text(p.x, p.y, f'{idx}', fontsize=10, ha='right')
    plt.text(p.x, p.y, f'{angle:.2f}', fontsize=10, ha='left')

plt.plot(pivot.x, pivot.y, 'o', color='red', markersize=5)

for i in range(len(stack)):
    plt.plot([stack[i].x, stack[(i + 1) % len(stack)].x], 
             [stack[i].y, stack[(i + 1) % len(stack)].y], color='green', linestyle='--')
plt.show()

# -----------------------------------------------------------------------------
# Andrew's monotone chain
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Quickhull
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# PROBLEM 2: Sweep line intersections in a set of line segments
# -----------------------------------------------------------------------------
"""
https://ics.uci.edu/~goodrich/teach/geom/notes/LineSweep.pdf
https://i11www.iti.kit.edu/_media/teaching/winter2015/compgeom/algogeom-ws15-vl02.pdf
https://cp-algorithms.com/geometry/intersecting_segments.html
Line Segment Intersection - Computational Geometry book
"""

# -----------------------------------------------------------------------------
# PROBLEM 3: Closest pair of points with sweep line
# -----------------------------------------------------------------------------
# https://cses.fi/problemset/task/2194

# -----------------------------------------------------------------------------
# PROBLEM 4: Area covered by N rectangles
# -----------------------------------------------------------------------------
"""
Segment Tree
"""


# -----------------------------------------------------------------------------
# PROBLEM 5: minimum flood fill operations
# -----------------------------------------------------------------------------

"""
minimum flood fill operations to monochromatic
https://people.maths.ox.ac.uk/scott/Papers/spanflood.pdf
"""


# -----------------------------------------------------------------------------
# PROBLEM 6: The Josephus problem
# -----------------------------------------------------------------------------

"""
https://en.wikipedia.org/wiki/Josephus_problem
N personas en un circulo
    Mata dejando 1 mi causa
    Elige un salto k

J(N)
    N = 1e9

N en binario
    agarrar el primer bit y lo ponemos al final
"""