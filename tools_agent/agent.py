import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()


def get_current_date() -> dict:
    """Get the current date and time"""
    return {
        "current_date": datetime.now().strftime("%Y-%m-%d"),
        "current_time": datetime.now().strftime("%H:%M:%S"),
    }


def get_weather_data(city: str = "Islamabad") -> dict:
    """Get current weather for a city (mock data for demo)"""
    # In real implementation, you'd call a weather API
    return {
        "city": city,
        "temperature": "25°C",
        "condition": "Sunny",
        "humidity": "60%",
    }


def calculate_marketing_budget(revenue: float, percentage: float = 10.0) -> dict:
    """Calculate recommended marketing budget based on revenue"""
    budget = revenue * (percentage / 100)
    return {
        "revenue": revenue,
        "percentage": percentage,
        "recommended_budget": budget,
        "monthly_budget": budget / 12,
    }


# Agent with tools
root_agent = Agent(
    name="SmartMarketingAssistant",
    model="gemini-2.0-flash",
    description="Marketing assistant with access to helpful tools",
    tools=[get_current_date, get_weather_data, calculate_marketing_budget],
    instruction="""
    You are a smart marketing assistant with access to helpful tools:

    1. get_current_date(): Get current date/time for timely content
    2. get_weather_data(city): Get weather info for location-based marketing
    3. calculate_marketing_budget(revenue, percentage): Calculate marketing budgets

    Use these tools when relevant to provide more accurate and helpful responses.
    Always explain why you're using a particular tool.
    """,
)
