import sys
import os
import math
import numpy as np
import cv2

def load_image(image_path: str) -> np.ndarray:
    """Load an image from the given path"""
    assert os.path.exists(image_path), f'Invalid input image path: {image_path}'
    img = cv2.imread(image_path)
    assert img is not None, f'Failed to load image: {image_path}'
    return img


def bilinear_interpolation(img: np.ndarray, new_shape: tuple) -> np.ndarray:
    """Perform bilinear interpolation on an image

    Args:
        img (np.ndarray): image to be interpolated
        new_shape (tuple): new shape of the image. Format: (height, width)

    Returns:
        np.ndarray: interpolated image

    References:
        https://en.wikipedia.org/wiki/Bilinear_interpolation
    """

    assert len(img.shape) == 3, 'Invalid image shape'
    assert len(new_shape) == 2, 'Invalid new shape'

    input_height, input_width, channels = img.shape
    output_height, output_width = new_shape

    scaling_x = output_height / input_height
    scaling_y = output_width / input_width

    output_image = np.zeros((output_height, output_width, channels))

    for i in range(output_height):
        for j in range(output_width):
            new_i, new_j = i / scaling_x, j / scaling_y

            x1, y1 = math.floor(new_i), math.floor(new_j)
            x2 = min(math.ceil(new_i), input_height - 1)
            y2 = min(math.ceil(new_j), input_width - 1)

            if (x1 == x2) and (y1 == y2):
                # CASE 1: 
                new_color = img[x1, y1, :]
            elif (x2 == x1):
                # CASE 2:
                f_x_y1 = img[x1, y1, :]
                f_x_y2 = img[x1, y2, :]
                diff_y = y2 - y1
                new_color = (y2 - new_j) / diff_y * f_x_y1 + \
                    (new_j - y1) / diff_y * f_x_y2
            elif (y2 == y1):
                # CASE 3:
                f_x1_y = img[x1, y1, :]
                f_x2_y = img[x2, y1, :]
                diff_x = x2 - x1

                new_color = (x2 - new_i) / diff_x * f_x1_y + \
                    (new_i - x1) / diff_x * f_x2_y
            else:
                # CASE 4:
                diff_x = x2 - x1
                f_x_y1 = (x2 - new_i) / diff_x * img[x1, y1, :] + \
                    (new_i - x1) / diff_x * img[x2, y1, :]
                f_x_y2 = (x2 - new_i) / diff_x * img[x1, y2, :] + \
                    (new_i - x1) / diff_x * img[x2, y2, :]
                diff_y = y2 - y1

                new_color = (y2 - new_j) / diff_y * f_x_y1 + \
                    (new_j - y1) / diff_y * f_x_y2
            
            output_image[i, j] = new_color
    
    return output_image.astype(np.uint8)


def exercise01(input_image_path: str, 
               new_height: int, new_width: int, 
               working_dir: str) -> None:
    """Solution for exercise 01

    Args:
        input_image_path (str): input image path
        new_height (int): height to resize the image
        new_width (int): width to resize the image
        working_dir (str): working directory to save the output image
    """
    img: np.ndarray = load_image(input_image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    output_image = bilinear_interpolation(img_rgb, (new_height, new_width))
    output_image = cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)

    file_name, _ = os.path.splitext(input_image_path)
    image_name = os.path.basename(file_name)
    new_image_name = f'{image_name}_{new_height}_{new_width}.png'
    output_image_path = os.path.join(working_dir, new_image_name)
    cv2.imwrite(output_image_path, output_image)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python solution.py <input_image> <height> <width>")
        sys.exit('Invalid number of arguments')
    

    working_dir = os.path.join(os.path.dirname(sys.argv[0]), 'output')
    os.makedirs(working_dir, exist_ok=True)

    input_image = sys.argv[1]
    new_height = int(sys.argv[2])
    new_width = int(sys.argv[3])

    # print(f'{working_dir=} {input_image=} {new_height=} {new_width=}')
    exercise01(input_image, new_height, new_width, working_dir)