import numpy as np
from PIL import Image
import os

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
    
    return np.array(vertices), np.array(faces)

def painter_algorithm_textures(full_path_input_mesh, full_path_input_texture, full_path_output_image,
                               min_x_coordinate_in_projection_plane, min_y_coordinate_in_projection_plane,
                               max_x_coordinate_in_projection_plane, max_y_coordinate_in_projection_plane,
                               width_in_pixels, height_in_pixels):
    # Load the mesh and texture
    vertices, faces = read_ply(full_path_input_mesh)
    texture_image = Image.open(full_path_input_texture).convert('RGB')
    texture = np.array(texture_image)

    # Avoid division by zero or extremely large values
    vertices[:, 2] = np.clip(vertices[:, 2], 1e-5, None)
    
    # Project vertices onto the 2D plane
    projected_vertices = vertices[:, :2] / vertices[:, 2].reshape(-1, 1)

    # Scale to image coordinates
    scale_x = width_in_pixels / (max_x_coordinate_in_projection_plane - min_x_coordinate_in_projection_plane)
    scale_y = height_in_pixels / (max_y_coordinate_in_projection_plane - min_y_coordinate_in_projection_plane)

    projected_vertices[:, 0] = (projected_vertices[:, 0] - min_x_coordinate_in_projection_plane) * scale_x
    projected_vertices[:, 1] = (projected_vertices[:, 1] - min_y_coordinate_in_projection_plane) * scale_y

    # Order faces by the farthest vertex
    face_depths = np.max(vertices[faces][:, :, 2], axis=1)
    ordered_faces = faces[np.argsort(-face_depths)]

    # Prepare the image and z-buffer
    image = np.zeros((height_in_pixels, width_in_pixels, 3), dtype=np.uint8)
    z_buffer = np.full((height_in_pixels, width_in_pixels), -np.inf)

    for face in ordered_faces:
        vert_indices = face
        vert_coords = projected_vertices[vert_indices]
        vert_depths = vertices[vert_indices, 2]
        uv_coords = vertices[vert_indices, -2:]

        if np.any(np.isnan(vert_coords)) or np.any(np.isinf(vert_coords)):
            continue

        bbox_min_x = max(int(np.min(vert_coords[:, 0])), 0)
        bbox_max_x = min(int(np.max(vert_coords[:, 0])), width_in_pixels - 1)
        bbox_min_y = max(int(np.min(vert_coords[:, 1])), 0)
        bbox_max_y = min(int(np.max(vert_coords[:, 1])), height_in_pixels - 1)

        for y in range(bbox_min_y, bbox_max_y + 1):
            for x in range(bbox_min_x, bbox_max_x + 1):
                u, v, w = compute_barycentric_coordinates(x, y, vert_coords)
                if u >= 0 and v >= 0 and w >= 0:
                    z = u * vert_depths[0] + v * vert_depths[1] + w * vert_depths[2]
                    if z > z_buffer[y, x]:
                        z_buffer[y, x] = z
                        tex_x = int((u * uv_coords[0, 0] + v * uv_coords[1, 0] + w * uv_coords[2, 0]) * (texture.shape[1] - 1))
                        tex_y = int((u * uv_coords[0, 1] + v * uv_coords[1, 1] + w * uv_coords[2, 1]) * (texture.shape[0] - 1))
                        tex_x = np.clip(tex_x, 0, texture.shape[1] - 1)
                        tex_y = np.clip(tex_y, 0, texture.shape[0] - 1)
                        image[y, x] = texture[tex_y, tex_x]

    output_image = Image.fromarray(image)
    output_image.save(full_path_output_image)

def compute_barycentric_coordinates(x, y, vertices):
    x0, y0 = vertices[0]
    x1, y1 = vertices[1]
    x2, y2 = vertices[2]
    
    denom = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if denom == 0:
        return -1, -1, -1  # Degenerate triangle
    u = ((y1 - y2) * (x - x2) + (x2 - x1) * (y - y2)) / denom
    v = ((y2 - y0) * (x - x2) + (x0 - x2) * (y - y2)) / denom
    w = 1 - u - v
    return u, v, w

# Ejemplo de uso:
painter_algorithm_textures(
    full_path_input_mesh='sphere-triangles_big.ply',
    full_path_input_texture='texture1.png',
    full_path_output_image='output.png',
    min_x_coordinate_in_projection_plane=-1.0,
    min_y_coordinate_in_projection_plane=-1.0,
    max_x_coordinate_in_projection_plane=1.0,
    max_y_coordinate_in_projection_plane=1.0,
    width_in_pixels=640,
    height_in_pixels=480
)


