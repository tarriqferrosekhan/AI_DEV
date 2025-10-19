import os
from typing import Any
from dotenv import load_dotenv
from fastapi import FastAPI
import httpx
from mcp.server.fastmcp import FastMCP
import os
new_title = "WeatherServer"
os.system(f"title {new_title}")

def getCurrentFileName():
    current_file_path = __file__
    file_name_with_extension = os.path.basename(current_file_path)
    file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
    #print("file_name_without_extension",file_name_without_extension)
    return file_name_without_extension

filenameforconfig=getCurrentFileName().lower().strip().replace(" ","")
#print("filenameforconfig=",filenameforconfig)
env_file_name=".env.mcp."+filenameforconfig
#print("env_file_name=",os.getcwd()+"\\"+env_file_name.strip())
load_dotenv(os.getcwd()+"\\"+env_file_name,override=True)

BASE_URL=os.getenv("BASE_URL")
SERVER_MODE=os.getenv("SERVER_MODE")#,"SSE"
SERVER_HOST=os.getenv("SERVER_HOST")#,"127.0.0.1"
SERVER_PORT=os.getenv("SERVER_PORT")#8000
#print(BASE_URL,SERVER_MODE,SERVER_HOST,SERVER_PORT)

# Initialize FastMCP server
mcp = FastMCP("weather")
app=FastAPI()
# Constants
NWS_API_BASE = BASE_URL
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

@app.get("/")
async def healthcheck():
    return {"status": "ok", "message": "MCP Weather Server running with SSE transport"}

if __name__ == "__main__":
    mcp.settings.host=SERVER_HOST
    mcp.settings.port=int(str(SERVER_PORT))
    mcp.run(transport=SERVER_MODE)