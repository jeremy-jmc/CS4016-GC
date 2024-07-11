import cv2
import numpy as np

marker_image = cv2.imread('marker.png', cv2.IMREAD_GRAYSCALE)
orb = cv2.ORB_create()

kp_marker, des_marker = orb.detectAndCompute(marker_image, None)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    kp_frame, des_frame = orb.detectAndCompute(gray_frame, None)
    matches = bf.match(des_marker, des_frame)
    matches = sorted(matches, key=lambda x: x.distance)

    if len(matches) > 135:
        src_pts = np.float32([kp_marker[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        h, w = marker_image.shape
        pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, matrix)

        frame = cv2.polylines(frame, [np.int32(dst)], True, (0, 255, 0), 3)

    if len(matches) > 135:
        src_pts = np.float32([kp_marker[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        matrix, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        h, w = marker_image.shape
        pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, matrix)

        ## Compute here a correct cube, with the correct pose. In this example
        ## I am just pasting a cube in an arbitrary pose on top of the
        ## original frame.
        img_to_overlay = cv2.imread('overlay_image.jpg')
        overlay = cv2.warpPerspective(img_to_overlay, matrix, (frame.shape[1], frame.shape[0]))
        mask = np.zeros_like(frame)
        cv2.fillPoly(mask, [np.int32(dst)], (255, 255, 255))

        masked_frame = cv2.bitwise_and(frame, 255 - mask)
        final_frame = cv2.add(masked_frame, overlay)
    else:
        final_frame = frame

    cv2.imshow('AR Overlay', final_frame)
    cv2.imshow('Marker Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

