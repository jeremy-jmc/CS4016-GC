import numpy as np
import matplotlib.pyplot as plt
import json
import math

"""
https://paulbourke.net/geometry/polygonise/
https://www.youtube.com/watch?v=5g7sL1RUu1I
Step 2:
    Classifiy each voxel according to whether it lies:
        - Outside the surface: value > isosurface value
        - Inside the surface: value <= isosurface value
Step 3:
    Use the binary labelling of each voxel vertex to create an index
Step 4:
    For a given index, access an array storing a list of edges
    All 256 cases can be derived from 1 + 14 = 15 base cases due to symmetries

    Get a edge list from lookup (case) table
        Decompose the case as a set of triangles
Step 5: 
    For each triangle edge, find the vertex location along the edge using the linear interpolation of the voxel values
Step 6:
    Calculate the normal at each cube vertex (central differences)
    Use linear interpolation to compute the polygon vertex normal (off the isosurface)
Step 7:
    Consider ambiguous cases
        - Ambiguous cases: 3, 6, 7, 10, 12, 13
        - Adjacent vertices: different states
        - Diagaonal vertices: same state
        - Resolution: choose one case (the right one)
"""


CASES = json.load(open("./cases.json", "r"))
# print(CASES)

N_SAMPLING = 1000000


class Mesh:
    # TODO: Refactor this class as a set of functions
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.index: int = 0

    def add_triangle(self, pol) -> None:
        for v in pol:
            t: tuple[float, float, float] = (v[0], v[1], v[2])
            self.vertices.append(t)

        self.index += 3
        self.faces.append([self.index - 3, self.index - 1, self.index - 2])

    def create_off(self, output_file: str) -> None:
        file = open(output_file, mode="w")
        file.write("OFF\n")
        file.write(f"{len(self.vertices)} {len(self.faces)} {len(self.vertices)}\n\n")

        for v in self.vertices:
            for p in v:
                file.write(f"{p} ")
            file.write("\n")
        file.write("\n")

        for face in self.faces:
            file.write(f"{len(face)} ")
            for i in face:
                file.write(f"{i} ")
            file.write("\n")
        file.close()


GLOBAL_MESH = Mesh()


def dist(p1: np.ndarray, p2: np.ndarray) -> float:
    return math.sqrt(
        pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2) + pow(p1[2] - p2[2], 2)
    )


def generate_random_points(
    n: int, x_range: tuple, y_range: tuple, z_range: tuple
) -> np.ndarray:
    x_points = np.random.uniform(x_range[0], x_range[1], n)
    y_points = np.random.uniform(y_range[0], y_range[1], n)
    z_points = np.random.uniform(z_range[0], z_range[1], n)

    return np.column_stack((x_points, y_points, z_points))


def divide_cube(cube_box: tuple) -> list:
    min_point, max_point = cube_box
    mid_point = (min_point + max_point) / 2

    new_cubes = [
        (min_point, mid_point),
        (
            np.array([mid_point[0], min_point[1], min_point[2]]),
            np.array([max_point[0], mid_point[1], mid_point[2]]),
        ),
        (
            np.array([min_point[0], mid_point[1], min_point[2]]),
            np.array([mid_point[0], max_point[1], mid_point[2]]),
        ),
        (
            np.array([mid_point[0], mid_point[1], min_point[2]]),
            np.array([max_point[0], max_point[1], mid_point[2]]),
        ),
        (
            np.array([min_point[0], min_point[1], mid_point[2]]),
            np.array([mid_point[0], mid_point[1], max_point[2]]),
        ),
        (
            np.array([mid_point[0], min_point[1], mid_point[2]]),
            np.array([max_point[0], mid_point[1], max_point[2]]),
        ),
        (
            np.array([min_point[0], mid_point[1], mid_point[2]]),
            np.array([mid_point[0], max_point[1], max_point[2]]),
        ),
        (mid_point, max_point),
    ]
    return new_cubes


