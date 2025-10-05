from transformers import pipeline
from PIL import Image
import os
import torch

# Load the pipeline globally (GPU if available)
PIPE = pipeline(
    "image-classification",
    model="linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification",
    device=0 if torch.cuda.is_available() else -1
)

def identify_disease(image_path):
    if not os.path.exists(image_path):
        return {"error": "Image not found."}

    try:
        # Open image and convert to RGB
        img = Image.open(image_path).convert("RGB")
        img = img.resize((224, 224))  # MobileNetV2 input size

        results = PIPE(img)

        if not results:
            return {"error": "No prediction returned"}

        # Take top result
        top = results[0]
        disease_name = top.get("label", "Unknown")
        confidence = float(top.get("score", 0)) * 100  # Convert to %

        return {
            "disease": disease_name,
            "confidence": round(confidence, 1),
            "image": image_path
        }

    except Exception as e:
        return {"error": str(e)}
