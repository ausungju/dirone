import sys
import base64
from io import BytesIO
# from PIL import Image
# from ultralytics import YOLO


# def detect_image(image):
#     model = YOLO("yolov8n.pt")     
#     results = model(image)
#     return results

image_base64 = sys.argv[1]
image = BytesIO(base64.b64decode(image_base64))
image_base64 = base64.b64encode(image.getvalue()).decode('utf-8')
print(image_base64)
