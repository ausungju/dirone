import sys
import base64
from io import BytesIO
from PIL import Image
# from ultralytics import YOLO
# import numpy as np
# import cv2

def detect_image(image):
    model = YOLO("yolov8n.pt")  
    results = model(image)
    result = model.predict(image, save=False,conf=0.5)
    plots = result[0].plot()

    return plots

while True:
    image_base64 = sys.stdin.readline()
    if not image_base64:
        break

    image = BytesIO(base64.b64decode(image_base64))
    image = Image.open(image)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    image = detect_image(image)
    image_base64 = base64.b64encode(image.tobytes).decode('utf-8')
    print(image_base64)

    sys.stdin.flush()

