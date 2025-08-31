# Building Your First AI Agent with Google ADK & Vertex AI

## TensorFlow User Group Islamabad - AI Study Jams Day 3 Workshop

Welcome to this hands-on 1-hour workshop where you'll learn to build, deploy, and visualize AI agents using Google's Agent Development Kit (ADK) and Vertex AI.

## 📋 Table of Contents

1. [Prerequisites & Setup](#prerequisites--setup) (5 min)
2. [Part 1: Single AI Agent](#part-1-single-ai-agent) (10 min)
3. [Part 2: Sequential Agents](#part-2-sequential-agents) (10 min)
4. [Part 3: Parallel Agents](#part-3-parallel-agents) (10 min)
5. [Part 4: Tool Integration](#part-4-tool-integration) (10 min)
6. [Part 5: Deployment](#part-5-deployment) (10 min)
7. [Part 6: Frontend with ADK Nexus](#part-6-frontend-with-adk-nexus) (5 min)

---

## Prerequisites & Setup

### What You Need

- Python 3.7+ installed
- Google Cloud account (free tier is sufficient)
- Google API key from [AI Studio](https://aistudio.google.com/)

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/your-repo/ai-agents-google-adk
cd ai-agents-google-adk

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

---

## Part 1: Single AI Agent

Let's start by creating our first AI agent that can help with marketing tasks.

### Create Your First Agent

Create a new folder `workshop/simple_agent/` and add `agent.py`:

```python
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
    """
)
```

### Test Your Agent

```bash
# Start the ADK web interface
adk web

# Navigate to localhost:8000 in your browser
# Select 'workshop/simple_agent' from the dropdown
# Try: "Create a tagline for a sustainable coffee brand"
```

**Expected Output**: The agent should provide creative marketing suggestions.

---

## Part 2: Sequential Agents

Now let's create multiple agents that work in sequence - each agent passes its output to the next.

### Create Sequential Workflow

Create `workshop/sequential_agents/agent.py`:

```python
import os
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent

load_dotenv()

# Agent 1: Research
research_agent = Agent(
    name="Researcher",
    model="gemini-2.0-flash",
    instruction="""
    You are a market researcher. Analyze the given product and provide:
    1. Target audience
    2. Market positioning
    3. Key benefits
    Keep it concise and actionable.
    """,
    output_key="research_results"
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
    output_key="messaging_strategy"
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
    """
)

# Sequential workflow
root_agent = SequentialAgent(
    name="MarketingPipeline",
    description="Complete marketing content creation pipeline",
    sub_agents=[research_agent, messaging_agent, content_agent]
)
```

### Test Sequential Agents

```bash
adk web
# Select 'workshop/sequential_agents'
# Try: "Create marketing content for eco-friendly water bottles"
```

Watch how each agent processes the output from the previous one!

---

## Part 3: Parallel Agents

Sometimes you want agents to work simultaneously on different aspects of the same problem.

### Create Parallel Workflow

Create `workshop/parallel_agents/agent.py`:

```python
import os
from dotenv import load_dotenv
from google.adk.agents import Agent, ParallelAgent, SequentialAgent

load_dotenv()

# Research Agent (runs first)
research_agent = Agent(
    name="ProductResearcher",
    model="gemini-2.0-flash",
    instruction="Research the given product and provide market insights.",
    output_key="research_data"
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
    output_key="social_content"
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
    output_key="email_content"
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
    output_key="ad_content"
)

# Parallel execution for content creation
parallel_creators = ParallelAgent(
    name="ContentCreators",
    sub_agents=[social_media_agent, email_agent, ad_agent],
    description="Create multiple types of marketing content simultaneously"
)

# Combine everything
root_agent = SequentialAgent(
    name="MarketingCampaignGenerator",
    description="Research product then create all marketing materials in parallel",
    sub_agents=[research_agent, parallel_creators]
)
```

### Test Parallel Agents

```bash
adk web
# Select 'workshop/parallel_agents'
# Try: "Create a complete marketing campaign for a new fitness app"
```

Notice how the three content agents run simultaneously after research completes!

---

## Part 4: Tool Integration

Let's add tools to make our agents more powerful. Tools are Python functions that agents can call.

### Create Agent with Tools

Create `workshop/tools_agent/agent.py`:

```python
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from google.adk.agents import Agent

load_dotenv()

def get_current_date() -> dict:
    """Get the current date and time"""
    return {
        "current_date": datetime.now().strftime("%Y-%m-%d"),
        "current_time": datetime.now().strftime("%H:%M:%S")
    }

def get_weather_data(city: str = "Islamabad") -> dict:
    """Get current weather for a city (mock data for demo)"""
    # In real implementation, you'd call a weather API
    return {
        "city": city,
        "temperature": "25°C",
        "condition": "Sunny",
        "humidity": "60%"
    }

def calculate_marketing_budget(revenue: float, percentage: float = 10.0) -> dict:
    """Calculate recommended marketing budget based on revenue"""
    budget = revenue * (percentage / 100)
    return {
        "revenue": revenue,
        "percentage": percentage,
        "recommended_budget": budget,
        "monthly_budget": budget / 12
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
    """
)
```

### Test Tools

```bash
adk web
# Select 'workshop/tools_agent'
# Try: "What's today's date and help me plan a seasonal campaign?"
# Try: "If my startup has $100,000 revenue, what should my marketing budget be?"
```

Watch the agent use tools to provide more accurate information!

---

## Part 5: Deployment

Now let's deploy our agent to Google Cloud so others can access it.

### Prepare for Deployment

1. **Authenticate with Google Cloud**:

```bash
# Login to Google Cloud
gcloud auth application-default login

# Set your project (replace with your actual project ID)
gcloud config set project your_project_id
```

2. **Enable required APIs**:

```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Enable Cloud Storage API (for staging)
gcloud services enable storage.googleapis.com
```

3. **Create a Cloud Storage bucket** (for staging files):

```bash
# Replace with your unique bucket name and project ID
gsutil mb gs://your-unique-bucket-name-for-agents
```

4. **Install additional dependencies**:

```bash
pip install "google-cloud-aiplatform[adk,agent_engines]" cloudpickle
```

5. **Create deployment configuration** in `workshop/deploy_agent/`:

Create `.env` file:

```env
GOOGLE_API_KEY=your_api_key
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your_project_id
STAGING_BUCKET=gs://your-unique-bucket-name-for-agents
```

Create `agent.py` (copy your best agent from previous steps):

```python
# Use your favorite agent from the previous steps
# For example, the sequential agents or tools agent
```

### Deploy to Vertex AI

```bash
# Navigate to your agent directory
cd workshop/deploy_agent

# Initialize Vertex AI (this sets up the staging bucket)
python -c "import vertexai; vertexai.init(project='your_project_id', location='us-central1', staging_bucket='gs://your-unique-bucket-name-for-agents')"

# Deploy using ADK CLI
adk deploy --agent-path . --gcp-project your_project_id --gcp-region us-central1

# This will return a RESOURCE_ID - save this!
```

The deployment process will:

1. Package your agent code
2. Upload to Google Cloud
3. Create a Vertex AI Agent Engine resource
4. Return a resource ID for access

---

## Part 6: Frontend with ADK Nexus

Now let's create a beautiful web interface for your deployed agent using ADK Nexus.

### What is ADK Nexus?

ADK Nexus is an open-source Streamlit chatbot interface that connects to your deployed Vertex AI agents. It provides:

- Beautiful chat interface
- Easy deployment to Streamlit Cloud
- Secure authentication
- Customizable branding

### Quick Setup

1. **Clone ADK Nexus**:

```bash
git clone https://github.com/iomechs/adk-nexus.git
cd adk-nexus
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Configure your agent**:

```bash
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:

```toml
RESOURCE_ID = "your-deployed-agent-resource-id"
LOCATION = "us-central1"
CHATBOT_NAME = "My Marketing Assistant"

[gcp_service_account]
# Add your service account JSON here (converted to TOML format)
type = "service_account"
project_id = "your-project-id"
# ... other service account fields
```

4. **Run locally**:

```bash
streamlit run app.py
```

5. **Test online instantly**: Visit [adk-nexus.dev.iomechs.com](http://adk-nexus.dev.iomechs.com) and enter your agent credentials in the modal.

### Deploy Your Frontend

1. **Push to GitHub**: Create a new repository with your ADK Nexus code
2. **Deploy to Streamlit Cloud**:
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - Connect your GitHub repo
   - Set main file to `app.py`
   - Copy your `secrets.toml` content to the secrets section
   - Deploy!

Your agent now has a professional web interface that anyone can access!

---

## 🎉 Workshop Complete!

In just 1 hour, you've learned to:

✅ **Create a single AI agent** with custom instructions  
✅ **Build sequential workflows** where agents pass data between each other  
✅ **Implement parallel processing** for simultaneous task execution  
✅ **Add tool integration** for enhanced capabilities  
✅ **Deploy to Google Cloud** for production access  
✅ **Create a beautiful frontend** with ADK Nexus

## What's Next?

### Immediate Actions

1. **Experiment**: Try different agent combinations and tools
2. **Customize**: Modify ADK Nexus styling and branding
3. **Share**: Send your deployed chatbot link to colleagues

### Advanced Learning

- Add custom tools for your specific domain
- Implement RAG (Retrieval-Augmented Generation) for knowledge bases
- Explore multi-modal capabilities (text + images)
- Build complex workflows with conditional logic

### Resources

- **Google ADK Docs**: [Cloud Agent Development Kit](https://cloud.google.com/agent-development-kit)
- **ADK Nexus**: [github.com/iomechs/adk-nexus](https://github.com/iomechs/adk-nexus)
- **Community**: Follow [bit.ly/TFUGIslamabad](http://bit.ly/TFUGIslamabad)

---

## Troubleshooting

**Can't see agent in ADK Web?**

- Check your folder structure matches the examples
- Ensure `root_agent` is defined in `agent.py`

**Deployment fails?**

- Verify Google Cloud project ID and permissions
- Check that required APIs are enabled

**ADK Nexus connection issues?**

- Verify RESOURCE_ID matches your deployed agent
- Ensure service account has Vertex AI User role

---

**From concept to deployment in 60 minutes!** 🚀

_Workshop created by Muhammad Ahsan Ayaz for TensorFlow User Group Islamabad_  
_Follow us: [bit.ly/TFUGIslamabad](http://bit.ly/TFUGIslamabad)_
