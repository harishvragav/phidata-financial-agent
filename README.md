# Financial AI Agent

A multi-agent Python application that provides:

- Latest company news using DuckDuckGo
- Analyst recommendations using Yahoo Finance
- Technical indicators for stocks
- Consolidated financial responses through Groq LLM

The application contains:

- **Web Search Agent** — Searches the web and provides sources
- **Finance Agent** — Retrieves analyst recommendations, news, and technical data
- **Team Agent** — Delegates work to the appropriate specialist agent and formats the final response

## Prerequisites

Install the following before starting:

- Miniconda or Anaconda
- Python 3.12
- A Groq API key

Create a Groq API key from:

https://console.groq.com/keys

Your Groq key should start with:

```text
gsk_
```

## Project Structure

```text
phidata-financial-agent/
│
├── financial_agent.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Environment Setup

Open PowerShell in the project folder:

```powershell
cd D:\PP\phidata-financial-agent
```

Create a Conda environment inside the project folder:

```powershell
conda create -p venv python=3.12 -y
```

Activate the environment:

```powershell
conda activate .\venv
```

> If `conda activate venv` does not work on Windows, use `conda activate .\venv` because the environment was created with `-p venv`.

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install all required packages:

```powershell
pip install -r requirements.txt
```

## Environment Variables

Create a file named `.env` in the project root.

```text
GROQ_API_KEY=gsk_your_actual_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Do not share your `.env` file or commit it to GitHub.

## Requirements

Create a `requirements.txt` file with:

```text
phidata
groq
python-dotenv
yfinance
duckduckgo-search
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the Application

After activating the environment, run:

```powershell
python financial_agent.py
```

Expected prompt:

```text
Summarize analyst recommendations and share the latest news for NVIDIA (NVDA).
```

The agent will:

1. Delegate financial-data requests to Yahoo Finance
2. Delegate web-news requests to DuckDuckGo
3. Combine the results into a structured Markdown response

## Model Configuration

The original tutorial uses:

```text
llama-3.1-70b-versatile
```

That model has been decommissioned by Groq. Use the model available in your account:

```text
openai/gpt-oss-120b
```

In `financial_agent.py`, use:

```python
MODEL_ID = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
```

Then provide the model consistently to every agent:

```python
model=Groq(id=MODEL_ID)
```

## Verify Available Groq Models

Run this command to see the exact model IDs available to your Groq API key:

```powershell
python -c "from groq import Groq; import os; from dotenv import load_dotenv; load_dotenv(); client = Groq(api_key=os.getenv('GROQ_API_KEY')); print([m.id for m in client.models.list().data])"
```

If `openai/gpt-oss-120b` is unavailable later, choose another general-purpose model from this output, for example:

```text
openai/gpt-oss-20b
groq/compound
groq/compound-mini
```

## Common Errors

### `AuthenticationError` or `401`

Cause: Invalid or missing Groq API key.

Fix:

1. Check that `.env` exists in the project root
2. Confirm the variable name is exactly `GROQ_API_KEY`
3. Confirm the key starts with `gsk_`
4. Restart the terminal after changing environment variables

```env
GROQ_API_KEY=gsk_your_actual_key
```

### `model_decommissioned`

Cause: You are using the old tutorial model:

```text
llama-3.1-70b-versatile
```

Fix: Change it to:

```python
MODEL_ID = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
```

### OpenAI API key error

Cause: The team agent has no model configured, so older Phidata versions use OpenAI by default.

Fix: Set the Groq model explicitly in the team agent:

```python
multi_ai_agent = Agent(
    team=[web_search_agent, finance_agent],
    model=Groq(id=MODEL_ID),
    instructions=[
        "Always include sources.",
        "Use tables to display data.",
    ],
    show_tool_calls=True,
    markdown=True,
)
```

You do not need these lines when your project uses Groq only:

```python
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
```

Remove them from `financial_agent.py`.

## Security

Add this to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```
