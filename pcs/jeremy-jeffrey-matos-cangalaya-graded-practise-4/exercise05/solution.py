import cv2
from ultralytics import YOLO
import torch
import supervision as sv
import json
import os
import requests


def download_model(url: str, model_path: str):
    response = requests.get(url)
    if response.status_code == 200:
        with open(model_path, "wb") as f:
            f.write(response.content)
        print(f"Modelo descargado y guardado en {model_path}")
    else:
        raise Exception(f"Error al descargar el modelo: {response.status_code}")


# https://docs.ultralytics.com/tasks/segment/#models
model_path = "yolov8s-seg.pt"
model_url = (
    "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8s-seg.pt"
)


def count_people_cars_and_bikes(full_path_input_video: str) -> tuple:
    if not os.path.exists(model_path):
        download_model(model_url, model_path)

    # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # model = torch.hub.load("WongKinYiu/yolov7","custom", path_or_model=model_path,
    #                         source='github', trust_repo=True, verbose=True)
    # model = model.to(device)
    # model.eval()

    model = YOLO("yolov8s-seg.pt", verbose=False)
    # print(vars(model))
    # print(dir(model))
    # print(json.dumps(model.names, indent=2))
    cap = cv2.VideoCapture(full_path_input_video)

    if not cap.isOpened():
        print("Error: No se pudo abrir el video.")
        return 0, 0, 0

    person_count, bike_count, car_count = 0, 0, 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # results = model(frame_rgb)
        # detections = results.xyxy[0].cpu().numpy()

        detections = model(frame_rgb)[0].cpu().numpy().boxes
        # print(vars(detections))
        # print(dir(detections))
        for cls_ in detections.cls:
            if int(cls_) == 0:  # Clase 0 es persona
                person_count += 1
            elif int(cls_) == 1:  # Clase 1 es bicicleta
                bike_count += 1
            elif int(cls_) == 2:  # Clase 2 es auto
                car_count += 1
            else:
                continue
    cap.release()
    cv2.destroyAllWindows()

    return person_count, bike_count, car_count


if __name__ == "__main__":
    result = count_people_cars_and_bikes(
        full_path_input_video="../pc4-example-inputs/video-for-yolo/videoplayback.mp4",
    )

    print(f"People detected: {result[0]}")
    print(f"Bikes detected: {result[1]}")
    print(f"Cars detected: {result[2]}")

"""
-> The output result should be like this:
result[0] --> number of people detected in the video
result[1] --> number of bikes detected in the video
result[2] --> number of cars detected in the video
"""
