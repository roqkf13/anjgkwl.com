from ultralytics import YOLO
from ultralytics.utils import ASSETS

model = YOLO("yolov8n.pt")
results = model(ASSETS / "bus.jpg")
results[0].show()
