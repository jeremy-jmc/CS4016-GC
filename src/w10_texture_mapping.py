"""
Texture mapping
    something that maps from 3d coordinates to 2d coordinates

"""


"""
Implement a program to model a sphere, a cylinder and a cube. Find different textures and apply each of them to all the 3 models created.
Your coude shoudl generate OFF files that show a sphere with texture, a cylinder with texture, etc

Example and sphere with the Peru flag
"""


import numpy as np
from PIL import Image

def generate_sphere_with_texture(radius, subdivisions):
    vertices = []
    phi = (1 + np.sqrt(5)) / 2

    vertices.append(np.array([-1,  phi, 0]))
    vertices.append(np.array([ 1,  phi, 0]))
    vertices.append(np.array([-1, -phi, 0]))
    vertices.append(np.array([ 1, -phi, 0]))
    vertices.append(np.array([ 0, -1,  phi]))
    vertices.append(np.array([ 0,  1,  phi]))
    vertices.append(np.array([ 0, -1, -phi]))
    vertices.append(np.array([ 0,  1, -phi]))
    vertices.append(np.array([ phi, 0, -1]))
    vertices.append(np.array([ phi, 0,  1]))
    vertices.append(np.array([-phi, 0, -1]))
    vertices.append(np.array([-phi, 0,  1]))

    vertices = [radius * v / np.linalg.norm(v) for v in vertices]

    tex_coords = [spherical_to_uv(v) for v in vertices]

    faces = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ]

    def midpoint(v1, v2):
        mid = (v1 + v2) / 2
        return radius * mid / np.linalg.norm(mid)

    for _ in range(subdivisions):
        new_faces = []
        midpoints = {}

        def get_midpoint_index(v1, v2):
            key = tuple(sorted((tuple(v1), tuple(v2))))
            if key not in midpoints:
                midpoints[key] = len(vertices)
                midpoint_vertex = midpoint(v1, v2)
                vertices.append(midpoint_vertex)
                tex_coords.append(spherical_to_uv(midpoint_vertex))
            return midpoints[key]

        for face in faces:
            v1, v2, v3 = [vertices[i] for i in face]
            a = get_midpoint_index(v1, v2)
            b = get_midpoint_index(v2, v3)
            c = get_midpoint_index(v3, v1)
            i1, i2, i3 = face
            new_faces.append([i1, a, c])
            new_faces.append([i2, b, a])
            new_faces.append([i3, c, b])
            new_faces.append([a, b, c])

        faces = new_faces

    return vertices, faces, tex_coords

def spherical_to_uv(v):
    x, y, z = v
    u = 0.5 + (np.arctan2(z, x) / (2 * np.pi))
    v = 0.5 - (np.arcsin(y / np.linalg.norm([x, y, z])) / np.pi)
    return [u, v]

def save_off_with_texture_colors(filename, vertices, faces, tex_coords, image):
    img = Image.open(image)
    img_width, img_height = img.size
    img = img.convert('RGB')

    colors = []
    for tex_coord in tex_coords:
        u, v = tex_coord
        px = int(u * img_width)
        py = int(v * img_height)
        px = min(px, img_width - 1)
        py = min(py, img_height - 1)
        r, g, b = img.getpixel((px, py))
        colors.append((r / 255.0, g / 255.0, b / 255.0))

    with open(filename, 'w') as f:
        f.write("COFF\n")
        f.write(f"{len(vertices)} {len(faces)} 0\n")
        
        for vertex, color in zip(vertices, colors):
            f.write(f"{vertex[0]} {vertex[1]} {vertex[2]} {color[0]} {color[1]} {color[2]}\n")
        
        for face in faces:
            f.write(f"3 {' '.join(map(str, face))}\n")

radius = 2.0
subdivisions = 7
image_path = 'map.jpg'

vertices, faces, tex_coords = generate_sphere_with_texture(radius, subdivisions)
save_off_with_texture_colors("sphere_with_texture_colors.off", vertices, faces, tex_coords, image_path)
