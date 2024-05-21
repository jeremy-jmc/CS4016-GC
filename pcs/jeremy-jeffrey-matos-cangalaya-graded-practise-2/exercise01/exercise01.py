"""
Write a function that receives 4 points (given by their coordinates)
    a = (xa , ya ), 
    b = (xb , yb ), 
    c = (xc , yc ), 
    d = (xd , yd ), and returns true if and only

ab ∩ cd = ∅.
"""

import matplotlib.pyplot as plt
import numpy as np
import random

random.seed(42)


class Point:
    def __init__(self, x: int, y: int, z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    def to_numpy(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])

    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f"Segment: ({self.p1.x}, {self.p1.y}) -> ({self.p2.x}, {self.p2.y})"

# -----------------------------------------------------------------------------
# Utilitites
# -----------------------------------------------------------------------------

def random_point(start: int = 1, end: int = 3) -> Point:
    """Generate a random point given a range"""
    return Point(random.randint(start, end), random.randint(start, end))


def plot_segment(s1: Segment, s2: Segment, title: str = ''):
    """Plot two segments in a graph with matplotlib"""
    plt.figure(figsize=(4, 4))
    plt.plot([s1.p1.x, s1.p2.x], [s1.p1.y, s1.p2.y],
             color='blue', marker='o', linestyle='--')
    plt.plot([s2.p1.x, s2.p2.x], [s2.p1.y, s2.p2.y],
             color='red', marker='o', alpha=0.5)

    plt.text(s1.p1.x, s1.p1.y, 'A', fontsize=12, ha='center')
    plt.text(s1.p2.x, s1.p2.y, 'B', fontsize=12, ha='center')
    plt.text(s2.p1.x, s2.p1.y, 'C', fontsize=12, ha='center')
    plt.text(s2.p2.x, s2.p2.y, 'D', fontsize=12, ha='center')

    plt.title(title)
    plt.show()


# -----------------------------------------------------------------------------
# Algorithm solution
# -----------------------------------------------------------------------------

def on_segment(p: np.ndarray, q: np.ndarray, r: np.ndarray) -> bool:
    """Check if point q is on segment pr, given p, q, r collinear points"""

    assert len(p) == len(q) == len(r) == 3, 'Invalid points'
    p = Point(*p)
    q = Point(*q)
    r = Point(*r)

    in_x_range = q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x)
    in_y_range = q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)
    if in_x_range and in_y_range:
        return True
    return False


def check_line_intersection(s1: Segment, s2: Segment) -> bool:
    """Check if two segments intersects
    References:
        https://www.geeksforgeeks.org/orientation-3-ordered-points/
    """
    A, B = s2.p1.to_numpy(), s2.p2.to_numpy()
    C, D = s1.p1.to_numpy(), s1.p2.to_numpy()

    # print(f'{A=} {B=} {C=} {D=}')

    # * (-): left, 0: parallel/collinear, (+): right
    ba_ca = np.cross(B - A, C - A)[2]
    ba_da = np.cross(B - A, D - A)[2]
    dc_ac = np.cross(D - C, A - C)[2]
    dc_bc = np.cross(D - C, B - C)[2]

    # print(f'{ba_ca=} {ba_da=} {dc_ac=} {dc_bc=}')

    if np.sign(ba_ca) != np.sign(ba_da) and np.sign(dc_ac) != np.sign(dc_bc):
        return True
    # Collinear
    # Dado que son colineales (situados sobre la misma recta, por lo tanto paralelos),
    # solo se verifica si un punto esta en el rango de las X e Y del otro segmento
    elif ba_ca == 0 and on_segment(A, C, B):
        return True
    elif ba_da == 0 and on_segment(A, D, B):
        return True
    elif dc_ac == 0 and on_segment(C, A, D):
        return True
    elif dc_bc == 0 and on_segment(C, B, D):
        return True

    return False


# -----------------------------------------------------------------------------
# Test cases
# -----------------------------------------------------------------------------

def cases(case_type: str = 'random') -> tuple[Segment, Segment]:
    if case_type == 'collinear':
        return Segment(Point(1, 2), Point(3, 4)), \
            Segment(Point(4, 5), Point(6, 7))
    elif case_type == 'collinear_overlap':
        return Segment(Point(1, 2), Point(3, 4)), \
            Segment(Point(2, 3), Point(4, 5))
    elif case_type == 'intersection':
        return Segment(Point(1, 2), Point(3, 4)), \
            Segment(Point(1, 4), Point(3, 2))
    elif case_type == 'random':
        return Segment(random_point(), random_point()), \
            Segment(random_point(), random_point())
    else:
        raise ValueError('Invalid case_type')


for case_type in ['collinear',  'collinear_overlap', 'intersection', 'random']:
    segment_1, segment_2 = cases(case_type)

    line_intersection = check_line_intersection(segment_1, segment_2)
    plot_segment(segment_1, segment_2,
                 f'{case_type} -> ' + ('Intersects' if line_intersection else 'Not intersect'))
