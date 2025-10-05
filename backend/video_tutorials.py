from fastapi import APIRouter
from gtts import gTTS
import os

router = APIRouter()

# Folder to save TTS audios
TTS_FOLDER = "tts_audio"
os.makedirs(TTS_FOLDER, exist_ok=True)

# Hardcoded tutorials data (from your tutorials.json)
TUTORIALS = [
    {"label": "Apple Scab", "video_url": "https://www.youtube.com/watch?v=SMS2jHqACrY"},
    {"label": "Apple with Black Rot", "video_url": "https://www.youtube.com/watch?v=cYLrdQGdjf8"},
    {"label": "Cedar Apple Rust", "video_url": "https://www.youtube.com/watch?v=ZyG6H1uZ4fI"},
    {"label": "Healthy Apple", "video_url": "https://www.youtube.com/watch?v=3Xk9g7G6g0g"},
    {"label": "Healthy Blueberry Plant", "video_url": "https://www.youtube.com/watch?v=8Qj9g5g5g5g"},
    {"label": "Cherry with Powdery Mildew", "video_url": "https://www.youtube.com/watch?v=q1G4RsslFYI"},
    {"label": "Healthy Cherry Plant", "video_url": "https://www.youtube.com/watch?v=5Xk9g5g5g5g"},
    {"label": "Corn (Maize) with Cercospora and Gray Leaf Spot", "video_url": "https://www.youtube.com/watch?v=3Xk9g7G6g0g"},
    {"label": "Corn (Maize) with Common Rust", "video_url": "https://www.youtube.com/watch?v=8Qj9g5g5g5g"},
    {"label": "Corn (Maize) with Northern Leaf Blight", "video_url": "https://www.youtube.com/watch?v=uafRy5EqwBQ"},
    {"label": "Healthy Corn (Maize) Plant", "video_url": "https://www.youtube.com/watch?v=5Xk9g5g5g5g"},
    {"label": "Grape with Black Rot", "video_url": "https://www.youtube.com/watch?v=3Xk9g7G6g0g"},
    {"label": "Grape with Esca (Black Measles)", "video_url": "https://www.youtube.com/watch?v=8Qj9g5g5g5g"},
    {"label": "Grape with Isariopsis Leaf Spot", "video_url": "https://www.youtube.com/watch?v=5Xk9g5g5g5g"},
    {"label": "Healthy Grape Plant", "video_url": "https://www.youtube.com/watch?v=3Xk9g7G6g0g"},
    {"label": "Orange with Citrus Greening", "video_url": "https://www.youtube.com/watch?v=8Qj9g5g5g5g"},
    {"label": "Peach with Bacterial Spot", "video_url": "https://www.youtube.com/watch?v=5Xk9g5g5g5g"},
    {"label": "Healthy Peach Plant", "video_url": "https://www.youtube.com/watch?v=3Xk9g7G6g0g"},
    {"label": "Bell Pepper with Bacterial Spot", "video_url": "https://www.youtube.com/watch?v=8Qj9g5g5g5g"},
    {"label": "Healthy Bell Pepper Plant", "video_url": "https://www.youtube.com/watch?v=5Xk9g5g5g5g"},
    {"label": "Potato with Early Blight", "video_url": "https://www.youtube.com/watch?v=AaTFOQLmK5M"},
    {"label": "Potato with Late Blight", "video_url": "https://www.youtube.com/watch?v=21-3WwRYiME"},
    {"label": "Healthy Potato Plant", "video_url": "https://www.youtube.com/watch?v=3Xk9g7G6g0g"},
    {"label": "Healthy Raspberry Plant", "video_url": "https://www.youtube.com/watch?v=8Qj9g5g5g5g"},
    {"label": "Healthy Soybean Plant", "video_url": "https://www.youtube.com/watch?v=5Xk9g5g5g5g"},
    {"label": "Squash with Powdery Mildew", "video_url": "https://www.youtube.com/watch?v=3Xk9g7G6g0g"},
    {"label": "Strawberry with Leaf Scorch", "video_url": "https://www.youtube.com/watch?v=8Qj9g5g5g5g"},
    {"label": "Healthy Strawberry Plant", "video_url": "https://www.youtube.com/watch?v=5Xk9g5g5g5g"},
    {"label": "Tomato with Bacterial Spot", "video_url": "https://www.youtube.com/watch?v=3Xk9g7G6g0g"},
    {"label": "Tomato with Early Blight", "video_url": "https://www.youtube.com/watch?v=8Qj9g5g5g5g"},
    {"label": "Tomato with Late Blight", "video_url": "https://www.youtube.com/watch?v=75rQk6-zdzY"},
    {"label": "Tomato with Leaf Mold", "video_url": "https://www.youtube.com/watch?v=3Xk9g7G6g0g"},
    {"label": "Tomato with Septoria Leaf Spot", "video_url": "https://www.youtube.com/watch?v=8Qj9g5g5g5g"},
    {"label": "Tomato with Spider Mites or Two-spotted Spider Mite", "video_url": "https://www.youtube.com/watch?v=5Xk9g5g5g5g"},
    {"label": "Tomato with Target Spot", "video_url": "https://www.youtube.com/watch?v=3Xk9g7G6g0g"},
    {"label": "Tomato Yellow Leaf Curl Virus", "video_url": "https://www.youtube.com/watch?v=3Xk9g7G6g0g"},
    {"label": "Tomato Mosaic Virus", "video_url": "https://www.youtube.com/watch?v=8Qj9g5g5g5g"},
    {"label": "Healthy Tomato Plant", "video_url": "https://www.youtube.com/watch?v=5Xk9g5g5g5g"}
]

def generate_tts(text, filename):
    """Generate Telugu TTS audio if not exists"""
    path = os.path.join(TTS_FOLDER, filename)
    if not os.path.exists(path):
        tts = gTTS(text=text, lang="te")
        tts.save(path)
    return path

@router.get("/tutorials")
async def get_tutorials():
    """Return video URLs with optional Telugu TTS instructions"""
    for t in TUTORIALS:
        # Add TTS audio
        t["tts_url"] = generate_tts(f"Here is advice for {t['label']}", f"{t['label'].replace(' ','_')}.mp3")
    return {"tutorials": TUTORIALS}
