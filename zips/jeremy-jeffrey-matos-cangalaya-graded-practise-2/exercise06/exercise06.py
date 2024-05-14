"""
Implement the Jarvis march and the Graham scan, with and without integer points elimination.

TODO: Akl-Toussaint heuristic
"""

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


def random_point(start: int = 1, end: int = 3) -> Point:
    """Generate a random point given a range"""
    return Point(random.randint(start, end), random.randint(start, end))


def generate_points(n_points: int = 50, start: int = 1, end: int = 20) -> list:
    """Generate a list of random points given a range"""
    point_list = []
    while len(point_list) < n_points:
        new_point = random_point(start, end)
        if new_point not in point_list:
            point_list.append(new_point)

    print(f'Generated {len(point_list)} points')

    plt.figure(figsize=(5, 5))
    for p in point_list:
        plt.plot(p.x, p.y, 'o', color='black', markersize=3)
    plt.show()

    return point_list


# -----------------------------------------------------------------------------
# Algorithm utilities
# -----------------------------------------------------------------------------

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


def plot_convex_hull(point_list: list, convex_hull: list) -> None:
    plt.figure(figsize=(5, 5))
    for p in point_list:
        plt.plot(p.x, p.y, 'o', color='black', markersize=5)

    for i, p in enumerate(convex_hull):
        plt.plot(p.x, p.y, 'o', color='blue', markersize=5)
        plt.plot([p.x, convex_hull[(i + 1) % len(convex_hull)].x], 
                [p.y, convex_hull[(i + 1) % len(convex_hull)].y], color='green', linestyle='--')
    plt.show()

# -----------------------------------------------------------------------------
# Convex Hull algorithms
# -----------------------------------------------------------------------------

def graham_scan(point_list: list) -> list:
    """Graham's scan algorithm to find the convex hull of a set of points

    Returns:
        list: list of points that form the convex hull
    """
    pivot = min(point_list, key=lambda p: (p.y, p.x))
    point_list.remove(pivot)

    # sort the points based on the polar angle
    comparer = lambda p: (np.arctan2(p.y - pivot.y, p.x - pivot.x) * 180 / np.pi, np.sqrt((p.x - pivot.x) ** 2 + (p.y - pivot.y) ** 2))
    point_list.sort(key=comparer)

    stack = [pivot]
    for p in point_list:
        while len(stack) > 1 and \
            orientation(stack[-2], stack[-1], p) == -1:
            stack.pop()
        stack.append(p)

    return stack


def jarvis_march(point_list: list):
    pass

point_list = generate_points()
graham_scan_convex_hull = graham_scan(point_list)

plot_convex_hull(point_list, graham_scan_convex_hull)