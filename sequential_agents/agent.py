import os

from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool


load_dotenv()

# Agent 1: Research
research_agent = Agent(
    name="Researcher",
    model="gemini-2.0-flash",
    instruction="""
    You are a market researcher. Who will use google search to analyze the given product and provide:
    1. Target audience
    2. Market positioning
    3. Key benefits
    Keep it concise and actionable. Use the google_search tool to gather information if needed.
    """,
    tools=[google_search],
    output_key="research_results",
)

# Agent 2: Messaging
messaging_agent = Agent(
    name="MessagingStrategist",
    model="gemini-2.0-flash",
    instruction="""
    Based on the research results, create:
    1. Main value proposition
    2. Key messaging points (3-5 points)
    3. Tagline options (3 options)

    Research: {{research_results}}
    """,
    output_key="messaging_strategy",
)

# Agent 3: Content Creator
content_agent = Agent(
    name="ContentCreator",
    model="gemini-2.0-flash",
    instruction="""
    Create marketing content based on the messaging strategy:
    1. Social media post
    2. Email subject line
    3. Ad copy (50 words max)

    Strategy: {{messaging_strategy}}
    """,
)

# Sequential workflow
root_agent = SequentialAgent(
    name="MarketingPipeline",
    description="Complete marketing content creation pipeline",
    sub_agents=[research_agent, messaging_agent, content_agent],
)
