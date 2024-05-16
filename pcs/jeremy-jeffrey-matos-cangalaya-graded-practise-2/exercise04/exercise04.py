"""
Given a triangle T (given by its vertices) and an input point P , 
decide if P ∈ T .

IDEA 1:
    Sumas el area de todos los triangulos formados por ese punto y 2 puntos consecutivos del triangulo/poligono
    Si la suma de las areas es igual al area del triangulo original, entonces el punto esta dentro del triangulo

IDEA 2:
    Para cada lado del triangulo, chequear si el punto esta a la izquierda con producto vectorial

INPUT:
    The polygon/triangle consists of n vertices (x_1,y_1),(x_2,y_2), ... ,(x_n,y_n). 
    The vertices (x_i,y_i) and (x_{i+1},y_{i+1}) are adjacent for i=1, 2, .., n-1, 
    and the vertices (x_1,y_1) and (x_n,y_n) are also adjacent in counterclockwise order.

REFERENCES:
    https://cses.fi/problemset/task/2192
TODO: QUESTIONS
    - El triangulo puede tener 2 vertices iguales?
    - A veces el input puede estar clockwise o counterclockwise, entonces la verificacion es que todos tengan el mismo signo, vd?
    - Que pasa si un punto es colineal con un lado del triangulo?
"""

import matplotlib.pyplot as plt
import numpy as np
import random

LEFT = 1
RIGHT = -1
COLLINEAR = 0

point = (np.array([1, 1]) + np.array([2, 3])) / 2  # np.array([random.uniform(0, 3.5), random.uniform(0, 3.5)])
# vertex are in counterclockwise order
polygon = np.array([[1, 1], [3, 2.5], [2, 3]])      # triangle
n = len(polygon)

def sign_of_cross_product(a: np.array, b: np.array) -> float:
    return np.sign(a[0] * b[1] - a[1] * b[0])

def orientation(a: np.array, b: np.array, c: np.array) -> int:
    """Check the orientation of 3 points a, b, c 
    calculating the cross product between vectors ab and bc
    
    Returns:
        int: 1 if counterclockwise, -1 if clockwise, 0 if collinear
    """
    s = sign_of_cross_product(a - b, c - b)
    if s > 0:
        return LEFT
    elif s < 0:
        return RIGHT
    return COLLINEAR

z_components = [
    orientation(polygon[(i + 1) % n], polygon[i], point)
    for i in range(n)
]
print(z_components)

result = all(z != RIGHT for z in z_components)

plt.plot(*point, 'o', color='black')
plt.text(point[0] + 0.1, point[1], 'P', color='black', ha='right')
for i in range(n):
    plt.plot(*polygon[i], 'o', color='blue')
    plt.plot([polygon[i][0], polygon[(i + 1) % n][0]], 
             [polygon[i][1], polygon[(i + 1) % n][1]], linestyle='-', color='red')
    plt.text(polygon[i][0] + 0.1, polygon[i][1], f'{i + 1}', fontsize=12, color='black', ha='right')
plt.title('Point in triangle' if result else 'Point outside triangle')
plt.show()
