import torch
from pathlib import Path
from PIL import Image
from torchvision.transforms import functional as F

class YOLOv8Inference:
    
    path = "/Users/nichdylan/Documents/AR_Assembly/runs/detect/train10/weights/best.pt"

    def __init__(self, model_path=path):
        self.model = torch.load(model_path).fuse().eval()

    def predict(self, image_path):
        img = Image.open(image_path)
        img = F.to_tensor(img).unsqueeze(0)

        with torch.no_grad():
            prediction = self.model(img)

        # Process the prediction as needed
        # For simplicity, returning the raw prediction for now
        return prediction
    
