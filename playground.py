import os

from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.playground import Playground, serve_playground_app
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

load_dotenv()

MODEL_ID = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the information",
    model=Groq(id=MODEL_ID),
    tools=[DuckDuckGo()],
    instructions=[
        "Always include sources."
    ],
    show_tool_calls=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance AI Agent",
    model=Groq(id=MODEL_ID),
    tools=[
        YFinanceTools(
            analyst_recommendations=True,
            company_news=True,
            technical_indicators=True,
        )
    ],
    instructions=[
        "Use tables to display the data."
    ],
    show_tool_calls=True,
    markdown=True,
)

app = Playground(
    agents=[finance_agent, web_search_agent]
).get_app()

if __name__ == "__main__":
    serve_playground_app(
        "playground:app",
        reload=True,
    )