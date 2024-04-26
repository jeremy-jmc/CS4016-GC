import matplotlib.pyplot as plt
import numpy as np
import random

# random.seed(42)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.z = 0

    def to_numpy(self):
        return np.array([self.x, self.y, self.z])


def random_point() -> Point:
    return Point(random.randint(1, 3), random.randint(1, 3))


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f"Segment: ({self.p1.x}, {self.p1.y}) -> ({self.p2.x}, {self.p2.y})"


def plot_segment(s1, s2, title=""):
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


def check_line_intersection(s1, s2):
    A, B = s2.p1.to_numpy(), s2.p2.to_numpy()
    C, D = s1.p1.to_numpy(), s1.p2.to_numpy()

    print(f'{A=} {B=} {C=} {D=}')

    # -1: left, 0: intersects, 1: right
    AB_wrt_CD = np.sign(np.cross(B - A, C - A)[2]) * np.sign(np.cross(B - A, D - A)[2])
    CD_wrt_AB = np.sign(np.cross(D - C, D - A)[2]) * np.sign(np.cross(D - C, D - B)[2])

    print(AB_wrt_CD, CD_wrt_AB)

    # TODO: revisar los casos patologicos
    if AB_wrt_CD == CD_wrt_AB:
        return True
    return False


# -----------------------------------------------------------------------------
# EXERCISE 2: Check if two segments intersects (or not)
# -----------------------------------------------------------------------------

def cases(case_type = ""):
    if case_type == 'collinear':
        return Segment(Point(1, 2), Point(3, 4)), \
            Segment(Point(4, 5), Point(6, 7))
    elif case_type == 'collinear_overlap':
        return Segment(Point(1, 2), Point(3, 4)),\
            Segment(Point(1, 2), Point(4, 5))
    elif case_type == 'intersection':
        return Segment(Point(1, 2), Point(3, 4)),\
            Segment(Point(1, 4), Point(3, 2))
    elif case_type == 'random':
        return Segment(random_point(), random_point()), \
            Segment(random_point(), random_point())
    else:
        raise ValueError('Invalid case_type')

"""
segment_1 = Segment(Point(1, 1), Point(3, 3))
segment_2 = Segment(Point(1, 3), Point(3, 1))

segment_1 = Segment(Point(1, 3), Point(2, 2))
segment_2 = Segment(Point(1.5, 2.5), Point(3, 1))
"""

for case_type in ['collinear', 'collinear_overlap', 'intersection', 'random']:
    segment_1, segment_2 = cases(case_type)

    line_intersection = check_line_intersection(segment_1, segment_2)
    plot_segment(segment_1, segment_2,
                case_type + ' Intersects' if line_intersection else ' No intersects')


# -----------------------------------------------------------------------------
# EXERCISE 3: Distance from a point to a line
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# EXERCISE 4: Check if a point P belongs to a triangle T
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# EXERCISE 5: 
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# EXERCISE 6: 
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# EXERCISE 7: 
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# EXERCISE 8: 
# -----------------------------------------------------------------------------
"""
focal distance
divide by Z
    project (X, Y, Z) dividing by Z obtaining (X/Z, Y/Z, Z/Z)
back face culling
"""

# -----------------------------------------------------------------------------
# EXERCISE 9: 
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# EXERCISE 10: 
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# EXERCISE 11: 
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# EXERCISE 12: 
# -----------------------------------------------------------------------------

