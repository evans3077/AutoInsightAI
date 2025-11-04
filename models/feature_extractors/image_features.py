import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

class ImageFeatureExtractor:
    def __init__(self):
        self.model = models.resnet18(pretrained=True)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

    def extract(self, image_path: str):
        image = Image.open(image_path).convert("RGB")
        image_tensor = self.transform(image).unsqueeze(0)
        with torch.no_grad():
            features = self.model(image_tensor)
        return features.squeeze().tolist()
