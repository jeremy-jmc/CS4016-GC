"""
https://github.com/roboflow/supervision
    https://supervision.roboflow.com/develop/cookbooks/
        https://supervision.roboflow.com/develop/notebooks/quickstart/#install
    https://supervision.roboflow.com/latest/how_to/detect_and_annotate/
https://docs.roboflow.com/
https://github.com/ultralytics/ultralytics
    https://docs.ultralytics.com/tasks/segment/
    https://docs.ultralytics.com/modes/predict/#inference-arguments

TASK FOR THIS WEEK
    1, 2 Last slide of Monday

    3 (continuation)
        Use YOLO to count in a video PEOPLE, CARS and BIKES
"""

import cv2
from ultralytics import YOLO    # SAM, FastSAM
import supervision as sv
from supervision.assets import download_assets, VideoAssets
import numpy as np
import math
import json
print(sv.__version__)
import os
from ipywidgets import Video

model = YOLO("yolov8x-seg.pt")
print(f'n_classes: {len(model.names)}')
help(model.__call__)
print(json.dumps(model.names, indent=2))


print(dir(VideoAssets))

# asset = VideoAssets.GROCERY_STORE
# download_assets(asset)
    
# video = Video.from_file(asset.value)
# video
