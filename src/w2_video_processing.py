# https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
import numpy as np
import cv2
import time
from numba import jit, prange
from tqdm import tqdm

@jit(nopython=True)
def replace_back(img_rgb: np.array, back_rgb: np.array, threshold: int=200):
    new_img = img_rgb.copy()
    w, h = new_img.shape[:2]

    for i in prange(w):
        for j in prange(h):
            d = np.sqrt(np.sum((new_img[i, j, :] - np.array([0, 255, 0])) ** 2))
            if d <= threshold:
                new_img[i, j, :] = back_rgb[i, j, :]
    
    return new_img.astype(np.uint8)


cap = cv2.VideoCapture('../videos/green_screen_2.mp4')
back = cv2.VideoCapture('../videos/background.mp4')
print(type(cap), type(back))

total_frames = int(min(cap.get(cv2.CAP_PROP_FRAME_COUNT), back.get(cv2.CAP_PROP_FRAME_COUNT)))
print(f"Total frames: {total_frames}")

frame_count = 0
frame_list = []
with tqdm(total=total_frames) as pbar:
    while cap.isOpened() and back.isOpened():
        ret, frame = cap.read()
        ret_back, frame_back = back.read()

        if not ret or not ret_back:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # print(type(frame), type(frame_back))

        frame_back = cv2.resize(frame_back, (frame.shape[1], frame.shape[0]))
        assert frame.shape == frame_back.shape, "Dimensions doesn't match"

        # frame, frame_back = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), cv2.cvtColor(frame_back, cv2.COLOR_BGR2RGB)
        new_frame = replace_back(frame, frame_back)

        # print(frame.shape, frame_back.shape)
        frame_list.append(new_frame)
        frame_count += 1
        pbar.update(1)

cap.release()
back.release()

for frame in frame_list:
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
    time.sleep(0.05)
cv2.destroyAllWindows()
