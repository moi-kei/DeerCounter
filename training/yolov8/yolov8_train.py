from ultralytics import YOLO

#change to last.pt when training again
model = YOLO("yolov8l.pt")

results = model.train(data="datasets/data.yaml", epochs=10)