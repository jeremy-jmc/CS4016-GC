import cv2
import matplotlib.pyplot as plt
import numpy as np
import random
import time

# -----------------------------------------------------------------------------
# 1a 1b 1c
# -----------------------------------------------------------------------------
table = np.full((10, 10, 10, 10, 3), 255, dtype='int')

w, h = table.shape[: 2]
plt.imshow(np.transpose(table, (0, 2, 1, 3, 4)).reshape((100, 100, 3)))
for i in range(w):
    for j in range(h):
        if i % 2 == 0:
            if j % 2 == 0:
                table[i, j, :, :] = [random.randint(0, 255) for _ in range(3)] # [0, 0, 0]
        else:
            if j % 2 != 0:
                table[i, j, :, :] = [random.randint(0, 255) for _ in range(3)]  # [0, 0, 0]

table = np.reshape(np.transpose(table, (0, 2, 1, 3, 4)), (100, 100, 3))
plt.imshow(table)


# -----------------------------------------------------------------------------
# 1c
# -----------------------------------------------------------------------------
radius = 30
canvas = np.full((100, 100, 3), 0, dtype='int')

w, h = canvas.shape[:2]
for i in range(w):
    for j in range(h):
        if (i - 50)**2 + (j - 50)**2 <= radius**2:
            canvas[i, j, :] = [0, 0, 255]
plt.imshow(canvas)


# -----------------------------------------------------------------------------
# 2a
# -----------------------------------------------------------------------------
def generate_frame(shape: tuple, 
                   center: tuple, 
                   direction: tuple, 
                   radius: int = 20):
    canvas = np.full(shape, 0, dtype='uint8')
    w, h = canvas.shape[:2]

    center_x, center_y = center
    dx, dy = direction

    if dx > 0 and center_x + radius >= w:
        dx = dx * -1
    elif dx < 0 and center_x - radius <= 0:
        dx = dx * -1
    if dy > 0 and center_y + radius >= h:
        dy = dy * -1
    elif dy < 0 and center_y - radius <= 0:
        dy = dy * -1
    
    center_x, center_y = center_x + dx, center_y + dy

    w, h = canvas.shape[:2]
    for i in range(w):
        for j in range(h):
            if (i - center_x)**2 + (j - center_y)**2 <= radius**2:
                canvas[i, j, :] = [0, 0, 255]
        
    center = (center_x, center_y)
    direction = (dx, dy)

    return direction, center, canvas

direction = (random.choice([-10, 10]), random.choice([-10, 10]))
w, h = (600, 1200)
radius = 40
center = (random.randint(0, w - radius), random.randint(0, h-radius))

while True:
    direction, center, img = generate_frame((w, h, 3), center, direction, radius)
    # print(direction, center)
    # time.sleep(2)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow("output", img_rgb)
    cv2.waitKey(1)
    # plt.imshow(img)
    # plt.show()

cv2.destroyAllWindows()

frame_list = []
video = cv2.VideoWriter('output.avi', 0, 1, w, h)
for image in frame_list:
    video.write(image)
video.release()

