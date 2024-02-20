from ultralytics import YOLO

model = YOLO("yolov8l.pt")

results = model.train(data="datasets/data.yaml", epochs=10)