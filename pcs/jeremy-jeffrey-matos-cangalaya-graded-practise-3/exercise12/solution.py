import numpy as np
import matplotlib.pyplot as plt

def read_ply(input_file: str):
    vertices = []
    faces = []
    vertex_count = 0
    face_count = 0

    with open(input_file, mode="r") as file:
        line = file.readline().strip()
        if line != "ply":
            raise ValueError(
                'The file does not start with "ply". It is not a valid PLY file.'
            )

        line = file.readline().strip()
        if line != "format ascii 1.0":
            raise ValueError("Only ASCII format PLY files are supported.")

        line = file.readline().strip()
        while line != "end_header":
            if line.startswith("element vertex"):
                vertex_count = int(line.split()[-1])
            elif line.startswith("element face"):
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

    assert (
        len(vertices) == vertex_count
    ), f"Expected {vertex_count} vertices, but got {len(vertices)}"
    assert (
        len(faces) == face_count
    ), f"Expected {face_count} faces, but got {len(faces)}"

    return vertices, faces


def read_off(input_file: str):
    vertices = []
    faces = []
    vertex_count = 0
    face_count = 0

    with open(input_file, mode="r") as file:
        line = file.readline().strip()
        if not line.startswith("OFF"):
            raise ValueError(
                'The file does not start with "OFF". It is not a valid OFF file.'
            )

        line = file.readline().strip()
        parts = line.split()
        if len(parts) != 3:
            raise ValueError(
                "The second line should contain three integers: number of vertices, number of faces, and number of edges."
            )

        try:
            vertex_count = int(parts[0])
            face_count = int(parts[1])
            edge_count = int(
                parts[2]
            )  # Although edges count is typically not used in reading OFF files
        except ValueError:
            raise ValueError(
                'Invalid header format. Expected three integers after "OFF".'
            )

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
            face = face_data[
                1:
            ]  # Assuming first number is the number of vertices per face (which is typically 3)
            faces.append(face)

    assert (
        len(vertices) == vertex_count
    ), f"Expected {vertex_count} vertices, but got {len(vertices)}"
    assert (
        len(faces) == face_count
    ), f"Expected {face_count} faces, but got {len(faces)}"

    return vertices, faces


def create_ply(output_file: str, vertices: list, faces: list):
    with open(output_file, mode="w") as file:
        file.write("ply\n")
        file.write("format ascii 1.0\n")
        file.write(f"element vertex {len(vertices)}\n")
        file.write("property float x\n")
        file.write("property float y\n")
        file.write("property float z\n")

        color = len(vertices[0]) == 8
        if color:
            file.write("property float u\n")  # Coordenada de textura u
            file.write("property float v\n")  # Coordenada de textura v
            file.write("property uchar red\n")
            file.write("property uchar green\n")
            file.write("property uchar blue\n")

        file.write(f"element face {len(faces)}\n")
        file.write("property list uchar int vertex_indices\n")
        file.write("end_header\n")

        for v in vertices:
            if color:
                file.write(f"{v[0]} {v[1]} {v[2]} {v[3]} {v[4]} {v[5]} {v[6]} {v[7]}\n")
            else:
                file.write(f"{v[0]} {v[1]} {v[2]}\n")

        for face in faces:
            if all(0 <= index < len(vertices) for index in face):
                file.write(f'{len(face)} {" ".join(map(str, face))}\n')
            else:
                print(f"Bad vertex index in face: {face}")  # Depuración
                raise ValueError(
                    "Bad vertex index in face: some indices refer to non-existent vertices."
                )


def create_off(output_file: str, vertices: list, faces: list):
    with open(output_file, mode="w") as file:
        if len(vertices[0]) > 3:
            file.write("COFF\n")
        else:
            file.write("OFF\n")
        file.write(f"{len(vertices)} {len(faces)} 0\n")  # Escribir el encabezado

        for v in vertices:
            if len(v) == 3:  # Vértices sin color
                file.write(f"{v[0]} {v[1]} {v[2]}\n")
            else:  # Vértices con color RGB
                try:
                    file.write(
                        f"{v[0]} {v[1]} {v[2]} {v[-3]/255} {v[-2]/255} {v[-1]/255}\n"
                    )
                except IndexError:
                    raise ValueError(f"Invalid vertex format: {v}")

        for face in faces:
            if all(0 <= index < len(vertices) for index in face):
                file.write(f'{len(face)} {" ".join(map(str, face))}\n')
            else:
                print(f"Bad vertex index in face: {face}")  # Depuración
                raise ValueError(
                    "Bad vertex index in face: some indices refer to non-existent vertices."
                )


def euclidean(a: np.ndarray, b: np.ndarray) -> float:
    return np.linalg.norm(a - b)


def painter_algorithm_simple_cosine_illumination(
    full_path_input_mesh: str,
    full_path_output_image: str,
    min_x_coordinate_in_projection_plane: float,
    min_y_coordinate_in_projection_plane: float,
    max_x_coordinate_in_projection_plane: float,
    max_y_coordinate_in_projection_plane: float,
    width_in_pixels: int,
    height_in_pixels: int,
):
    focus = [0, 0, 0]
    vertices, faces = [], []
    if full_path_input_mesh.endswith(".off"):
        vertices, faces = read_off(full_path_input_mesh)
    elif full_path_input_mesh.endswith(".ply"):
        vertices, faces = read_ply(full_path_input_mesh)
    else:
        raise ValueError("Only OFF and PLY files are supported.")
    vertices, faces = np.array(vertices), np.array(faces)

    def max_triangle_distance(focus: tuple, faces: tuple) -> float:
        return max([euclidean(focus, vertices[face]) for face in faces])

    def get_normal_vector_of_face(face: tuple) -> np.ndarray:
        normal_vector = np.cross(vertices[face[1]] - vertices[face[0]],
                                vertices[face[2]] - vertices[face[0]])
        norm = np.linalg.norm(normal_vector)
        if norm == 0:
            return np.zeros_like(normal_vector)
        return normal_vector / norm

    sort_faces = \
        sorted(faces, key=lambda face: max_triangle_distance(focus, face), reverse=True)
    normal_vector_of_sort_faces = \
        [get_normal_vector_of_face(face) for face in sort_faces]

    angle_of_sort_faces = [tup[2] for tup in normal_vector_of_sort_faces]
    
    color_of_sort_faces = \
        [np.array([255, 255, 255]) * cos_angle if cos_angle > 0 else [-1, -1, -1]
        for cos_angle in angle_of_sort_faces]

    normalized_vertices_by_z = [vertex/vertex[2] if vertex[2] != 0 else vertex for vertex in vertices]

    my_dpi = 100
    plt.figure(figsize=(width_in_pixels/my_dpi, height_in_pixels/my_dpi))
    plt.xlim(min_x_coordinate_in_projection_plane, max_x_coordinate_in_projection_plane)
    plt.ylim(min_y_coordinate_in_projection_plane, max_y_coordinate_in_projection_plane)
    
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
                    # edgecolor='red',
                    # linewidth=0.25
                    )
    plt.axis('off')
    plt.savefig(full_path_output_image, dpi=my_dpi)
    plt.show()

if __name__ == "__main__":
    painter_algorithm_simple_cosine_illumination(
        full_path_input_mesh="./sphere-triangles_big.off",
        full_path_output_image="./photo-of-sphere.png",
        min_x_coordinate_in_projection_plane=-1.0,
        min_y_coordinate_in_projection_plane=-1.0,
        max_x_coordinate_in_projection_plane=1.0,
        max_y_coordinate_in_projection_plane=1.0,
        width_in_pixels=640,
        height_in_pixels=480,
    )
