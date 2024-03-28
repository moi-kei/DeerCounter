import os
from ultralytics import YOLO

def predict_image(image_path):
    model = YOLO('models/yolov8m_250_deer.pt')
    
    # Extract image name from image path
    image_name = os.path.basename(image_path)
    
    # Predict and save the result
    results = model.predict(image_path, save=True, show_labels=False, show_conf=False, verbose=False, project=".", exist_ok=True)
    boxes = results[0].boxes.xyxy.tolist()
    for box in boxes:
        print(box)

    # Construct the path of the saved image and normalize it
    saved_image_path = os.path.normpath(os.path.join("predict", image_name))
    
    return saved_image_path