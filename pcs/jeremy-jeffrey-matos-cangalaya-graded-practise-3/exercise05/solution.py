import numpy as np
import math
import cv2


def read_ply(input_file: str):
    vertices = []
    faces = []
    vertex_count = 0
    face_count = 0
    
    with open(input_file, mode='r') as file:
        line = file.readline().strip()
        if line != 'ply':
            raise ValueError('The file does not start with "ply". It is not a valid PLY file.')

        line = file.readline().strip()
        if line != 'format ascii 1.0':
            raise ValueError('Only ASCII format PLY files are supported.')
        
        line = file.readline().strip()
        while line != 'end_header':
            if line.startswith('element vertex'):
                vertex_count = int(line.split()[-1])
            elif line.startswith('element face'):
                face_count = int(line.split()[-1])
            line = file.readline().strip()

        for _ in range(vertex_count):
            line = ""
            while not line:
                line = file.readline().strip()
            
            vertex = list(map(float, line.split()))
            vertices.append(vertex)
    
        for _ in range(face_count):
            line = ""
            while not line:
                line = file.readline().strip()
            face_data = list(map(int, line.split()))
            face = face_data[1:]
            faces.append(face)
    
    assert len(vertices) == vertex_count, f"Expected {vertex_count} vertices, but got {len(vertices)}"
    assert len(faces) == face_count, f"Expected {face_count} faces, but got {len(faces)}"
    
    return vertices, faces


def create_ply(output_file: str, vertices: list, faces: list):
    with open(output_file, mode='w') as file:
        file.write('ply\n')
        file.write('format ascii 1.0\n')
        
        # Escribir el encabezado para los vértices
        file.write(f'element vertex {len(vertices)}\n')
        file.write('property float x\n')
        file.write('property float y\n')
        file.write('property float z\n')
        file.write('property float u\n')  # Coordenada de textura u
        file.write('property float v\n')  # Coordenada de textura v
        file.write('property uchar red\n')
        file.write('property uchar green\n')
        file.write('property uchar blue\n')
        
        file.write(f'element face {len(faces)}\n')
        file.write('property list uchar int vertex_indices\n')
        file.write('end_header\n')

        for v in vertices:
            file.write(f'{" ".join(map(str, v))}\n')
        
        for face in faces:
            if all(0 <= index < len(vertices) for index in face):
                file.write(f'{len(face)} {" ".join(map(str, face))}\n')
            else:
                print(f"Bad vertex index in face: {face}")  # Depuración
                raise ValueError("Bad vertex index in face: some indices refer to non-existent vertices.")


def sphere_with_texture(
    full_path_input_ply: str,
    full_path_texture: str,
    center: tuple,
    full_path_output_ply: str,
):
    vertices, faces = read_ply(full_path_input_ply)
    
    texture_data = cv2.imread(full_path_texture)
    texture_data = cv2.cvtColor(texture_data, cv2.COLOR_BGR2RGB)
    texture_height, texture_width, _ = texture_data.shape
    
    center_x, center_y, center_z = center
    for vertex in vertices:
        if vertex == []:
            continue
        vx, vy, vz = map(float, vertex[:3])
        
        # Convertir a coordenadas polares
        theta = math.atan2(vy - center_y, vx - center_x)
        phi = math.acos((vz - center_z) / np.linalg.norm([vx - center_x, vy - center_y, vz - center_z]))
        
        # Normalizar a rango [0, 1]
        u = (theta + math.pi) / (2 * math.pi)
        v = phi / math.pi
        
        # Mapear coordenadas de textura a píxeles en la imagen de textura
        tex_x = int(u * (texture_width - 1))
        tex_y = int((1 - v) * (texture_height - 1))
        
        # Obtener el color de la textura en las coordenadas calculadas
        color = texture_data[tex_y, tex_x]
        
        # Añadir coordenadas de textura y color al vértice
        vertex.extend([u, v, color[0], color[1], color[2]])
    
    # print(f"Total vertices with texture: {len(vertices)}")
    create_ply(full_path_output_ply, vertices, faces)


if __name__ == "__main__":
    sphere_with_texture(
        full_path_input_ply="sphere-rectangles.ply",
        full_path_texture="texture1.png",
        center=(2, 3, 5),
        full_path_output_ply="sphere-with-texture-1.ply",
    )
