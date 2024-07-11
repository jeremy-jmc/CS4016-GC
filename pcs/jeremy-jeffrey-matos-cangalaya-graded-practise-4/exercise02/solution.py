import numpy as np
import cv2
import glob


def load_mesh(file_path: str) -> np.ndarray:
    with open(file_path, "r") as file:
        lines = file.readlines()

    if "OFF" not in lines[0].strip():
        raise ValueError("The provided file is not in OFF format")

    # Read the number of vertices, faces, and edges
    parts = lines[1].strip().split()
    num_vertices = int(parts[0])

    # Read the vertex data
    vertices = []
    for i in range(2, 2 + num_vertices):
        try:
            vertex = list(map(float, lines[i].strip().split()[:3]))
            vertices.append(vertex)
        except:
            continue
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

    optical_center = np.array(
        [optical_center_x, optical_center_y, optical_center_z])
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

    vertices_homogeneous = np.hstack(
        [vertices, np.ones((vertices.shape[0], 1))])
    projected_vertices = vertices_homogeneous @ projection_matrix.T
    projected_vertices /= projected_vertices[:, 3][:, np.newaxis]

    pixel_coords = np.zeros((vertices.shape[0], 2))
    pixel_coords[:, 0] = output_width_in_pixels / \
        2 * (1 + projected_vertices[:, 0])
    pixel_coords[:, 1] = output_height_in_pixels / \
        2 * (1 - projected_vertices[:, 1])

    # Clipping pixel coordinates to ensure they fall within the image dimensions
    pixel_coords[:, 0] = np.clip(
        pixel_coords[:, 0], 0, output_width_in_pixels - 1)
    pixel_coords[:, 1] = np.clip(
        pixel_coords[:, 1], 0, output_height_in_pixels - 1)

    output_image = np.zeros(
        (output_height_in_pixels, output_width_in_pixels, 3), dtype=np.uint8)

    # Plotting the points on the image
    for x, y in pixel_coords.astype(int):
        if 0 <= x < output_width_in_pixels and 0 <= y < output_height_in_pixels:
            output_image[int(y), int(x)] = (255, 255, 255)

    cv2.imwrite(full_path_output, output_image)


#  Implement the function
#  that uses the previous exercise to take a sequence of photos of the vertices present
#  in the mesh described in full_path_input_mesh. Everything is exactly the same
#  as in the previous exercise, but the parameters enclosed by square brackets are lists.
#  The assumptions made in this exercise are the same as the ones made in the previ
# ous exercise. The les produced as output must be {prefix_output_files}-1.png,
#  {prefix_output_files}-2.png, ...

def sequence_of_projections(
        full_path_input_mesh: str,
        optical_center_x: list,
        optical_center_y: list,
        optical_center_z: list,
        optical_axis_x: list,
        optical_axis_y: list,
        optical_axis_z: list,
        output_width_in_pixels: int,
        output_height_in_pixels: int,
        prefix_output_files: str,
):
    vertices = load_mesh(full_path_input_mesh)

    for idx, (oc_x, oc_y, oc_z, oa_x, oa_y, oa_z) in enumerate(
            zip(optical_center_x, optical_center_y, optical_center_z, optical_axis_x, optical_axis_y, optical_axis_z)):
        optical_center = np.array([oc_x, oc_y, oc_z])
        optical_axis = np.array([oa_x, oa_y, oa_z])
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

        vertices_homogeneous = np.hstack(
            [vertices, np.ones((vertices.shape[0], 1))])
        projected_vertices = vertices_homogeneous @ projection_matrix.T
        projected_vertices /= projected_vertices[:, 3][:, np.newaxis]

        pixel_coords = np.zeros((vertices.shape[0], 2))
        pixel_coords[:, 0] = output_width_in_pixels / \
            2 * (1 + projected_vertices[:, 0])
        pixel_coords[:, 1] = output_height_in_pixels / \
            2 * (1 - projected_vertices[:, 1])

        # Clipping pixel coordinates to ensure they fall within the image dimensions
        pixel_coords[:, 0] = np.clip(
            pixel_coords[:, 0], 0, output_width_in_pixels - 1)
        pixel_coords[:, 1] = np.clip(
            pixel_coords[:, 1], 0, output_height_in_pixels - 1)

        output_image = np.zeros(
            (output_height_in_pixels, output_width_in_pixels, 3), dtype=np.uint8)

        # Plotting the points on the image
        for x, y in pixel_coords.astype(int):
            if 0 <= x < output_width_in_pixels and 0 <= y < output_height_in_pixels:
                output_image[int(y), int(x)] = (255, 255, 255)

        cv2.imwrite(f'{prefix_output_files}-{idx+1}.png', output_image)


if __name__ == "__main__":
    optical = [1000, 1, 20, 2, 8, 8]
    for idx, path in enumerate(glob.glob('../../pc4-example-inputs/meshes-for-exercises-1-2-3/*.off')):
        try:
            print(path)
            filename = path.split('/')[-1].split('.')[0][27:]
            center_x = [4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0]
            center_y = [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]
            # center_z = [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]
            center_z = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
            axis_x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            axis_y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            axis_z = [-1.0, -1.0, -1.0, -1.0, -
                      1.0, -1.0, -1.0, -1.0, -1.0, -1.0]
            sequence_of_projections(
                full_path_input_mesh=path,
                optical_center_x=center_x,
                optical_center_y=center_y,
                optical_center_z=center_z,
                optical_axis_x=axis_x,
                optical_axis_y=axis_y,
                optical_axis_z=axis_z,
                output_width_in_pixels=1920,
                output_height_in_pixels=1080,
                prefix_output_files=f'{filename}',
            )

            # sequence_of_projections(
            #     full_path_input_mesh=path,
            #     optical_center_x=[0.0],
            #     optical_center_y=[0.0],
            #     optical_center_z=[optical[idx]],
            #     optical_axis_x=[0.0],
            #     optical_axis_y=[0.0],
            #     optical_axis_z=[1.0],
            #     output_width_in_pixels=1920,
            #     output_height_in_pixels=1080,
            #     prefix_output_files=f'./output/{filename}',
            # )
        except Exception as e:
            print(e)
