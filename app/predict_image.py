import os
from ultralytics import YOLO

def predict_image(image_path):
    model = YOLO('models/best.pt')
    
    # Extract image name from image path
    image_name = os.path.basename(image_path)
    
    # Predict and save the result
    model.predict(image_path, save=True, show_labels=False, show_conf=False, verbose=False, project="predicted_images", exist_ok=True)
    
    # Construct the path of the saved image and normalize it
    saved_image_path = os.path.normpath(os.path.join("predicted_images/predict", image_name))
    
    return saved_image_path