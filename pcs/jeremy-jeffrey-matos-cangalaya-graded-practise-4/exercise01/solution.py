import numpy as np
import cv2
import glob


def load_mesh(file_path: str) -> np.ndarray:
    with open(file_path, "r") as file:
        lines = file.readlines()

    if lines[0].strip() != "OFF":
        raise ValueError("The provided file is not in OFF format")

    # Read the number of vertices, faces, and edges
    parts = lines[1].strip().split()
    num_vertices = int(parts[0])

    # Read the vertex data
    vertices = []
    for i in range(2, 2 + num_vertices):
        vertex = list(map(float, lines[i].strip().split()))
        vertices.append(vertex)

    return np.array(vertices)


def project_points(
    full_path_input_mesh: str,
    optical_center_x: float,
    optical_center_y: float,
    optical_center_z: float,
    optical_axis_x: float,
    optical_axis_y: float,
    optical_axis_z: float,
    output_width_in_pixels: int,
    output_height_in_pixels: int,
    full_path_output: str,
) -> None:
    vertices = load_mesh(full_path_input_mesh)

    optical_center = np.array([optical_center_x, optical_center_y, optical_center_z])
    optical_axis = np.array([optical_axis_x, optical_axis_y, optical_axis_z])
    focal_distance = np.linalg.norm(optical_axis)
    optical_axis /= focal_distance

    vertices -= optical_center

    near_plane = 0.1
    far_plane = 1000.0
    field_of_view = np.pi / 4
    aspect_ratio = output_width_in_pixels / output_height_in_pixels

    f = 1 / np.tan(field_of_view / 2)
    projection_matrix = np.array(
        [
            [f / aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [
                0,
                0,
                -(far_plane + near_plane) / (far_plane - near_plane),
                -2 * far_plane * near_plane / (far_plane - near_plane),
            ],
            [0, 0, -1, 0],
        ]
    )

    vertices_homogeneous = np.hstack([vertices, np.ones((vertices.shape[0], 1))])
    projected_vertices = vertices_homogeneous @ projection_matrix.T
    projected_vertices /= projected_vertices[:, 3][:, np.newaxis]

    pixel_coords = np.zeros((vertices.shape[0], 2))
    pixel_coords[:, 0] = output_width_in_pixels / 2 * (1 + projected_vertices[:, 0])
    pixel_coords[:, 1] = output_height_in_pixels / 2 * (1 - projected_vertices[:, 1])

    # Clipping pixel coordinates to ensure they fall within the image dimensions
    pixel_coords[:, 0] = np.clip(pixel_coords[:, 0], 0, output_width_in_pixels - 1)
    pixel_coords[:, 1] = np.clip(pixel_coords[:, 1], 0, output_height_in_pixels - 1)

    output_image = np.zeros((output_height_in_pixels, output_width_in_pixels, 3), dtype=np.uint8)

    # Plotting the points on the image
    for x, y in pixel_coords.astype(int):
        if 0 <= x < output_width_in_pixels and 0 <= y < output_height_in_pixels:
            output_image[int(y), int(x)] = (255, 255, 255)

    cv2.imwrite(full_path_output, output_image)


for idx, path in enumerate(glob.glob('../pc4-example-inputs/meshes-for-exercises-1-2-3/*.off')):
    project_points(
        full_path_input_mesh=path,
        optical_center_x=0.0,
        optical_center_y=10.0,
        optical_center_z=1000.0,
        optical_axis_x=0.0,
        optical_axis_y=0.0,
        optical_axis_z=1.0,
        output_width_in_pixels=1920,
        output_height_in_pixels=1080,
        full_path_output=f'./result_{idx+1}.png',
    )
