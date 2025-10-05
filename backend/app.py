from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from photo_recognition import identify_disease
import os
import json

# ===== Load labels with advice =====
LABELS_PATH = os.path.join(os.path.dirname(__file__), "labels.json")
with open(LABELS_PATH, "r") as f:
    LABELS = json.load(f)

# ===== Import feature routers =====
from organic_advice import router as organic_router
from seasonal_calendar import router as calendar_router
from weather_alerts import router as weather_router
from community import router as community_router
from success_tracking import router as success_router
from video_tutorials import router as video_router
from offline_support import router as offline_router
from local_suppliers import router as supplier_router

# ===== Initialize FastAPI app =====
app = FastAPI(title="Plant Disease Advisory API")

# ===== Enable CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Root endpoint =====
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Plant Disease Advisory API is running."}

# ===== /predict endpoint =====
@app.post("/predict", tags=["Prediction"])
async def predict(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    try:
        # Save uploaded file temporarily
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Predict disease using photo_recognition.py
        result = identify_disease(temp_path)
        disease_name = result.get("disease", "Unknown")
        confidence = result.get("confidence", 0)

        # Match disease exactly from JSON (case-insensitive)
        advice = "Advice not available. Please consult an expert."
        for val in LABELS.values():
            if val["label"].strip().lower() == disease_name.strip().lower():
                advice = val["advice"]
                break

        return {
            "disease": disease_name,
            "confidence": confidence,
            "advice": advice
        }

    except Exception as e:
        return {
            "disease": "Error",
            "confidence": 0,
            "advice": str(e)
        }

    finally:
        # Ensure temporary file is removed
        if os.path.exists(temp_path):
            os.remove(temp_path)

# ===== Include all routers with adjusted prefixes =====
# Now frontend JS can call exactly:
# /organic/advice, /calendar/seasonal_calendar, /weather/weather_alert/{city}, /suppliers/?lat=&lon=
app.include_router(organic_router, prefix="/organic", tags=["Organic Advice"])
app.include_router(calendar_router, prefix="/calendar", tags=["Seasonal Calendar"])
app.include_router(weather_router, prefix="/weather", tags=["Weather Alerts"])
app.include_router(community_router, prefix="/community", tags=["Community"])
app.include_router(success_router, prefix="/success", tags=["Success Tracking"])
app.include_router(video_router, prefix="/videos", tags=["Video Tutorials"])
app.include_router(offline_router, prefix="/offline", tags=["Offline Support"])
app.include_router(supplier_router, prefix="/suppliers", tags=["Local Suppliers"])
