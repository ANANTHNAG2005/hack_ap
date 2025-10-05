from fastapi import APIRouter
import json
import os

router = APIRouter()

# Path to seasonal calendar JSON
CALENDAR_FILE = "seasonal_calendar.json"

def load_calendar():
    """Load seasonal calendar from JSON file"""
    if os.path.exists(CALENDAR_FILE):
        with open(CALENDAR_FILE, "r") as f:
            return json.load(f)
    return {}

@router.get("/seasonal_calendar")
async def seasonal_calendar(month: str = None):
    """
    Return a month-wise advisory of preventive organic treatments.
    Optionally, filter by a specific month.
    """
    calendar = load_calendar()

    if month:
        month_title = month.capitalize()
        if month_title in calendar:
            return {month_title: calendar[month_title]}
        else:
            return {"error": f"No data available for month: {month}"}

    return {"calendar": calendar}
