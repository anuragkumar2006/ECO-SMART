import io
from PIL import Image
import torch
from torchvision import transforms

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

transform_pipeline = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def validate_image_file(uploaded_file):
    if uploaded_file.size > MAX_FILE_SIZE_BYTES:
        raise ValueError("Image file size exceeds the 10MB maximum limit.")

    ext = uploaded_file.name.split('.')[-1].lower() if '.' in uploaded_file.name else ''
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file format. Please upload a valid JPG, JPEG, or PNG image.")

    try:
        image = Image.open(uploaded_file)
        image.verify()
        uploaded_file.seek(0)
    except Exception:
        raise ValueError("Corrupted or unreadable image file.")

def preprocess_image(uploaded_file):
    validate_image_file(uploaded_file)
    uploaded_file.seek(0)
    img = Image.open(uploaded_file).convert('RGB')
    tensor = transform_pipeline(img).unsqueeze(0)
    return tensor, img