def get_vertexes_from_cube_box(cube_box: tuple) -> np.ndarray:
    min_point, max_point = cube_box
    x_min, y_min, z_min = min_point
    x_max, y_max, z_max = max_point

    return np.array(
        [
            [x_min, y_min, z_min],
            [x_max, y_min, z_min],
            [x_max, y_max, z_min],
            [x_min, y_max, z_min],
            [x_min, y_min, z_max],
            [x_max, y_min, z_max],
            [x_max, y_max, z_max],
            [x_min, y_max, z_max],
        ]
    )


def get_edges_from_cube_box(cube_box: tuple) -> list:
    edge_idx = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    ]
    vertexes = get_vertexes_from_cube_box(cube_box)
    return [(vertexes[i], vertexes[j]) for i, j in edge_idx]


def add_surface(f, cube_box):
    global GLOBAL_MESH, CASES
    vertexes = get_vertexes_from_cube_box(cube_box)

    result = f(vertexes[:, 0], vertexes[:, 1], vertexes[:, 2])
    case = 0
    for i, val in enumerate(result):
        if val > 0:
            case += pow(2, i)

    edges = get_edges_from_cube_box(cube_box)
    fig_case = CASES[case]

    for edge_idx in fig_case:
        ed_1, ed_2, ed_3 = edges[edge_idx[0]], edges[edge_idx[1]], edges[edge_idx[2]]
        v_1 = (ed_1[0] + ed_1[1]) / 2
        v_2 = (ed_2[0] + ed_2[1]) / 2
        v_3 = (ed_3[0] + ed_3[1]) / 2

        GLOBAL_MESH.add_triangle([v_1, v_2, v_3])


