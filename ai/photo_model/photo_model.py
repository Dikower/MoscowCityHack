from PIL import Image
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as T


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CPU = torch.device("cpu")
PATH_TO_MODEL = "model.pth"


"""
Ищет непотребный контент на изображениях.
"""

class PhotoModel:

    def __init__(self):
        self.model = models.resnet50(pretrained=True)

        self.model.fc = nn.Sequential(
            nn.Linear(2048, 1, bias=True),
            nn.Sigmoid()
        )
        self.model.load_state_dict(torch.load(PATH_TO_MODEL))
        self.model.eval()

        self.transformations = T.Compose([
            T.ToTensor(),
            T.Normalize((0, 0, 0),(1, 1, 1))
        ])

    def make_prediction(img, device):
    	img = img.convert("RGB")
    	if img.size != (224, 224):
    		img = img.resize((224, 224))
    	img_tensor = self.transformations(img)
    	return self.model(torch.reshape(img_tensor, (1, 3, 224, 224)).to(DEVICE))
