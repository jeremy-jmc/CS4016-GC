"""
1. (2 points) OFF and PLY meshes of a cube with square faces.
"""

POINTS = [
    [-1, -1, -1],
    [-1, 1, -1],
    [-1, 1, 1],
    [-1, -1, 1],
    [1, -1, -1],
    [1, 1, -1],
    [1, 1, 1],
    [1, -1, 1]
]

FACES = [
    [0, 3, 2, 1],
    [3, 7, 6, 2],
    [7, 4, 5, 6],
    [4, 0, 1, 5],
    [1, 2, 6, 5],
    [3, 0, 4, 7]
]

def create_off(output_file: str, vertices: list, faces: list):
    file = open(output_file, mode='w')

    file.write('OFF\n')
    file.write(f'{len(vertices)} {len(faces)} {len(vertices)}')
    file.write('\n\n')

    for v in vertices:
        for p in v:
            file.write(f'{p} ')
        file.write('\n')
    
    file.write('\n')
    for face in faces:
        file.write(f'{len(face)} ')
        for i in face:
            file.write(f'{i} ')
        file.write('\n')
    file.close()


def create_ply(output_file: str, vertices: list, faces: list):
    file = open(output_file, mode='w')

    file.write('ply\n')
    file.write('format ascii 1.0\n')
    file.write(f'element vertex {len(vertices)}\n')
    file.write('property float x\n')
    file.write('property float y\n')
    file.write('property float z\n')
    file.write(f'element face {len(faces)}\n')
    file.write('property list uchar int vertex_index\n')
    file.write('end_header\n')
    file.write('\n')

    for v in vertices:
        for p in v:
            file.write(f'{p} ')
        file.write('\n')
    
    file.write('\n')
    for face in faces:
        file.write(f'{len(face)} ')
        for i in face:
            file.write(f'{i} ')
        file.write('\n')
    file.close()


def cube_with_square_faces(full_path_output_file: str):
    extension = full_path_output_file.split('.')[-1]

    if extension not in ['ply', 'off']:
        raise ValueError('File format not supported')

    if extension == 'off':
        create_off(full_path_output_file, POINTS, FACES)
    elif extension == 'ply':
        create_ply(full_path_output_file, POINTS, FACES)


if __name__ == '__main__':
    cube_with_square_faces('cube_off.off')
    cube_with_square_faces('cube_ply.ply')