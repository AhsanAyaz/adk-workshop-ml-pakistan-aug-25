import os

from dotenv import load_dotenv
from google.adk.agents import Agent, ParallelAgent, SequentialAgent

load_dotenv()

# Research Agent (runs first)
research_agent = Agent(
    name="ProductResearcher",
    model="gemini-2.0-flash",
    instruction="Research the given product and provide market insights.",
    output_key="research_data",
)

# Parallel Content Creators
social_media_agent = Agent(
    name="SocialMediaExpert",
    model="gemini-2.0-flash",
    instruction="""
    Create social media content based on research:
    - Instagram caption with hashtags
    - Twitter thread (3 tweets)
    - LinkedIn post

    Research: {{research_data}}
    """,
    output_key="social_content",
)

email_agent = Agent(
    name="EmailExpert",
    model="gemini-2.0-flash",
    instruction="""
    Create email marketing content based on research:
    - Subject lines (5 options)
    - Email body (150 words)
    - Call-to-action options

    Research: {{research_data}}
    """,
    output_key="email_content",
)

ad_agent = Agent(
    name="AdExpert",
    model="gemini-2.0-flash",
    instruction="""
    Create advertising content based on research:
    - Google Ads headlines (3 options)
    - Facebook ad copy
    - Display ad taglines

    Research: {{research_data}}
    """,
    output_key="ad_content",
)

# Parallel execution for content creation
parallel_creators = ParallelAgent(
    name="ContentCreators",
    sub_agents=[social_media_agent, email_agent, ad_agent],
    description="Create multiple types of marketing content simultaneously",
)

# Combine everything
root_agent = SequentialAgent(
    name="MarketingCampaignGenerator",
    description="Research product then create all marketing materials in parallel",
    sub_agents=[research_agent, parallel_creators],
)
