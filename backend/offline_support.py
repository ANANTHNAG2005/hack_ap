from fastapi import APIRouter
import os
import json

router = APIRouter()

LABELS_FILE = os.path.join(os.path.dirname(__file__), "labels.json")
TUTORIALS_FILE = os.path.join(os.path.dirname(__file__), "tutorials.json")
CACHE_FILE = os.path.join(os.path.dirname(__file__), "offline_cache.json")

def load_labels():
    with open(LABELS_FILE, "r") as f:
        return json.load(f)

def load_tutorials():
    with open(TUTORIALS_FILE, "r") as f:
        return json.load(f)

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)

    labels_data = load_labels()
    tutorials_data = load_tutorials()

    recent_remedies = [{"label": val["label"], "advice": val["advice"]} for val in labels_data.values()][:20]
    recent_tutorials = [{"label": val["label"], "video_url": val["video_url"]} for val in tutorials_data.values()][:20]

    cache = {"recent_remedies": recent_remedies, "recent_tutorials": recent_tutorials}

    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

    return cache

def update_cache(remedy=None, tutorial=None):
    cache = load_cache()
    if remedy:
        cache["recent_remedies"].insert(0, remedy)
        cache["recent_remedies"] = cache["recent_remedies"][:20]
    if tutorial:
        cache["recent_tutorials"].insert(0, tutorial)
        cache["recent_tutorials"] = cache["recent_tutorials"][:20]
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

@router.get("/offline_data")
async def offline_data():
    return load_cache()
