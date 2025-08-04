import os
import cv2
from datetime import datetime

def save_image(image, folder="data"):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"fingerprint_{timestamp}.png"
    filepath = os.path.join(folder, filename)
    
    success = cv2.imwrite(filepath, image)
    if success:
        return filepath
    return None
