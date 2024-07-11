import cv2
import numpy as np
import tempfile
from mayavi import mlab
import glob

def load_off(file_path):
    with open(file_path, 'r') as f:
        if 'OFF' not in f.readline().strip():
            raise ValueError("Not a valid OFF file")
        
        n_verts, n_faces, _ = map(int, f.readline().strip().split())
        verts = []
        for _ in range(n_verts):
            try:
                face_info = f.readline().strip().split()
                face_indices = list(map(float, face_info[:3]))
                verts.append(face_indices)
            except:
                n_verts+=1
        faces = []
        for _ in range(n_faces):
            face_info = f.readline().strip().split()
            n_indices = int(face_info[0])
            face_indices = list(map(int, face_info[1:n_indices+1]))
            faces.append(face_indices)
    return np.array(verts, dtype=np.float32), np.array(faces, dtype=np.uint32)

def draw_mesh_on_top_of_marker(full_path_input_image, full_path_mesh, full_path_output_image):
    # Load the input image
    input_image = cv2.imread(full_path_input_image)
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(input_image, cv2.IMREAD_GRAYSCALE)
    
    # Detect the QR code in the image
    qr_detector = cv2.QRCodeDetector()
    retval, points = qr_detector.detect(gray_image)
    
    if not retval:
        raise ValueError("No QR code detected in the image.")
    
    # Get the bounding box of the QR code
    points = points[0]
    qr_bbox = np.array(points, dtype=np.float32)
    
    # Load the mesh from the .off file
    verts, faces = load_off(full_path_mesh)
    
    # Compute the pose transformation
    qr_center = np.mean(qr_bbox, axis=0)
    qr_size = np.linalg.norm(qr_bbox[0] - qr_bbox[1])
    
    # Scale the mesh to fit the QR code
    bbox_min = verts.min(axis=0)
    bbox_max = verts.max(axis=0)
    bbox_center = (bbox_max + bbox_min) / 2
    bbox_size = np.linalg.norm(bbox_max - bbox_min)
    scale_factor = qr_size / bbox_size
    verts = (verts - bbox_center) * scale_factor + qr_center
    
    # Render the mesh using mayavi
    mlab.figure(size=(800, 600), bgcolor=(1, 1, 1))
    mlab.triangular_mesh(verts[:, 0], verts[:, 1], verts[:, 2], faces)
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    mlab.savefig(temp_file.name)
    mlab.close()
    
    # Load the rendered mesh image
    rendered_mesh_image = cv2.imread(temp_file.name)
    
    # Blend the rendered mesh with the original image
    alpha = 0.6
    blended_image = cv2.addWeighted(input_image, alpha, rendered_mesh_image, 1 - alpha, 0)
    
    # Save the output image
    cv2.imwrite(full_path_output_image, blended_image)

for idx, path in enumerate(glob.glob('../pc4-example-inputs/meshes-for-exercises-1-2-3/*.off')):
    #try:
        print(path)
        draw_mesh_on_top_of_marker(
            full_path_input_image='./qr.png',
            full_path_mesh=path,
            full_path_output_image=f'./result_02_{idx+1}.png',
        )
        break
    #except Exception as e:
    #    print(e)