def marching_cubes_compute(f, cube_box: tuple, precision: float = 0.025, n_sampling = N_SAMPLING, depth: int = 0):
    if depth == 0:
        global GLOBAL_MESH
        GLOBAL_MESH = Mesh()

    min_point, max_point = cube_box
    x_min, y_min, z_min = min_point
    x_max, y_max, z_max = max_point

    p_sampling = np.vstack(
        [
            generate_random_points(
                n_sampling, (x_min, x_max), (y_min, y_max), (z_min, z_max)
            ),
            get_vertexes_from_cube_box(cube_box),
        ]
    )
    eval_points = f(p_sampling[:, 0], p_sampling[:, 1], p_sampling[:, 2])
    
    # * contar (+) (-) (0)
    n_positives = len(eval_points[eval_points > 0])  # outside: todos -> afuera
    n_negatives = len(eval_points[eval_points < 0])  # inside: todos -> adentro
    n_zeros = len(eval_points[eval_points == 0])  # border
    
    if n_zeros == 0:
        if n_negatives > 0 and n_positives == 0:
            # cubo esta totalmente adentro
            return
        if n_positives > 0 and n_negatives == 0:
            # cubo esta totalmente afuera
            return

    if (
        x_max - x_min < precision
        and y_max - y_min < precision
        and z_max - z_min < precision
    ):
        add_surface(f, cube_box)
        return

    for each_cube in divide_cube(cube_box):
        marching_cubes_compute(f, each_cube, precision, min(n_sampling // 8, 100), depth + 1)


def eval_obj(json_obj: dict, x, y, z) -> np.ndarray:
    if json_obj["op"] == "union":
        # result_childs = np.array([eval_obj(child, x, y) for child in json_obj['childs']])

        result_childs = []
        for child in json_obj["childs"]:
            result_childs.append(eval_obj(child, x, y, z))

        n_neg = np.sum(np.array(result_childs) < 0, axis=0)
        n_zeros = np.sum(np.array(result_childs) == 0, axis=0)
        result = np.where(n_neg > 0, -1, np.where(n_zeros > 0, 0, 1))

        return result
    elif json_obj["op"] == "intersection":
        # TODO: implementar
        pass
    elif json_obj["op"] == "":
        return json_obj["function"](x=x, y=y, z=z)


def transform_functions_to_lambdas(node):
    if "function" in node and node["function"]:
        node["function"] = eval(f"lambda x, y, z: {node['function'].replace('^', '**')}")
    if "childs" in node and node["childs"]:
        for child in node["childs"]:
            transform_functions_to_lambdas(child)


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------

# # Plot random points
# from mpl_toolkits.mplot3d import Axes3D
# %matplotlib widget

# points = generate_random_points(N_SAMPLING, (0, 10), (0, 10), (0, 10))
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(points[:, 0], points[:, 1], points[:, 2])
# ax.grid(False)
# plt.show()


# scene = {'op': '', 'function': 'x**2 + 2*y**2 + z**2 - 5'}

scene = {
    "op": "union",
    "function": "",
    "childs": [
        {"op": "", "function": "x**2 + 3*y**2 + z**2 - 5", "childs": []},
        {"op": "", "function": "x**2 + 0.5*y**2 + 4*z**2 - 5", "childs": []},
    ],
}


scene = {
    "op": "union",
    "function": "",
    "childs": [
        {
            "op": "union",
            "function": "",
            "childs": [
                {
                    "op": "union",
                    "function": "",
                    "childs": [
                        {
                            "op": "",
                            "function": "x**2 + y**2 + z**2 - 2 ** 1",
                            "childs": [],
                        },
                        {
                            "op": "",
                            "function": "(x-2)**2 + (y-2)**2 + (z-2)**2 - 2 ** 2",
                            "childs": [],
                        },
                    ]
                },
            ]
        },
        {
            "op": "union",
            "function": "",
            "childs": [
                {
                    "op": "",
                    "function": "(x+10)**2 + (y+10)**2 + (z+10)**2 - 3 ** 2",
                    "childs": [],
                },
                {
                    "op": "",
                    "function": "(x+15)**2 + (y+15)**2 + (z+15)**2 - 6 ** 2",
                    "childs": [],
                }
            ]
        }
    ]
}

# transform_functions_to_lambdas(scene)
# print(scene)


def f_json(x, y, z) -> int:
    return eval_obj(scene, x, y, z)


# marching_cubes_compute(f_json, (np.array([-10, -10, -10]), np.array([10, 10, 10])), 0.05)
# GLOBAL_MESH.create_off('./output.off')


# -----------------------------------------------------------------------------
# Biagioli's tests
# -----------------------------------------------------------------------------


def marching_cubes(
    json_object_describing_surface,
    output_filename,
    x_min,
    y_min,
    x_max,
    y_max,
    z_min,
    z_max,
    precision,
):
    transform_functions_to_lambdas(json_object_describing_surface)
    def json_func(x, y, z) -> int:
        return eval_obj(json_object_describing_surface, x, y, z)

    marching_cubes_compute(
        json_func,
        (np.array([x_min, y_min, z_min]), np.array([x_max, y_max, z_max])),
        precision,
    )

    # TODO: handle PLY file
    GLOBAL_MESH.create_off(output_filename)


example_json = scene

# import cProfile
# cProfile.run('marching_cubes(example_json, "./example-marching-ga.off", -100, -100, 100, 100, -100, 100, 0.1)', sort='cumtime')


# marching_cubes(
#     example_json, "./example-marching-ga.off", 
#     -100, -100, 100, 100, -100, 100, 0.1
# )

# ! WARNING: order of the arguments
marching_cubes(
    # sphere of radius 1 centered at (2, 2, 2)
    {"op": "", "function": "(x-2)^2+(y-2)^2+(z-2)^2-1", "childs": []},
    "./example-marching-cubes_2.off",
    -5, -5, 10, 10, -5, 10, 0.1
)

marching_cubes(
    {
        "op": "union",
        "function": "",
        "childs": [
            {"op": "", "function": "(x-2)^2+(y-2)^2+(z-2)^2-1", "childs": []},
            {"op": "", "function": "(x-4)^2+(y-2)^2+(z-2)^2-1", "childs": []},
        ],
    },
    "./example-marching-cubes_3.off",
    -5, -5, 10, 10, -5, 10, 0.1
)
