import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import torch
from PIL import Image
import torchvision.transforms as transforms
from models.efficientnet import EfficientNetClassifier
from config import MODEL_CONFIG

import torch.nn.functional as F
# Initialize model
model = EfficientNetClassifier(
    num_classes=MODEL_CONFIG['num_classes'],
    pretrained=False
)

# Set model to evaluation mode
model.eval()



# Load and preprocess a real image
image_path = "./images_test_website/canterbury_15_31857_20911.jpg"  
image = Image.open(image_path).convert('RGB')

# Define transforms to match training preprocessing
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Apply transforms and add batch dimension
image_tensor = transform(image).unsqueeze(0)

# Run forward pass
with torch.no_grad():
    outputs = model(image_tensor)



print(f"Type: {type(outputs)}")
print(f"Shape: {outputs.shape}")  
print(f"Raw values: {outputs}")


# After softmax:
probabilities = F.softmax(outputs, dim=1)

print(f"Probabilities: {probabilities}")
print(f"Probability sum: {probabilities.sum()}")  # Should be to 1.0


# Get the eligible probability (class 1)
eligible_prob = probabilities[0, 1].item()

# Use your optimal threshold to determine eligibility
OPTIMAL_THRESHOLD = 0.2031

if eligible_prob > OPTIMAL_THRESHOLD:
    print(f" ELIGIBLE - Confidence: {eligible_prob:.4f} ({eligible_prob*100:.2f}%)")
else:
    print(f"INELIGIBLE - Confidence: {(1-eligible_prob):.4f} ({(1-eligible_prob)*100:.2f}%)")

    
# Get predicted class
predicted_class = torch.argmax(probabilities, dim=1)
print(f"Predicted class: {predicted_class.item()}")
print(f"Confidence: {probabilities[0, predicted_class].item():.4f}")