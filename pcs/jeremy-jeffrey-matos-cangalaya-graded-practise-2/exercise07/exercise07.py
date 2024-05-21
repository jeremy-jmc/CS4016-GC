"""
Implement a function that decides if there are intersections in a set of line segments, 
with runtime proportional to N log N (where N is the number of segments in the set)

https://cp-algorithms.com/geometry/intersecting_segments.html
https://stackoverflow.com/questions/37873954/what-are-pythons-equivalents-of-stdlower-bound-and-stdupper-bound-c-algor
https://www.geeksforgeeks.org/given-a-set-of-line-segments-find-if-any-two-segments-intersect/
https://understandingg.is/Generalisation/
https://wrfranklin.org/p/214-mauricio-iceis-2015.pdf
https://strncat.github.io/
https://strncat.github.io/jekyll/update/2020/05/15/any-pair-of-segments-intersection.html
https://panda-man.medium.com/mastering-efficiency-exploring-line-sweep-algorithm-with-python-673e4522e979
"""

from sortedcontainers import SortedList
from collections import deque
import numpy as np
import matplotlib.pyplot as plt


def plot_segments(segments: list, intersections: list, title: str):
    for segment in segments:
        plt.plot([segment[0][0], segment[1][0]], [segment[0][1], segment[1][1]],
                 color='black', marker='o', linestyle='-')

    for intersection in intersections:
        s1, s2 = intersection
        plt.plot([s1[0][0], s1[1][0]], [s1[0][1], s1[1][1]],
                 color='red', marker='o', linestyle=':')
        plt.plot([s2[0][0], s2[1][0]], [s2[0][1], s2[1][1]],
                 color='red', marker='o', linestyle=':')
    plt.title(title)
    plt.show()


def on_segment(p: np.ndarray, q: np.ndarray, r: np.ndarray) -> bool:
    in_x_range = q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0])
    in_y_range = q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])
    if in_x_range and in_y_range:
        return True
    return False


def intersection(s1: np.ndarray, s2: np.ndarray) -> bool:
    A, B = s2[0], s2[1]
    C, D = s1[0], s1[1]

    # * (-): left, 0: parallel/collinear, (+): right
    ba_ca = np.cross(B - A, C - A)
    ba_da = np.cross(B - A, D - A)
    dc_ac = np.cross(D - C, A - C)
    dc_bc = np.cross(D - C, B - C)

    if np.sign(ba_ca) != np.sign(ba_da) and np.sign(dc_ac) != np.sign(dc_bc):
        return True

    elif ba_ca == 0 and on_segment(A, C, B):
        return True
    elif ba_da == 0 and on_segment(A, D, B):
        return True
    elif dc_ac == 0 and on_segment(C, A, D):
        return True
    elif dc_bc == 0 and on_segment(C, B, D):
        return True

    return False


class Event:
    def __init__(self, point: np.ndarray, start: bool, index: list):
        self.x, self.y = point
        self.start = start
        self.index = index

    def __lt__(self, other):
        if self.y == other.y:
            return self.x < other.x
        return self.y < other.y

    def __eq__(self, other):
        return self.index == other.index

    def __repr__(self):
        return f'[({self.x}, {self.y}), {self.start}]'


def sweep_line(segments: list) -> list:
    events = []
    for idx, segment in enumerate(segments):
        events.append(Event(segment[0], True, idx))
        events.append(Event(segment[1], False, idx))

    events.sort(key=lambda e: (e.x, not e.start))

    active_segments = SortedList(key=lambda e: (e.y, e.x))
    intersections = deque()

    def add_intersection(i1, i2):
        if (i1, i2) not in intersections and (i2, i1) not in intersections:
            intersections.append((i1, i2))

    start_events = {}

    for event in events:
        event_type, index = event.start, event.index
        # print(active_segments)
        if event_type == True:
            active_segments.add(event)
            start_events[index] = event
            pos = active_segments.index(event)

            if pos > 0 and intersection(segments[active_segments[pos - 1].index],
                                        segments[index]):
                add_intersection(active_segments[pos - 1].index, index)

            if pos < len(active_segments) - 1 and intersection(segments[active_segments[pos + 1].index],
                                                               segments[index]):
                add_intersection(active_segments[pos + 1].index, index)
        else:  # event_type == 'end'
            start_event = start_events[index]
            pos = active_segments.index(start_event)

            if pos > 0 and pos < len(active_segments) - 1:
                if intersection(segments[active_segments[pos - 1].index], segments[active_segments[pos + 1].index]):
                    add_intersection(active_segments[pos - 1].index, 
                                     active_segments[pos + 1].index)

            active_segments.remove(start_event)

    intersections = [(segments[i1], segments[i2]) for i1, i2 in intersections]
    return intersections


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------

segments_list = np.array([
    [[1, 5], [4, 5]],
    [[2, 5], [10, 1]],
    [[3, 2], [10, 3]],
    [[6, 4], [9, 4]],
    [[7, 1], [8, 1]]
])


intersections = sweep_line(segments_list)
plot_segments(segments_list, intersections, 
              f'Intersections: {len(intersections)}')

segments_list = np.array([
    [[2, 3], [6, 5]],
    [[2, 2], [8, 3]],
    [[4, 1], [9, 5]],
    [[2, 6], [10, 3]],
    [[10, 8], [17, 2]]
])
intersections = sweep_line(segments_list)
plot_segments(segments_list, intersections, 
              f'Intersections: {len(intersections)}')