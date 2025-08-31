import os

from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()

# Simple marketing assistant
root_agent = Agent(
    name="MarketingAssistant",
    model="gemini-2.0-flash",
    description="A helpful marketing assistant",
    instruction="""
    You are a marketing expert who helps create compelling marketing content.
    Be creative, professional, and provide actionable advice.
    """,
)
