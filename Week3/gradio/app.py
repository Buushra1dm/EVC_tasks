import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image
import gradio as gr

# Load the pre-trained model (ResNet50)
model = resnet50(pretrained=True)
model.eval()

# Define the transforms
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize to the size expected by ResNet
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Define the prediction function
def predict(image):
    image = Image.fromarray(image.astype('uint8'), 'RGB')
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
    return predicted.item()

# Create and launch the Gradio interface
iface = gr.Interface(fn=predict, inputs="image", outputs="label")
iface.launch()
