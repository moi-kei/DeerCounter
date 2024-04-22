from ultralytics import YOLO

def predict_image(image_path):
    """Predict bounding boxes for objects in an image using YOLOv5 model.

    Args:
        image_path (str): Path to the input image file.

    Returns:
        list: A list of bounding boxes in the format [[x_min, y_min, x_max, y_max], ...].
    """
    # Initialize YOLO model with pre-trained weights
    model = YOLO('models/yolov8m_250_deer.pt')
    
    # Predict bounding boxes
    results = model.predict(image_path, save=True, show_labels=False, show_conf=False, verbose=False, project=".", exist_ok=True)
    
    # Extract bounding box coordinates
    boxes = results[0].boxes.xyxy.tolist()
    
    return boxes