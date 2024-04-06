import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

# -----------------------------------------------------------------------------
# Read in an image
# -----------------------------------------------------------------------------
img : np.ndarray = cv2.imread('../img/lenna.png')     # read in BGR by default
print(img.shape)
img = cv2.resize(img, (50, 50))
print(dir(img))
print(img.shape)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print(type(img))

plt.imshow(img_rgb)

# -----------------------------------------------------------------------------
# Resampling the image with bilinear interpolation
# -----------------------------------------------------------------------------

"""
Let's assuming that the image is something continuous

"""

def bilinear_interpolation(img: np.ndarray, new_shape: tuple) -> np.ndarray:
    input_height, input_width = img.shape[:2]
    channels = img.shape[2]
    output_height, output_width = new_shape

    scaling_x, scaling_y = output_height / input_height, output_width / input_width
    # print(scaling_x, scaling_y)

    output_image = np.zeros((output_height, output_width, channels))

    for i in range(output_height):
        for j in range(output_width):
            new_i, new_j = i / scaling_x, j / scaling_y

            x1, y1 = math.floor(new_i), math.floor(new_j)
            x2, y2 = min(math.ceil(new_i), input_height - 1), min(math.ceil(new_j), input_width - 1)


            # weighted average: https://en.wikipedia.org/wiki/Bilinear_interpolation#/media/File:BilinearInterpolationV2.svg
            # bbox = ((x1, y1), (x2, y2))
            # print((i, j), '->', (new_i, new_j), '->', bbox)
            if (x1 == x2) and (y1 == y2):
                new_color = img[x1, y1, :]
            elif (x2 == x1):
                f_x_y1 = img[x1, y1, :]
                f_x_y2 = img[x1, y2, :]
                new_color = (y2 - new_j) / (y2 - y1) * f_x_y1 + \
                    (new_j - y1) / (y2 - y1) * f_x_y2
            elif (y2 == y1):
                f_x1_y = img[x1, y1, :]
                f_x2_y = img[x2, y1, :]
                new_color = (x2 - new_i) / (x2 - x1) * f_x1_y + \
                    (new_i - x1) / (x2 - x1) * f_x2_y
            else:
                f_x_y1 = (x2 - new_i) / (x2 - x1) * img[x1, y1, :] + \
                    (new_i - x1) / (x2 - x1) * img[x2, y1, :]
                f_x_y2 = (x2 - new_i) / (x2 - x1) * img[x1, y2, :] + \
                    (new_i - x1) / (x2 - x1) * img[x2, y2, :]
                
                new_color = (y2 - new_j) / (y2 - y1) * f_x_y1 + (new_j - y1) / (y2 - y1) * f_x_y2
            
            output_image[i, j] = new_color
    
    # print(output_image)
    return output_image

plt.imshow(img_rgb)
plt.show()
output_image = bilinear_interpolation(img_rgb, (200, 200)).astype(int)
plt.imshow(output_image)
plt.show()

plt.hist(output_image.ravel())

# # -----------------------------------------------------------------------------
# # Display each channel
# # -----------------------------------------------------------------------------
# fig, axs = plt.subplots(3, 1, figsize=(8, 8))

# axs[0].imshow(img_rgb[:, :, 0], cmap='Reds')
# axs[0].set_title('Red Channel')

# axs[1].imshow(img_rgb[:, :, 1], cmap='Greens')
# axs[1].set_title('Green Channel')

# axs[2].imshow(img_rgb[:, :, 2], cmap='Blues')
# axs[2].set_title('Blue Channel')

# plt.tight_layout()
# plt.show()

# # -----------------------------------------------------------------------------
# # Display the histogram of each channel
# # -----------------------------------------------------------------------------
# fig, axs = plt.subplots(3, 1, figsize=(8, 8))
# axs[0].hist(img_rgb[:, :, 0].ravel(), bins=256, color='r', alpha=0.5, label='Red Channel')
# axs[1].hist(img_rgb[:, :, 1].ravel(), bins=256, color='g', alpha=0.5, label='Green Channel')
# axs[2].hist(img_rgb[:, :, 2].ravel(), bins=256, color='b', alpha=0.5, label='Blue Channel')
# plt.show()
