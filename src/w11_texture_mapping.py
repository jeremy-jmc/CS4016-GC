

"""
Simple cosine ilumination
    The angle between the vision

Painter's algorithm

1. White triangles
2. Triangles with texture
3. Animation

Draw an sphere

Camera in (0, 0, 0)

Sort by the distance to the focus point
    Painter's algorithm

Dividir las 3 coordenadas
"""

from w8_meshes import generate_sphere
from scipy.spatial.distance import euclidean
import numpy as np
import matplotlib.pyplot as plt
import random

vertices, faces = generate_sphere(1.0, 50, 
                                  0, 0, 5)
vertices, faces = np.array(vertices), np.array(faces)

focus = [0, 0, 0]

def max_triangle_distance(focus: tuple, faces: tuple) -> float:
    return max([euclidean(focus, vertices[face]) for face in faces])


sort_faces = \
    sorted(faces, key=lambda face: max_triangle_distance(focus, face), reverse=True)
normalized_vertices_by_z = \
    [vertex/vertex[2] for vertex in vertices]

"""
blanco multiplicado por el coseno del angulo
para cada cara la normal, que angulo forma esa normal con el z = 1
si el angulo es mayor a 90 grados no pintar la cara

En vez de blanco multiplicado por el coseno del angulo, pintarlo en el color correspondiente a la textura
Interpolar las coordenadas baricentricas
    Combinacion convexa de los pintos A, B, C
        P = alpha_a * A + alpha_b * B + alpha_c * C
"""

def get_normal_vector_of_face(face: tuple) -> np.ndarray:
    normal_vector = np.cross(vertices[face[1]] - vertices[face[0]],
                             vertices[face[2]] - vertices[face[0]])
    norm = np.linalg.norm(normal_vector)
    if norm == 0:
        return np.zeros_like(normal_vector)
    return normal_vector / norm

normal_vector_of_sort_faces = \
    [get_normal_vector_of_face(face) for face in sort_faces]
print(normal_vector_of_sort_faces)
angle_of_sort_faces = [tup[2] for tup in normal_vector_of_sort_faces]

# angle_of_sort_faces = \
#     [np.arccos(np.dot(normal_vector, [0, 0, 1])) for normal_vector in normal_vector_of_sort_faces]

# * si es negativo no pintar la cara o de negro
color_of_sort_faces = \
    [np.array([255, 255, 255]) * cos_angle if cos_angle > 0 else [-1, -1, -1]
      for cos_angle in angle_of_sort_faces]
print(color_of_sort_faces)


plt.figure(figsize=(10, 10))
for idx, face in enumerate(sort_faces):
    tr = [normalized_vertices_by_z[v] for v in face]
    # plot triangle
    if not np.array_equal(color_of_sort_faces[idx], [-1, -1, -1]):
        # plt.plot(*tr[0], marker='o', c=random.choice(['red', 'green', 'blue', 'yellow', 'purple']))
        # plt.plot(*tr[1], marker='o', c=random.choice(['red', 'green', 'blue', 'yellow', 'purple']))
        # plt.plot(*tr[2], marker='o', c=random.choice(['red', 'green', 'blue', 'yellow', 'purple']))
        
        
        color = np.array(color_of_sort_faces[idx]) / 255
        # check if any color value is negative
        has_negative = np.any(color < 0)
        if has_negative:
            print(color)

        tr = np.array(tr).T
        plt.fill((tr[0][0], tr[0][1], tr[0][2], tr[0][0]),
                (tr[1][0], tr[1][1], tr[1][2], tr[1][0]),
                color=color,
                edgecolor='red',
                linewidth=0.25
                )
plt.show()


# TODO: vertex rotation