from fastapi import APIRouter, Query
import json
import os

router = APIRouter()

# Path to labels.json
LABELS_PATH = os.path.join(os.path.dirname(__file__), "labels.json")

# Load labels.json at startup
with open(LABELS_PATH, "r") as f:
    labels_data = json.load(f)

# Map disease label → advice steps
organic_remedies = {}
for val in labels_data.values():
    label = val["label"]
    advice = val["advice"]
    steps = [step.strip() for step in advice.split(".") if step.strip()]
    organic_remedies[label] = steps

@router.get("/advice")
async def get_organic_advice(disease: str = Query(..., description="Name of the plant disease")):
    remedies = organic_remedies.get(disease, ["No advice available. Please consult an expert."])
    return {"disease": disease, "organic_remedies": remedies}
