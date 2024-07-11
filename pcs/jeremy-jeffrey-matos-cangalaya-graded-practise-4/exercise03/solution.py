import cv2
import numpy as np
import tempfile
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import glob

orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

def load_off(file_path):
    with open(file_path, 'r') as f:
        if 'OFF' not in f.readline().strip():
            raise ValueError("Not a valid OFF file")
        
        n_verts, n_faces, _ = map(int, f.readline().strip().split())
        verts = []
        for _ in range(n_verts):
            face_info = f.readline().strip().split()
            if '#' in face_info:
                face_info = f.readline().strip().split()
            face_indices = list(map(float, face_info[:3]))
            verts.append(face_indices)
        faces = []
        for _ in range(n_faces):
            face_info = f.readline().strip().split()
            n_indices = int(face_info[0])
            face_indices = list(map(int, face_info[1:n_indices+1]))
            faces.append(face_indices)
    return np.array(verts, dtype=np.float32), np.array(faces, dtype=np.uint32)

def rotate_y(vertices, angle):
    angle_rad = np.deg2rad(angle)
    rotation_matrix = np.array([
        [np.cos(angle_rad), 0, np.sin(angle_rad)],
        [0, 1, 0],
        [-np.sin(angle_rad), 0, np.cos(angle_rad)]
    ])
    return np.dot(vertices, rotation_matrix)

def draw_mesh_on_top_of_marker(full_path_input_image, full_path_mesh, full_path_output_image):
    frame = cv2.imread(full_path_input_image)
    marker_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect QR code
    qr_detector = cv2.QRCodeDetector()
    retval, points = qr_detector.detect(marker_image)
    if not retval:
        raise ValueError("No QR code detected in the image.")
    points = points[0].reshape(-1, 2)

    # Load and process 3D model image
    verts, faces = load_off(full_path_mesh)
    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.grid(False)
    ax.axis('off')
    ax.view_init(elev=90, azim=-90)
    ax.add_collection3d(Poly3DCollection(verts[faces], alpha=0.25))
    x_limits = [verts[:,0].min(), verts[:,0].max()]
    y_limits = [verts[:,1].min(), verts[:,1].max()]
    z_limits = [verts[:,2].min(), verts[:,2].max()]
    max_range = np.array([x_limits, y_limits, z_limits]).ptp(axis=1).max() / 2

    mid_x = sum(x_limits) / 2
    mid_y = sum(y_limits) / 2
    mid_z = sum(z_limits) / 2

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    # Save the figure
    plt.savefig('model_image.png')
    plt.close(fig)  # Close the figure to free memory

    img_to_overlay = cv2.imread('model_image.png')

    # Compute bounding box dimensions for resizing the overlay
    qr_width = int(np.linalg.norm(points[0] - points[1]))
    qr_height = int(np.linalg.norm(points[1] - points[2]))
    img_to_overlay = cv2.resize(img_to_overlay, (qr_width, qr_height))

    # Create a mask for the QR code area
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [np.int32(points)], 255)

    # Mask the area in the frame where the QR code is
    frame[mask == 255] = 0

    # Place the resized overlay image at the QR code location
    x, y = np.min(points, axis=0).astype(int)
    frame[y:y+qr_height, x:x+qr_width] = img_to_overlay

    # Save the final result
    cv2.imwrite(full_path_output_image, frame)

# Example usage
for idx, path in enumerate(glob.glob('../pc4-example-inputs/meshes-for-exercises-1-2-3/*.off')):
    try:
        print(path)
        draw_mesh_on_top_of_marker(
            full_path_input_image='./qr.png',
            full_path_mesh=path,
            full_path_output_image=f'./result_02_{idx+1}.png',
        )
    except Exception as e:
        print(e)
