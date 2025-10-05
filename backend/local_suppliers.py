from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter()

OVERPASS_URL = "https://overpass-api.de/api/interpreter"  # Overpass API endpoint

@router.get("/suppliers/")
async def get_suppliers(lat: float, lon: float, radius: int = 5000):
    query = f"""
    [out:json][timeout:25];
    (
      node["shop"~"fertilizer|agriculture|garden|agricultural_supplies|hardware"](around:{radius},{lat},{lon});
      way["shop"~"fertilizer|agriculture|garden|agricultural_supplies|hardware"](around:{radius},{lat},{lon});
      relation["shop"~"fertilizer|agriculture|garden|agricultural_supplies|hardware"](around:{radius},{lat},{lon});
    );
    out center;
    """
    
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.get(OVERPASS_URL, params={"data": query})
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Overpass API error: {str(e)}")

    suppliers = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        name = tags.get("name", "Unknown")
        shop_type = tags.get("shop", "Unknown")
        lat_elem = element.get("lat") or element.get("center", {}).get("lat")
        lon_elem = element.get("lon") or element.get("center", {}).get("lon")

        if lat_elem and lon_elem:
            suppliers.append({
                "name": name,
                "type": shop_type,
                "lat": lat_elem,
                "lon": lon_elem
            })

    if not suppliers:
        return {"count": 0, "message": "No suppliers found nearby. Try increasing radius or check coordinates."}

    return {"count": len(suppliers), "suppliers": suppliers}
