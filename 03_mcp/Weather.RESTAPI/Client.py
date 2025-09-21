# client.py
import requests

BASE_URL = "http://localhost:8000"

def get_alerts(state: str):
    url = f"{BASE_URL}/alerts/{state}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def get_forecast(latitude: float, longitude: float):
    url = f"{BASE_URL}/forecast"
    resp = requests.get(url, params={"latitude": latitude, "longitude": longitude})
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    # Example usage
    alerts = get_alerts("CA")
    print("Weather Alerts for CA:", alerts)

    forecast = get_forecast(40.7, -74.0)
    print("Forecast for NYC (40.7,-74.0):", forecast)
