import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
import math
import random

img : np.ndarray = cv2.imread('../img/mario.jpg')
background : np.ndarray = cv2.imread('../img/comas_fondo.png')

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
back_rgb = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)
back_rgb = cv2.resize(back_rgb, (img_rgb.shape[1], img_rgb.shape[0]))

assert img_rgb.shape == back_rgb.shape, "Dimensions doesn't match"
assert img_rgb.dtype == back_rgb.dtype, "Dtype doesn't match"

# plt.hist(img_rgb.ravel())

# pixel_list = img_rgb.reshape(-1, 3)
# value_counts = np.unique(pixel_list, axis=0, return_counts=True)
# sorted_idx = np.argsort(value_counts[1])[::-1]

# sorted_pixels = value_counts[0][sorted_idx]
# sorted_freqs = value_counts[1][sorted_idx]

# for valor, conteo in zip(sorted_pixels, sorted_freqs):
#     print(f"Valor: {valor}, Conteo: {conteo}")

new_img = img_rgb.copy()
w, h = new_img.shape[:2]
threshold = 125

distances = []
for i in range(w):
    for j in range(h):
        d = distance.euclidean(new_img[i, j, :], np.array([0, 255, 0]))
        if d <= threshold:
            # print(new_img[i, j, :], back_rgb[i, j, :])
            new_img[i, j, :] = back_rgb[i, j, :]
        distances.append(d)

# plt.hist(distances)
plt.imshow(img_rgb)
plt.axis('off')
plt.show()

plt.imshow(back_rgb)
plt.axis('off')
plt.show()

plt.imshow(new_img)
plt.axis('off')
plt.show()