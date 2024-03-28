from ultralytics import YOLO

def predict_image(image_path):
    model = YOLO('models/yolov8m_250_deer.pt')
    
    # Predict and save the result
    results = model.predict(image_path, save=True, show_labels=False, show_conf=False, verbose=False, project=".", exist_ok=True)
    boxes = results[0].boxes.xyxy.tolist()
    
    return boxes