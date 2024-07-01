import numpy as np
import copy

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


def read_off(input_file: str):
    vertices = []
    faces = []
    vertex_count = 0
    face_count = 0
    
    with open(input_file, mode='r') as file:
        line = file.readline().strip()
        if not line.startswith('OFF'):
            raise ValueError('The file does not start with "OFF". It is not a valid OFF file.')

        line = file.readline().strip()
        parts = line.split()
        if len(parts) != 3:
            raise ValueError('The second line should contain three integers: number of vertices, number of faces, and number of edges.')
        
        try:
            vertex_count = int(parts[0])
            face_count = int(parts[1])
            edge_count = int(parts[2])  # Although edges count is typically not used in reading OFF files
        except ValueError:
            raise ValueError('Invalid header format. Expected three integers after "OFF".')

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
            face = face_data[1:]  # Assuming first number is the number of vertices per face (which is typically 3)
            faces.append(face)
    
    assert len(vertices) == vertex_count, f"Expected {vertex_count} vertices, but got {len(vertices)}"
    assert len(faces) == face_count, f"Expected {face_count} faces, but got {len(faces)}"
    
    return vertices, faces


def create_ply(output_file: str, vertices: list, faces: list):
    with open(output_file, mode='w') as file:
        file.write('ply\n')
        file.write('format ascii 1.0\n')
        file.write(f'element vertex {len(vertices)}\n')
        file.write('property float x\n')
        file.write('property float y\n')
        file.write('property float z\n')

        color = len(vertices[0]) == 8        
        if color:
            file.write('property float u\n')  # Coordenada de textura u
            file.write('property float v\n')  # Coordenada de textura v
            file.write('property uchar red\n')
            file.write('property uchar green\n')
            file.write('property uchar blue\n')
        
        file.write(f'element face {len(faces)}\n')
        file.write('property list uchar int vertex_indices\n')
        file.write('end_header\n')

        for v in vertices:
            if color:
                file.write(f'{v[0]} {v[1]} {v[2]} {v[3]} {v[4]} {v[5]} {v[6]} {v[7]}\n')
            else:
                file.write(f'{v[0]} {v[1]} {v[2]}\n')
        
        for face in faces:
            if all(0 <= index < len(vertices) for index in face):
                file.write(f'{len(face)} {" ".join(map(str, face))}\n')
            else:
                print(f"Bad vertex index in face: {face}")  # Depuración
                raise ValueError("Bad vertex index in face: some indices refer to non-existent vertices.")


def create_off(output_file: str, vertices: list, faces: list):
    with open(output_file, mode='w') as file:
        if len(vertices[0]) > 3:
            file.write('COFF\n')
        else:
            file.write('OFF\n')
        file.write(f'{len(vertices)} {len(faces)} 0\n')  # Escribir el encabezado

        for v in vertices:
            if len(v) == 3:  # Vértices sin color
                file.write(f'{v[0]} {v[1]} {v[2]}\n')
            else:  # Vértices con color RGB
                try:
                    file.write(f'{v[0]} {v[1]} {v[2]} {v[-3]/255} {v[-2]/255} {v[-1]/255}\n')
                except IndexError:
                    raise ValueError(f"Invalid vertex format: {v}")

        for face in faces:
            if all(0 <= index < len(vertices) for index in face):
                file.write(f'{len(face)} {" ".join(map(str, face))}\n')
            else:
                print(f"Bad vertex index in face: {face}")  # Depuración
                raise ValueError("Bad vertex index in face: some indices refer to non-existent vertices.")


def translate_mesh(
    full_path_input_mesh: str,
    d: tuple, ## d has the format (d_x, d_y, d_z)
    full_path_output_mesh: str,
):
    vertices, faces = [], []
    if full_path_input_mesh.endswith(".off"):
        vertices, faces = read_off(full_path_input_mesh)
    elif full_path_input_mesh.endswith(".ply"):
        vertices, faces = read_ply(full_path_input_mesh)
    else:
        raise ValueError("Only OFF and PLY files are supported.")
    
    d_x, d_y, d_z = d
    translated_vertices = copy.deepcopy(vertices)

    for vertex in translated_vertices:
        vertex[0] += d_x
        vertex[1] += d_y
        vertex[2] += d_z

    if full_path_output_mesh.endswith(".off"):
        create_off(full_path_output_mesh, translated_vertices, faces)
    elif full_path_output_mesh.endswith(".ply"):
        create_ply(full_path_output_mesh, translated_vertices, faces)


if __name__ == "__main__":
    translate_mesh(
        full_path_input_mesh="sphere-rectangles-nocolor.off",
        d=(10, 20, 30),
        full_path_output_mesh="sphere-rectangles-translated-pos.off",
    )
    translate_mesh(
        full_path_input_mesh="sphere-rectangles-nocolor.off",
        d=(-10, -20, -30),
        full_path_output_mesh="sphere-rectangles-translated-neg.off",
    )
