import cv2
from ultralytics import SAM, FastSAM
from ultralytics.models.fastsam import FastSAMPrompt
import torch
import supervision as sv
import json
import os
import requests
import torch
import numpy as np

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def download_model(url: str, model_path: str):
    response = requests.get(url)
    if response.status_code == 200:
        with open(model_path, "wb") as f:
            f.write(response.content)
        print(f"Modelo descargado y guardado en {model_path}")
    else:
        raise Exception(f"Error al descargar el modelo: {response.status_code}")


# https://docs.ultralytics.com/tasks/segment/#models
model_path = "sam.pt"
model_url = (
    # "https://github.com/ultralytics/assets/releases/download/v8.2.0/sam_b.pt"
    "https://github.com/ultralytics/assets/releases/download/v8.2.0/FastSAM-s.pt"
)

def highlight_people_cars_and_bikes(
    full_path_input_image: str,
    color_scale_image: tuple,
    color_scale_people: tuple,
    color_scale_cars: tuple,
    color_scale_bikes: tuple,
    full_path_output_image: str,
):
    if not os.path.exists(model_path):
        download_model(model_url, model_path)

    model = FastSAM(model_path)
    everything_results = model(full_path_input_image, device=device, retina_masks=True, imgsz=1024, conf=0.1, iou=0.9)
    print(everything_results)
    print(dir(everything_results))
    
    prompt_process = FastSAMPrompt(full_path_input_image, everything_results, device="cpu")
    # ann = prompt_process.everything_prompt()

    people = prompt_process.text_prompt(text="a photo of people")
    cars = prompt_process.text_prompt(text="a photo of cars")
    bikes = prompt_process.text_prompt(text="a photo of bikes")

    print('=========================================================================s')
    # print('people' in ann)
    print(people)
    print(cars)
    print(bikes)


if __name__ == "__main__":
    # for im in ['example1.jpg', 'example2.jpg', 'example3.jpg']:
    #     torch.cuda.empty_cache()
    #     highlight_people_cars_and_bikes(
    #         full_path_input_image=f'../pc4-example-inputs/images-for-last-exercise/{im}',
    #         color_scale_image=(255, 255, 255),
    #         color_scale_people=(255, 0, 0),
    #         color_scale_cars=(0, 255, 0),
    #         color_scale_bikes=(0, 0, 255),
    #         full_path_output_image=f"./detections-{im}",
    #     )
    #     break

    full_path_input_image=f'../pc4-example-inputs/images-for-last-exercise/example2.jpg'
    im = cv2.imread(full_path_input_image)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    print(im.shape)

    model = FastSAM(model_path)
    # print(everything_results)
    # print(dir(everything_results))
    
    for idx, t in enumerate(["person", "car", "bike"]):
        everything_results = model(full_path_input_image, device=device)    # , retina_masks=True, conf=0.1, iou=0.9
        prompt_process = FastSAMPrompt(full_path_input_image, everything_results, device="cpu")
        ann = prompt_process.text_prompt(text=t)
        mask = ann[0].masks.data.cpu().numpy()
        print(mask.shape)
        print(mask)
        # value counts
        print(np.unique(mask, return_counts=True))
        # save mask as black and white image
        cv2.imwrite(f'./{idx}.png', mask[0] * 255)

