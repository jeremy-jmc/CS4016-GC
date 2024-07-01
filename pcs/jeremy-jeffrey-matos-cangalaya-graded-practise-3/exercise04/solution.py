import numpy as np
import math

def create_off(output_file: str, vertices: list, faces: list):
    with open(output_file, mode='w') as file:
        file.write('OFF\n')
        file.write(f'{len(vertices)} {len(faces)} 0\n')
        file.write('\n')

        for v in vertices:
            file.write(f'{" ".join(map(str, v))}\n')
        
        file.write('\n')
        for face in faces:
            file.write(f'{len(face)} {" ".join(map(str, face))}\n')


def create_ply(output_file: str, vertices: list, faces: list):
    with open(output_file, mode='w') as file:
        file.write('ply\n')
        file.write('format ascii 1.0\n')
        file.write(f'element vertex {len(vertices)}\n')
        file.write('property float x\n')
        file.write('property float y\n')
        file.write('property float z\n')
        file.write(f'element face {len(faces)}\n')
        file.write('property list uchar int vertex_index\n')
        file.write('end_header\n')
        file.write('\n')

        for v in vertices:
            file.write(f'{" ".join(map(str, v))}\n')
        
        file.write('\n')
        for face in faces:
            file.write(f'{len(face)} {" ".join(map(str, face))}\n')


def sphere_with_triangular_faces(full_path_output_file: str, radius: float, center: tuple):
    vertices, faces = [], []

    theta_steps = 90
    phi_steps = 180

    center_x, center_y, center_z = center
    for theta in range(0, theta_steps + 1):
        for phi in range(0, phi_steps + 1):
            x = center_x + radius * math.sin(math.radians(theta * 180 / theta_steps)) * math.cos(math.radians(phi * 360 / phi_steps))
            y = center_y + radius * math.sin(math.radians(theta * 180 / theta_steps)) * math.sin(math.radians(phi * 360 / phi_steps))
            z = center_z + radius * math.cos(math.radians(theta * 180 / theta_steps))
            vertices.append([x, y, z])
        
    for theta in range(theta_steps):
        for phi in range(phi_steps):
            i = theta * (phi_steps + 1) + phi
            faces.append([i, i + phi_steps + 2, i + 1])
            faces.append([i, i + phi_steps + 1, i + phi_steps + 2])

    # print(len(vertices), len(faces))
    if full_path_output_file.endswith(".off"):
        create_off(full_path_output_file, vertices, faces)
    elif full_path_output_file.endswith(".ply"):
        create_ply(full_path_output_file, vertices, faces)

if __name__ == "__main__":
    sphere_with_triangular_faces(
        full_path_output_file="sphere-triangles.off", radius=5, center=(0, 0, 10)
    )
    # --> Produces an OFF mesh of a sphere of radius 5 centered at (2,3,5)
    sphere_with_triangular_faces(
        full_path_output_file="sphere-triangles.ply", radius=5, center=(0, 0, 10)
    )
    # --> Produces a PLY mesh of a sphere of radius 5 centered at (2,3,5)
