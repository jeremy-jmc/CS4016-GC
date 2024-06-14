"""
Create a mesh that represents a sphere

iterar sobre los meridianos y las latitudes
"""

import math

def generate_sphere(radius, subdivisions, center_x=0, center_y=0, center_z=0):
    vertices = []
    faces = []
    phi_step = math.pi / subdivisions
    theta_step = 2 * math.pi / subdivisions

    # Generate vertices
    for i in range(subdivisions + 1):
        phi = i * phi_step
        for j in range(subdivisions + 1):
            theta = j * theta_step
            x = radius * math.sin(phi) * math.cos(theta) + center_x
            y = radius * math.sin(phi) * math.sin(theta) + center_y
            z = radius * math.cos(phi) + center_z
            vertices.append((x, y, z))

    # Generate triangular faces
    for i in range(subdivisions):
        for j in range(subdivisions):
            p1 = i * (subdivisions + 1) + j
            p2 = p1 + (subdivisions + 1)
            p3 = p2 + 1
            p4 = p1 + 1

            # Add two triangles for each quad, ensuring correct orientation
            if i != 0:
                faces.append((p1, p3, p4))
                faces.append((p1, p2, p3))
            if i != subdivisions - 1:
                faces.append((p1, p2, p4))
                faces.append((p2, p3, p4))

    return vertices, faces


def write_off_file(filename, vertices, faces):
    with open(filename, 'w') as file:
        file.write("OFF\n")
        file.write(f"{len(vertices)} {len(faces)} 0\n")
        for vertex in vertices:
            file.write(f"{vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            file.write(f"3 {face[0]} {face[1]} {face[2]}\n")


if __name__ == '__main__':
    radius = 1.0
    subdivisions = 20  # Increase for a smoother sphere
    center_x = 1.0
    center_y = 2.0
    center_z = 3.0

    vertices, faces = generate_sphere(radius, subdivisions, center_x, center_y, center_z)
    write_off_file("sphere_translated.off", vertices, faces)
    print("OFF file generated successfully.")


