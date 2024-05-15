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
    and the vertices (x_1,y_1) and (x_n,y_n) are also adjacent.

REFERENCES:
    https://cses.fi/problemset/task/2192
QUESTIONS:
    - El triangulo puede tener 2 vertices iguales?
    - A veces el input puede estar clockwise o counterclockwise, entonces la verificacion es que todos tengan el mismo signo, vd?
"""

import matplotlib.pyplot as plt
import numpy as np

point = np.array([2, 2])
polygon = np.array([[1, 1], [3, 2.5], [2, 3]])      # triangle
n = len(polygon)

z_components = [
    np.sign(np.cross(polygon[(i + 1) % n] - polygon[i], point - polygon[i]))
    for i in range(n)
]
print(z_components)

result = all(z == z_components[0] for z in z_components)

plt.plot(*point, 'o', color='black')
plt.text(point[0] + 0.1, point[1], 'P', color='black', ha='right')
for i in range(n):
    plt.plot(*polygon[i], 'o', color='blue')
    plt.plot([polygon[i][0], polygon[(i + 1) % n][0]], 
             [polygon[i][1], polygon[(i + 1) % n][1]], linestyle='-', color='red')
    plt.text(polygon[i][0] + 0.1, polygon[i][1], f'{i + 1}', fontsize=12, color='black', ha='right')
plt.title('Point in triangle' if result else 'Point outside triangle')
plt.show()
