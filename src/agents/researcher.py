from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import StructuredTool
from src.prompts import AGENT_RESEARCHER
import tools.exploration as exploration
from pydantic import BaseModel, Field

# https://medium.com/pythoneers/building-ai-agent-systems-with-langgraph-9d85537a6326

class ResearcherInvocationInput(BaseModel):
    query: str = Field(
        ...,
        description=(
            "A precise location to research (e.g., 'Malasaña district, Madrid'). "
            "This should be specific enough to support socioeconomic, tourism, "
            "quality-of-life, and taxation analysis."
        )
    )

search_tools = [
    exploration.search_tourism_revenue_tool,
    exploration.search_local_taxes_regulations_tool,
    exploration.search_quality_of_life_tool,
    exploration.search_socioeconomic_indexes_tool
]

agent_researcher = create_agent( # Thought -> Action -> Observation and iterates
    model=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    tools=search_tools,
    system_prompt=AGENT_RESEARCHER
)

def invoke_researcher(query: str):
    result = agent_researcher.invoke(
        {"messages": [HumanMessage(content=query)]}
    )

    # Forward only the final message content
    return result[-1].content

invoke_researcher_tool = StructuredTool(
    name="invoke_researcher",
    func=invoke_researcher,
    args_schema=ResearcherInvocationInput,
    description=(
        "Delegates comprehensive, multi-domain property research to the Researcher Agent.\n\n"
        "Use this tool when analysis requires external knowledge or context not present in the "
        "local property dataset.\n\n"
        "The Researcher Agent performs the following on your behalf:\n"
        "1. Socioeconomic index searches (crime, unemployment, income, population density)\n"
        "2. Local taxes and municipal fee research (IBI, waste management, tourist fees)\n"
        "3. Quality-of-life and sentiment analysis (schools, noise complaints, vibe)\n"
        "4. Tourism market benchmarks (occupancy, ADR, rental density)\n\n"
        "Input must be a precise location such as a neighborhood, district, or small geographic unit. "
        "Returns a consolidated string with all structured raw research results."
    ),
)