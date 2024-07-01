import matplotlib.pyplot as plt
import numpy as np
import copy


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


# Each vertex has its own unique Vertice Edge node
class Vertice_Edge_Node:
    def __init__(self, name, coordinates, incident_edge=None):
        self.vname = name
        self.coordinates = coordinates
        self.incident_edge = incident_edge
        self.Q_error = None

    def __str__(self):
        return f"[vertice: {self.vname},  coordinates: {self.coordinates}, incident: {self.incident_edge} , Q: {self.Q_error}]\n"

    def __repr__(self):
        return f"[vertice: {self.vname},  coordinates: {self.coordinates}, incident: {self.incident_edge} , Q: {self.Q_error}]\n"
    
# Each Face has a unique Face node identified by a  unique name
class Face_Node:
    def __init__(self, name, half_edge):
        self.fname = name
        self.half_edge = half_edge
        self.normal = None

    def __str__(self):
        return f"[face: {self.fname},  half edge: {self.half_edge} , Normal: {self.normal}]\n"

    def __repr__(self):
        return f"[face: {self.fname},  half edge: {self.half_edge} , Normal: {self.normal}]\n"


class Half_Edge_Node:
    def __init__(
        self,
        he_name,
        origin,
        end_vertex=None,
        twin_name=None,
        incident_face=None,
        next=None,
        prev=None,
    ):
        self.he_name = he_name
        self.origin = origin
        self.end_vertex = end_vertex
        self.twin_name = twin_name
        self.incident_face = incident_face
        self.next = next
        self.prev = prev
        self.child_odd_vertex = None

    def __str__(self):
        return f"\n half edge: {self.he_name}, origin vertice: {self.origin}, end vertex: {self.end_vertex}, twin: {self.twin_name}, incident face: {self.incident_face}, next: {self.next}, prev: {self.prev }, mid: {self.child_odd_vertex} |\n"

    def __repr__(self):
        return f"\n half edge: {self.he_name}, origin vertice: {self.origin}, end vertex: {self.end_vertex}, twin: {self.twin_name}, incident face: {self.incident_face}, next: {self.next}, prev: {self.prev }, mid: {self.child_odd_vertex} |\n"


def create_half_edge(mesh, vertices_list, half_edge_list, faces_list):
    for i in range(len(mesh.vertices)):
        vertices_list[f"v{i}"] = Vertice_Edge_Node(
            f"v{i}", np.array(mesh.vertices[i]), None
        )

    # Step 2 & 3: Create half-edges
    edge_count = 0
    for i in range(len(mesh.triangles)):
        triangle = mesh.triangles[i]
        faces_list[f"f{i}"] = Face_Node(f"f{i}", None)

        # print("Triangle:",triangle)

        for j in range(3):
            v_name = None
            for pt in vertices_list:
                # print(vertices_list[pt].coordinates , triangle[j], type(vertices_list[pt].coordinates) ,type(triangle[j]))
                if np.array_equal(vertices_list[pt].coordinates, triangle[j]):
                    v_name = pt
                    break
            if v_name == None:
                print("Vertex not found for coordinates", triangle[j])

            half_edge_list[f"e{edge_count}"] = Half_Edge_Node(f"e{edge_count}", v_name)
            vertices_list[v_name].incident_edge = f"e{edge_count}"
            half_edge_list[f"e{edge_count}"].incident_face = f"f{i}"

            # Assign half edge to a face
            if j == 0:
                faces_list[f"f{i}"].half_edge = f"e{edge_count}"
            if j > 0:
                half_edge_list[f"e{edge_count}"].prev = f"e{edge_count-1}"
                half_edge_list[f"e{edge_count-1}"].next = f"e{edge_count}"
                half_edge_list[f"e{edge_count-1}"].end_vertex = half_edge_list[
                    f"e{edge_count}"
                ].origin
            if j == 2:
                half_edge_list[f"e{edge_count}"].next = f"e{edge_count-2}"
                half_edge_list[f"e{edge_count-2}"].prev = f"e{edge_count}"
                half_edge_list[f"e{edge_count}"].end_vertex = half_edge_list[
                    f"e{edge_count-2}"
                ].origin

            edge_count += 1

    # Step 4: Connect half-edges
    for he_name in half_edge_list:
        if half_edge_list[he_name].twin_name is None:
            for twin_he_name in half_edge_list:
                if (
                    half_edge_list[twin_he_name].origin
                    == half_edge_list[he_name].end_vertex
                    and half_edge_list[twin_he_name].end_vertex
                    == half_edge_list[he_name].origin
                ):
                    half_edge_list[he_name].twin_name = twin_he_name
                    half_edge_list[twin_he_name].twin_name = he_name
                    break


