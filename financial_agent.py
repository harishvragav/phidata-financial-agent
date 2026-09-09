import os
from dotenv import load_dotenv

from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

load_dotenv()

# Active Groq model
MODEL_ID = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Agent 1: Web search
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for information and provide sources",
    model=Groq(id=MODEL_ID),
    tools=[DuckDuckGo()],
    instructions=[
        "Always include sources.",
    ],
    show_tool_calls=True,
    markdown=True,
)

# Agent 2: Finance data
finance_agent = Agent(
    name="Finance AI Agent",
    role="Retrieve stock information and analyst recommendations",
    model=Groq(id=MODEL_ID),
    tools=[
        YFinanceTools(
            analyst_recommendations=True,
            company_news=True,
            technical_indicators=True,
        )
    ],
    instructions=[
        "Use tables to display financial data.",
    ],
    show_tool_calls=True,
    markdown=True,
)

# Team agent
multi_ai_agent = Agent(
    team=[web_search_agent, finance_agent],
    model=Groq(id=MODEL_ID),
    instructions=[
        "Use the web search agent for current company news.",
        "Use the finance agent for analyst recommendations and market data.",
        "Always include sources.",
        "Use tables when presenting financial data.",
    ],
    show_tool_calls=True,
    markdown=True,
)

if __name__ == "__main__":
    multi_ai_agent.print_response(
        "Summarize analyst recommendations and share the latest news for NVIDIA (NVDA).",
        stream=True,
    )