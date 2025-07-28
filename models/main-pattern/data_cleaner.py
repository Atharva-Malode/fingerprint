import cv2
import numpy as np
import os
from pathlib import Path

class DatasetPreprocessor:
    def __init__(self, input_root, output_root="preprocessed_data"):
        self.input_root = Path(input_root)
        self.output_root = Path(output_root)
        self.output_root.mkdir(parents=True, exist_ok=True)

    def preprocess_image(self, image_path):
        """Enhance contrast, smooth, binarize, and invert to white ridges on black."""
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

  
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(img)

      
        blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)

       
        binary = cv2.adaptiveThreshold(
            blurred, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            blockSize=11,
            C=2
        )

        
        kernel = np.ones((2, 2), np.uint8)
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)

        
        smoothed = cv2.GaussianBlur(closed, (3, 3), 0)
        _, final = cv2.threshold(smoothed, 128, 255, cv2.THRESH_BINARY)

        return final

    def process_dataset(self):
        """Walks through the dataset and processes every image."""
        for root, _, files in os.walk(self.input_root):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif')):
                    input_file_path = Path(root) / file
                    relative_path = input_file_path.relative_to(self.input_root)
                    output_file_path = self.output_root / relative_path

                    
                    output_file_path.parent.mkdir(parents=True, exist_ok=True)

                    processed_image = self.preprocess_image(input_file_path)
                    cv2.imwrite(str(output_file_path), processed_image)

        print(f"✅ Preprocessing complete. All data saved to: {self.output_root.resolve()}")


if __name__ == "__main__":
    input_dir = r"path"
    processor = DatasetPreprocessor(input_dir)
    processor.process_dataset()
