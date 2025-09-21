# client.py
import os
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("Please set OPENAI_API_KEY in your environment")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

# ---- Custom API Wrappers (hardcoded, no MCP) ----
def get_alerts(state: str):
    resp = requests.get(f"{BASE_URL}/alerts/{state}")
    resp.raise_for_status()
    return resp.json()

def get_forecast(latitude: float, longitude: float):
    resp = requests.get(f"{BASE_URL}/forecast", params={"latitude": latitude, "longitude": longitude})
    resp.raise_for_status()
    return resp.json()

# ---- Orchestration with LLM ----
def ask_llm(user_query: str):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_alerts",
                "description": "Get weather alerts for a state code (e.g. CA, NY)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "state": {"type": "string"}
                    },
                    "required": ["state"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_forecast",
                "description": "Get forecast for given coordinates",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "latitude": {"type": "number"},
                        "longitude": {"type": "number"}
                    },
                    "required": ["latitude", "longitude"]
                }
            }
        }
    ]

    # Initial request to LLM
    resp = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": user_query}],
        tools=tools,
        tool_choice="auto"
    )

    msg = resp.choices[0].message
    if msg.tool_calls:
        results = []
        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            if fn_name == "get_alerts":
                result = get_alerts(args["state"])
            elif fn_name == "get_forecast":
                result = get_forecast(args["latitude"], args["longitude"])
            else:
                result = {"error": "Unknown function"}
            results.append({"tool_call_id": tool_call.id, "content": json.dumps(result)})

        # Pass results back to LLM
        followup = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "user", "content": user_query},
                msg,
                *[{"role": "tool", **r} for r in results]
            ]
        )
        return followup.choices[0].message.content
    else:
        return msg.content


if __name__ == "__main__":
    print("User: Give me alerts for CA and forecast for NYC")
    answer = ask_llm("Give me alerts for CA and forecast for NYC (40.7,-74.0)")
    print("Assistant:", answer)
