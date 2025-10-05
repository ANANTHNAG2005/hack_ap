from fastapi import APIRouter, Query
import requests

router = APIRouter()

WEATHER_ADVICE = {
    "Clear": "Good weather for planting and crop inspection.",
    "Clouds": "Monitor humidity; ensure proper ventilation.",
    "Rain": "Protect young plants, check for waterlogging, and monitor pests.",
    "Drizzle": "Light rain, check soil moisture and pest risk.",
    "Thunderstorm": "Avoid fieldwork and secure loose plants.",
    "Snow": "Not applicable for tropical crops, protect sensitive plants.",
    "Mist": "Low visibility, check dew and humidity-sensitive crops.",
    "Fog": "Low visibility, inspect for fungal risks."
}

CODE_MAP = {
    0: "Clear", 1: "Clear", 2: "Clouds", 3: "Clouds",
    45: "Mist", 48: "Mist",
    51: "Drizzle", 53: "Drizzle", 55: "Drizzle", 56: "Drizzle", 57: "Drizzle",
    61: "Rain", 63: "Rain", 65: "Rain", 66: "Rain", 67: "Rain",
    71: "Snow", 73: "Snow", 75: "Snow", 77: "Snow",
    80: "Rain", 81: "Rain", 82: "Rain",
    95: "Thunderstorm", 96: "Thunderstorm", 99: "Thunderstorm"
}

def get_coordinates(city_name):
    """Get latitude and longitude from city name using OpenStreetMap Nominatim"""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city_name, "format": "json", "limit": 1}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if not data:
            return None, None
        return float(data[0]["lat"]), float(data[0]["lon"])
    except:
        return None, None

@router.get("/weather_alert/{city}")
async def weather_alert(city: str, lat: float = Query(None), lon: float = Query(None)):
    # Use provided lat/lon if city geocoding fails
    if lat is None or lon is None:
        geolat, geolon = get_coordinates(city)
        if geolat is None or geolon is None:
            # fallback: demo sample weather
            return {
                "location": city,
                "temperature_c": 30,
                "weather": "Clear",
                "alert": "Good weather for planting and crop inspection."
            }
        lat, lon = geolat, geolon

    # Fetch current weather from Open-Meteo
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "current_weather" not in data:
            # fallback sample
            return {
                "location": city,
                "temperature_c": 30,
                "weather": "Clear",
                "alert": "Good weather for planting and crop inspection."
            }

        weather_code = data["current_weather"]["weathercode"]
        temperature = data["current_weather"]["temperature"]

        weather_main = CODE_MAP.get(weather_code, "Unknown")
        advice = WEATHER_ADVICE.get(weather_main, "No specific advice available.")

        return {
            "location": city,
            "temperature_c": temperature,
            "weather": weather_main,
            "alert": advice
        }

    except Exception as e:
        # fallback sample
        return {
            "location": city,
            "temperature_c": 30,
            "weather": "Clear",
            "alert": f"Error fetching weather: {str(e)}"
        }
