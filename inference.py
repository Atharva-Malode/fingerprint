import torch
from torchvision import transforms
from PIL import Image
import torch.nn.functional as F


from swin_transformer import FingerprintSwinWithAttention

def load_model(model_path, num_classes=3, device='cpu'):
    """
    Loads the trained model from a .pth file.
    """
    print(f"Loading model from: {model_path}")
    

    model = FingerprintSwinWithAttention(num_classes=num_classes, freeze_base=False)

    try:
        checkpoint = torch.load(model_path, map_location=device)
    except FileNotFoundError:
        print(f"❌ Error: Model file not found at {model_path}")
        return None
        

    model.load_state_dict(checkpoint['model_state_dict'])
    

    model.to(device)
    model.eval()
    
    print("✅ Model loaded successfully.")
    return model

def preprocess_image(image_path):
    """
    Loads an image, resizes it, and applies the necessary transformations.
    """

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    

    try:
        image = Image.open(image_path).convert('RGB')
    except FileNotFoundError:
        print(f"❌ Error: Image file not found at {image_path}")
        return None
        
    
    return transform(image).unsqueeze(0)

def predict(model, image_tensor, class_names, device='cpu'):
    """
    Performs inference on a single image tensor and returns the prediction.
    """
    
    image_tensor = image_tensor.to(device)
    
    with torch.no_grad():
       
        outputs = model(image_tensor)
        
        
        probabilities = F.softmax(outputs, dim=1)[0]
        
       
        confidence, predicted_idx = torch.max(probabilities, 0)
        
   
    predicted_class = class_names[predicted_idx.item()]
    
    return predicted_class, confidence.item(), probabilities.cpu().numpy()

if __name__ == '__main__':

    MODEL_PATH = r"path"  
    IMAGE_PATH = "fingerprint.bmp"                 

    CLASS_NAMES = ['Arch', 'Whorl', 'Loop']
    

    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {DEVICE}")

    model = load_model(MODEL_PATH, num_classes=len(CLASS_NAMES), device=DEVICE)
    
    if model is not None:

        image_tensor = preprocess_image(IMAGE_PATH)
        
        if image_tensor is not None:
            
            predicted_class, confidence, all_probabilities = predict(model, image_tensor, CLASS_NAMES, device=DEVICE)

            print("\n" + "="*30)
            print("🔍 Inference Results")
            print("="*30)
            print(f"🖼️ Image Path: {IMAGE_PATH}")
            print(f"🎯 Predicted Pattern: **{predicted_class}**")
            print(f"Confidence: {confidence:.2%}")
            print("\n📊 Full Probability Distribution:")
            for i, class_name in enumerate(CLASS_NAMES):
                print(f"  - {class_name:<10}: {all_probabilities[i]:.2%}")
            print("="*30)
