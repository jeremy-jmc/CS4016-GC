import numpy as np

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


def rotate_mesh_around_line(
    full_path_input_mesh: str,
    axis_of_rotation: tuple,
    # Has the structure ((p_x, p_y, p_z), (d_x, d_y, d_z))
    # where (p_x, p_y, p_z) is a point and
    # (d_x, d_y, d_z) is a direction
    alpha: float,  ## number of degrees that we want to rotate the vertices
    full_path_output_mesh: str,
):
    vertices, faces = [], []
    if full_path_input_mesh.endswith(".off"):
        vertices, faces = read_off(full_path_input_mesh)
    elif full_path_input_mesh.endswith(".ply"):
        vertices, faces = read_ply(full_path_input_mesh)
    else:
        raise ValueError("Only OFF and PLY files are supported.")
    
    
    vertices_np = np.array(vertices)
    vertices_np, color = (vertices_np[:, :3], vertices_np[:, 3:]) if len(vertices[0]) > 3 else (vertices_np, None)

    p, d = axis_of_rotation
    p = np.array(p)
    d = np.array(d)
    d = d/ np.linalg.norm(d)
    
    alpha_rad = np.deg2rad(alpha)

    d_x, d_y, d_z = d

    # Matriz de rotación para rotar alpha radianes alrededor del vector d
    rotation_matrix = np.array([
        [np.cos(alpha_rad) + d_x**2 * (1 - np.cos(alpha_rad)), 
         d_x * d_y * (1 - np.cos(alpha_rad)) - d_z * np.sin(alpha_rad), 
         d_x * d_z * (1 - np.cos(alpha_rad)) + d_y * np.sin(alpha_rad)],
        [d_y * d_x * (1 - np.cos(alpha_rad)) + d_z * np.sin(alpha_rad), 
         np.cos(alpha_rad) + d_y**2 * (1 - np.cos(alpha_rad)), 
         d_y * d_z * (1 - np.cos(alpha_rad)) - d_x * np.sin(alpha_rad)],
        [d_z * d_x * (1 - np.cos(alpha_rad)) - d_y * np.sin(alpha_rad), 
         d_z * d_y * (1 - np.cos(alpha_rad)) + d_x * np.sin(alpha_rad), 
         np.cos(alpha_rad) + d_z**2 * (1 - np.cos(alpha_rad))]
    ])

    # Aplicar la rotación a los vértices
    rotated_vertices_np = np.dot(vertices_np - p, rotation_matrix.T) + p

    rotated_vertices = rotated_vertices_np.tolist()
    if color is not None:
        rotated_vertices = [v + list(c) for v, c in zip(rotated_vertices, color)]
    
    if full_path_output_mesh.endswith(".off"):
        create_off(full_path_output_mesh, rotated_vertices, faces)
    elif full_path_output_mesh.endswith(".ply"):
        create_ply(full_path_output_mesh, rotated_vertices, faces)


if __name__ == "__main__":
    angle = 60
    rotate_mesh_around_line(
        full_path_input_mesh="sphere-rectangles-nocolor.off",
        axis_of_rotation=((0, 0, 0), (0, 0, 1)),
        alpha=angle,
        full_path_output_mesh=f"sphere-rectangles-rotated-{angle}.off",
    )

    angle = 90
    rotate_mesh_around_line(
        full_path_input_mesh="sphere-rectangles-nocolor.ply",
        axis_of_rotation=((0, 0, 0), (0, 0, 1)),
        alpha=angle,
        full_path_output_mesh=f"sphere-rectangles-rotated-{angle}.off",
    )

    rotate_mesh_around_line(
        full_path_input_mesh="sphere-with-texture-1.ply",
        axis_of_rotation=((0, 0, 0), (0, 0, 1)),
        alpha=angle,
        full_path_output_mesh=f"sphere-rectangles-rotated-{angle}-texture.off",
    )

