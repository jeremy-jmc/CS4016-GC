# https://github.com/paulguerrero/lang-sam
# !pip install torch torchvision
# !pip install -U git+https://github.com/luca-medeiros/lang-segment-anything.git

from PIL import Image
from lang_sam import LangSAM
import numpy as np
import matplotlib.pyplot as plt
import torch
import warnings
warnings.filterwarnings('ignore')

model = LangSAM()


def project_colors(img_input: np.ndarray, 
                   mask_or_vector: list = [255, 255, 255]
                   ) -> np.ndarray:
    """Project each pixel (color) of the image to a vector e.g. achromatic line

    Args:
        img_input (np.array): input image
        mask_or_vector (list, optional): Vector to calculate the projection of each color or mask with one vector to project for each pixel. Defaults to the achromatic line.
    """
    w, h = img_input.shape[:2]
    mask_or_vector = np.array(mask_or_vector)

    # generate projection mask
    mask = np.zeros((w, h, 3))
    if mask_or_vector.ndim == 1:
        mask[:, :, :] = mask_or_vector
    else:
        assert mask_or_vector.shape == img_input.shape, \
            "projecting mask does not have the same shape of img_input"
        mask = mask_or_vector.copy()

    # do projections
    new_img = np.zeros((w, h, 3))
    for i in range(w):
        for j in range(h):
            u, v = img_input[i, j], mask[i, j]
            new_img[i, j] = np.clip(v * np.dot(u, v) / np.dot(v, v), 0, 255)
    
    return new_img.astype(np.uint8)


def generate_mask(masks, colors, default_color) -> np.ndarray:
    assert len(masks) == len(colors)

    w, h = masks[0].shape[:2]
    mask_output = np.zeros((w, h, 3), np.uint8)
    for i in range(w):
        for j in range(h):
            flag = False
            for m , c in zip(masks, colors):
                if m[i, j] == 1:
                    mask_output[i, j] = np.array(c)
                    flag = True
                    break
            if not flag:
                mask_output[i, j] = np.array(default_color)
    return mask_output.astype('float64')


def highlight_people_cars_and_bikes(
    full_path_input_image: str,
    color_scale_image: tuple,
    color_scale_people: tuple,
    color_scale_cars: tuple,
    color_scale_bikes: tuple,
    full_path_output_image: str,
) -> None:
    print('Run by preference in Google Colab')
    image_pil = Image.open(full_path_input_image).convert("RGB")
    image_np = np.array(image_pil)
    # print(type(image_pil))
    # print(image_np.shape)
    
    # total_mask = np.zeros_like(image_pil.size).T
    prompts, color_scales = ["person", "bikes", "car"], \
        [color_scale_people, color_scale_bikes, color_scale_cars]
    
    mask_list = []
    for text_prompt in prompts:
        masks, boxes, phrases, logits = model.predict(image_pil, text_prompt)

        # print(np.unique(masks, return_counts=True))
        summed_masks = torch.sum(masks, dim=0).numpy()
        summed_masks[summed_masks > 0] = 1

        # print(summed_masks.shape)
        # print(np.unique(summed_masks, return_counts=True))
        
        mask_list.append(summed_masks)
        # plt.imshow(summed_masks)
        # plt.show()
    
    final_mask = generate_mask(mask_list, color_scales, color_scale_image)
    final_img = project_colors(image_np, final_mask)
    
    # plt.imshow(final_mask)
    # plt.show()
    # plt.imshow(image_np)
    # plt.show()
    # plt.imshow(final_img)
    # plt.show()

    # save image
    image = Image.fromarray(final_img)
    image.save(full_path_output_image)


if __name__ == '__main__':
    for idx, im in enumerate(['example1.jpg', 'example2.jpg', 'example3.jpg']):
        torch.cuda.empty_cache()
        highlight_people_cars_and_bikes(
            full_path_input_image=f'../pc4-example-inputs/images-for-last-exercise/{im}',   # im, 
            color_scale_image=(255, 255, 255),
            color_scale_people=(255, 0, 0),
            color_scale_cars=(0, 255, 0),
            color_scale_bikes=(0, 0, 255),
            full_path_output_image=f"./detections-{idx+1}.png",
        )
