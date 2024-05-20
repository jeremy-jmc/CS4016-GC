"""
Implement Visvalingam-Whyatt

INPUT:
    A polyline P in the form of a list of points, where each point is a tuple (x, y)
    A tolerance value ε or area tolerance

https://en.wikipedia.org/wiki/Visvalingam%E2%80%93Whyatt_algorithm
https://github.com/Permafacture/Py-Visvalingam-Whyatt/blob/master/polysimplify.py
https://bost.ocks.org/mike/simplify/
https://www.jasondavies.com/simplify/
https://stackoverflow.com/questions/10558299/visvalingam-whyatt-polyline-simplification-algorithm-clarification
https://archive.is/Tzq2
"""

import heapq
import numpy as np
import matplotlib.pyplot as plt


def plot_polyline(polyline: np.ndarray, simplified: np.ndarray, figsize: tuple = ()):
    if len(figsize) == 0:
        plt.figure()
    else:
        plt.figure(figsize=figsize)

    x, y, _ = polyline.T
    plt.plot(x, y, 'o-', label='Original', linewidth=2.5)
    for i, (x, y, _) in enumerate(polyline):
        plt.text(x, y, f'{i}', ha='right', va='bottom')

    if len(simplified) > 0:
        x, y, _ = simplified.T
        plt.plot(x, y, marker='o', linestyle='-.', label='Simplified')

    plt.title('Visvalingam Whyatt')
    plt.legend()
    plt.show()


def plot_vwhyatt(points: list):
    polyline = np.array([point.data for point in points])
    simplified = np.array(
        [point.data for point in points if point.prev or point.next])
    plot_polyline(polyline, simplified)


class Point:
    def __init__(self, data: np.ndarray):
        self.data = data
        self.prev = None
        self.next = None
        self.area = 0

    def __lt__(self, other):
        return self.area < other.area

    def __repr__(self) -> str:
        return f"Point: {list(self.data)} {self.area}"


def area(point: Point) -> float:
    if point.prev is None or point.next is None:
        return float('inf')
    ab = point.next.data - point.data
    cb = point.prev.data - point.data
    return np.linalg.norm(np.cross(ab, cb)) / 2


def remove(point: list):
    if point.prev:
        point.prev.next = point.next
    if point.next:
        point.next.prev = point.prev

    point.prev = None
    point.next = None


def update(point: Point, heap: list):
    # TODO: optimize complexity
    heap.remove(point)
    heapq.heapify(heap)
    point.area = area(point)
    heapq.heappush(heap, point)


def visvalingam_whyatt(points: list):
    heap = []
    for point in points:
        heapq.heappush(heap, point)

    while len(heap) > 2:
        plot_vwhyatt(points)
        point = heapq.heappop(heap)
        # print(heap)
        remove(point)

        if point.prev:
            update(point.prev, heap)
        if point.next:
            update(point.next, heap)
    plot_vwhyatt(points)


def preprocessing(polygon):
    points = [Point(np.append(xy, 0)) for xy in polygon]

    for i in range(len(points)):
        if i > 0:
            points[i].prev = points[i - 1]
        if i < len(points) - 1:
            points[i].next = points[i + 1]
        points[i].area = area(points[i])

    return points


# -----------------------------------------------------------------------------
# Visualize the results
# -----------------------------------------------------------------------------

polyline = np.array([[1, 1], [3, -2], [5, -2], [7, 1],
                    [9, 3], [11, 2.5], [13, -1], [15, 1.5]])
points = preprocessing(polyline)

visvalingam_whyatt(points)

polygon = np.array([
    [0.0, 0.0],
    [1.0, 0.5],
    [2.0, 0.0],
    [3.0, 0.5],
    [3.75, -2],
    [4.0, -5.0],
    [3.0, -5.5],
    [3.0, -4.0],
    [2.5, -3.5],
    [1.5, -1.0],
    [0.0, 0.0]  # Cerrando el polígono
])
points = preprocessing(polygon)
visvalingam_whyatt(points)