def plot_half_edge(new_half_edge_list, new_vertices_list, deleted_vertices=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Iterate through half edges and plot them
    for e_name in new_half_edge_list:
        org, end = (
            new_half_edge_list[e_name].origin,
            new_half_edge_list[e_name].end_vertex,
        )
        org_coords, end_coords = (
            new_vertices_list[org].coordinates,
            new_vertices_list[end].coordinates,
        )

        # print(f"Org: {org}, End {end}, {org_coords}, {end_coords}")
        ax.plot(
            [org_coords[0], end_coords[0]],
            [org_coords[1], end_coords[1]],
            [org_coords[2], end_coords[2]],
            color="b",
        )

    # Set labels and show plot
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Annotating vertices
    if deleted_vertices is not None:
        for vertex_name in deleted_vertices:
            ax.scatter(
                deleted_vertices[vertex_name].coordinates[0],
                deleted_vertices[vertex_name].coordinates[1],
                deleted_vertices[vertex_name].coordinates[2],
                color="g",
            )
            ax.text(
                deleted_vertices[vertex_name].coordinates[0],
                deleted_vertices[vertex_name].coordinates[1],
                deleted_vertices[vertex_name].coordinates[2],
                vertex_name,
            )

    for vertex_name in new_vertices_list:
        ax.scatter(
            new_vertices_list[vertex_name].coordinates[0],
            new_vertices_list[vertex_name].coordinates[1],
            new_vertices_list[vertex_name].coordinates[2],
            color="r",
        )
        ax.text(
            new_vertices_list[vertex_name].coordinates[0],
            new_vertices_list[vertex_name].coordinates[1],
            new_vertices_list[vertex_name].coordinates[2],
            vertex_name,
        )

    plt.show()


def compute_odd_vertices(
    half_edge_list, vertices_list, new_vertices_list, debug=False
):
    visited = set([])
    for e_name in half_edge_list:
        if e_name not in visited:
            if debug:
                print(e_name, visited)
            twin_e_name = half_edge_list[e_name].twin_name
            visited.add(e_name)
            visited.add(twin_e_name)

            higher_weight_vertex1 = half_edge_list[e_name].origin
            higher_weight_vertex2 = half_edge_list[e_name].end_vertex

            lower_weight_vertex1 = half_edge_list[
                half_edge_list[e_name].next
            ].end_vertex
            lower_weight_vertex2 = half_edge_list[
                half_edge_list[twin_e_name].next
            ].end_vertex

            odd_vertex = 3 / 8 * (
                vertices_list[higher_weight_vertex1].coordinates
                + vertices_list[higher_weight_vertex2].coordinates
            ) + 1 / 8 * (
                vertices_list[lower_weight_vertex1].coordinates
                + vertices_list[lower_weight_vertex2].coordinates
            )

            half_edge_list[e_name].child_odd_vertex = f"v{len(new_vertices_list)}"
            half_edge_list[twin_e_name].child_odd_vertex = f"v{len(new_vertices_list)}"
            new_vertices_list[f"v{len(new_vertices_list)}"] = Vertice_Edge_Node(
                f"v{len(new_vertices_list)}", np.array(odd_vertex)
            )


def compute_even_vertices(
    half_edge_list, vertices_list, new_vertices_list, debug=False
):

    for vertex_name in vertices_list:
        neighbours = set([])
        for he_name in half_edge_list:
            if half_edge_list[he_name].origin == vertex_name:
                neighbours.add(half_edge_list[he_name].end_vertex)
        sum_neighbours = 0
        for neighbour in neighbours:
            sum_neighbours += vertices_list[neighbour].coordinates
        if debug:
            print("Sum neighbours :", sum_neighbours)

        beta = 3 / 16.0
        if len(neighbours) > 3:
            beta = (
                1
                / len(neighbours)
                * (
                    5 / 8.0
                    - (3 / 8.0 + 1 / 4.0 * np.cos(2 * np.pi / len(neighbours))) ** 2
                )
            )
        elif len(neighbours) < 3:
            raise Warning(f"Too few neighbours for {vertex_name} :: {neighbours}")

        new_vertices_list[vertex_name].coordinates = (
            vertices_list[vertex_name].coordinates * (1 - len(neighbours) * beta)
            + sum_neighbours * beta
        )


def create_new_faces(new_face_list, new_half_edge_list, triangle):
    curr_face = f"f{len(new_face_list)}"
    edge_count = len(new_half_edge_list)
    for j in range(3):

        new_half_edge_list[f"e{edge_count}"] = Half_Edge_Node(
            f"e{edge_count}", triangle[j]
        )
        new_half_edge_list[f"e{edge_count}"].incident_face = curr_face

        # Assign half edge to a face
        if j == 0:
            new_face_list[curr_face] = Face_Node(
                curr_face, new_half_edge_list[f"e{edge_count}"]
            )
            new_face_list[curr_face].half_edge = f"e{edge_count}"
        if j > 0:
            new_half_edge_list[f"e{edge_count}"].prev = f"e{edge_count-1}"
            new_half_edge_list[f"e{edge_count-1}"].next = f"e{edge_count}"
            new_half_edge_list[f"e{edge_count-1}"].end_vertex = new_half_edge_list[
                f"e{edge_count}"
            ].origin
        if j == 2:
            new_half_edge_list[f"e{edge_count}"].next = f"e{edge_count-2}"
            new_half_edge_list[f"e{edge_count-2}"].prev = f"e{edge_count}"
            new_half_edge_list[f"e{edge_count}"].end_vertex = new_half_edge_list[
                f"e{edge_count-2}"
            ].origin

        edge_count += 1


def compute_new_faces(
    faces_list,
    half_edge_list,
    new_vertices_list,
    new_half_edge_list,
    new_face_list,
    debug=False,
):

    for f_name in faces_list:
        he_name = faces_list[f_name].half_edge
        prev_he_name = half_edge_list[he_name].prev
        next_he_name = half_edge_list[he_name].next

        origin_vertex1 = half_edge_list[he_name].origin
        end_vertex1 = half_edge_list[he_name].end_vertex
        child_odd_vertex1 = half_edge_list[he_name].child_odd_vertex

        origin_vertex2 = half_edge_list[prev_he_name].origin
        end_vertex2 = half_edge_list[prev_he_name].end_vertex
        child_odd_vertex2 = half_edge_list[prev_he_name].child_odd_vertex

        origin_vertex3 = half_edge_list[next_he_name].origin
        end_vertex3 = half_edge_list[next_he_name].end_vertex
        child_odd_vertex3 = half_edge_list[next_he_name].child_odd_vertex

        if debug:
            print("Creating 4 new faces")
            print([origin_vertex1, child_odd_vertex1, child_odd_vertex2])
            print([origin_vertex2, child_odd_vertex2, child_odd_vertex3])
            print([origin_vertex3, child_odd_vertex3, child_odd_vertex1])
            print([child_odd_vertex1, child_odd_vertex3, child_odd_vertex2])

        create_new_faces(
            new_face_list,
            new_half_edge_list,
            [origin_vertex1, child_odd_vertex1, child_odd_vertex2],
        )
        create_new_faces(
            new_face_list,
            new_half_edge_list,
            [origin_vertex2, child_odd_vertex2, child_odd_vertex3],
        )
        create_new_faces(
            new_face_list,
            new_half_edge_list,
            [origin_vertex3, child_odd_vertex3, child_odd_vertex1],
        )
        create_new_faces(
            new_face_list,
            new_half_edge_list,
            [child_odd_vertex1, child_odd_vertex3, child_odd_vertex2],
        )
        # print(new_face_list)


def connect_twin_half_edges(new_half_edge_list):
    for he_name in new_half_edge_list:
        if new_half_edge_list[he_name].twin_name is None:
            for twin_he_name in new_half_edge_list:
                if (
                    new_half_edge_list[twin_he_name].origin
                    == new_half_edge_list[he_name].end_vertex
                    and new_half_edge_list[twin_he_name].end_vertex
                    == new_half_edge_list[he_name].origin
                ):
                    new_half_edge_list[he_name].twin_name = twin_he_name
                    new_half_edge_list[twin_he_name].twin_name = he_name
                    break


def subdivision_loop(
    mesh, vertices_list, half_edge_list, faces_list, iterations=1, debug=True
):
    """
    Apply Loop subdivision to the input mesh for the specified number of iterations.
    :param mesh: input mesh
    :param iterations: number of iterations
    :return: mesh after subdivision
    """
    new_vertices_list = copy.deepcopy(vertices_list)
    new_half_edge_list = {}
    new_face_list = {}
    for _ in range(iterations):
        new_half_edge_list = {}
        new_face_list = {}
        # new_half_edge_list= copy.deepcopy(half_edge_list)
        new_vertices_list = copy.deepcopy(vertices_list)
        # print(f"Iteration {iter}")
        # print(half_edge_list)

        compute_odd_vertices(
            half_edge_list=half_edge_list,
            vertices_list=vertices_list,
            new_vertices_list=new_vertices_list,
        )

        compute_even_vertices(
            half_edge_list=half_edge_list,
            vertices_list=vertices_list,
            new_vertices_list=new_vertices_list,
        )

        compute_new_faces(
            faces_list,
            half_edge_list,
            new_vertices_list,
            new_half_edge_list,
            new_face_list,
        )

        connect_twin_half_edges(new_half_edge_list=new_half_edge_list)

        half_edge_list = copy.deepcopy(new_half_edge_list)
        faces_list = copy.deepcopy(new_face_list)
        vertices_list = copy.deepcopy(new_vertices_list)

        # print(f"End of iteration {iter}")
        # print("\n Half Edge List ::\n", half_edge_list)
        # print(" \n Faces List : \n ", faces_list)
        # print("\n Vertices List \n", vertices_list)

    # print(len(new_half_edge_list), len(new_vertices_list), len(new_face_list))
    # plot_half_edge(new_half_edge_list, new_vertices_list)

    return new_half_edge_list, new_vertices_list, new_face_list


class Mesh:
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self.triangles = [
            [vertices[face[0]], vertices[face[1]], vertices[face[2]]]
            for face in faces
        ]


def loop(full_path_input_mesh, number_of_iterations, full_path_output_mesh):
    vertices, faces = [], []
    if full_path_input_mesh.endswith(".off"):
        vertices, faces = read_off(full_path_input_mesh)
    elif full_path_input_mesh.endswith(".ply"):
        vertices, faces = read_ply(full_path_input_mesh)
    else:
        raise ValueError("Only OFF and PLY files are supported.")

    vertices, faces = np.array(vertices), np.array(faces)
    
    mesh = Mesh(vertices, faces)
    # print(mesh.vertices)
    # print(mesh.faces)
    vertices_list, half_edge_list, faces_list = {}, {}, {}
    create_half_edge(
        mesh=mesh,
        vertices_list=vertices_list,
        half_edge_list=half_edge_list,
        faces_list=faces_list,
    )

    new_half_edge_list, new_vertices_list, new_face_list = subdivision_loop(
        mesh, vertices_list, half_edge_list, faces_list, iterations=number_of_iterations
    )

    # print(new_vertices_list)
    new_vertices = [new_vertices_list[v].coordinates for v in new_vertices_list]
    # print(new_vertices)
    # print(new_half_edge_list)
    # print(new_face_list)

    new_faces = []
    for face in new_face_list:
        face_obj = new_face_list[face]
        he_name = face_obj.half_edge
        he = new_half_edge_list[he_name]
        # print(face_obj.fname, he_name)

        face_vertices = []
        for _ in range(3):
            face_vertices.append(int(he.origin.replace("v", "")))
            he = new_half_edge_list[he.next]
        new_faces.append(face_vertices)
    # print(new_faces)

    if full_path_output_mesh.endswith(".off"):
        create_off(full_path_output_mesh, new_vertices, new_faces)
    elif full_path_output_mesh.endswith(".ply"):
        create_ply(full_path_output_mesh, new_vertices, new_faces)
    

if __name__ == "__main__":
    loop(
        full_path_input_mesh="./cube_triangular_off.off",
        number_of_iterations=3,
        full_path_output_mesh="loop-from-cube-3-iterations.off",
    )