# server.py
from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="Weather API")

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str):
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers, timeout=30.0)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None


@app.get("/alerts/{state}")
async def get_alerts(state: str):
    """Get weather alerts for a US state (e.g. /alerts/CA)."""
    url = f"{NWS_API_BASE}/alerts/active/area/{state.upper()}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        raise HTTPException(status_code=500, detail="Unable to fetch alerts")

    if not data["features"]:
        return {"alerts": []}

    alerts = []
    for feature in data["features"]:
        props = feature["properties"]
        alerts.append({
            "event": props.get("event", "Unknown"),
            "area": props.get("areaDesc", "Unknown"),
            "severity": props.get("severity", "Unknown"),
            "description": props.get("description", "No description"),
            "instructions": props.get("instruction", "No instructions")
        })

    return {"alerts": alerts}


@app.get("/forecast")
async def get_forecast(latitude: float, longitude: float):
    """Get weather forecast for given coordinates (e.g. /forecast?latitude=40.7&longitude=-74.0)."""
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)
    if not points_data or "properties" not in points_data:
        raise HTTPException(status_code=500, detail="Unable to fetch location data")

    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)
    if not forecast_data or "properties" not in forecast_data:
        raise HTTPException(status_code=500, detail="Unable to fetch forecast")

    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for p in periods[:5]:  # next 5 periods
        forecasts.append({
            "name": p["name"],
            "temperature": f"{p['temperature']}°{p['temperatureUnit']}",
            "wind": f"{p['windSpeed']} {p['windDirection']}",
            "forecast": p["detailedForecast"]
        })

    return {"forecasts": forecasts}
