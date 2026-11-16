import os
from strands import Agent
from strands.models import BedrockModel
from strands.vended_tools import http_request  # vended by the SDK (strands_tools.http_request was removed in 0.9.0)
from typing import Dict, Any

# Define a weather-focused system prompt
WEATHER_SYSTEM_PROMPT = """You are a weather assistant with HTTP capabilities. You can:

1. Make HTTP requests to the National Weather Service API
2. Process and display weather forecast data
3. Provide weather information for locations in the United States

When retrieving weather information:
1. First get the coordinates or grid information using https://api.weather.gov/points/{latitude},{longitude} or https://api.weather.gov/points/{zipcode}
2. Then use the returned forecast URL to get the actual forecast

When displaying responses:
- Format weather data in a human-readable way
- Highlight important information like temperature, precipitation, and alerts
- Handle errors appropriately
- Convert technical terms to user-friendly language

Always explain the weather conditions clearly and provide context for the forecast.
"""

def handler(event: Dict[str, Any], _context) -> str:
    # MODEL_ID is set by the CDK stack (defaults to Claude Haiku 5.5, global inference profile)
    model = BedrockModel(model_id=os.environ.get("MODEL_ID", "global.anthropic.claude-haiku-5-5"))

    weather_agent = Agent(
        model=model,
        system_prompt=WEATHER_SYSTEM_PROMPT,
        tools=[http_request],
    )

    response = weather_agent(event.get('prompt'))
    # Claude 4.6+ models can emit a reasoningContent block first, so collect only the text blocks
    return "\n".join(block["text"] for block in response.message["content"] if "text" in block)