from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool
from langchain_core.messages import HumanMessage
from src.agents.researcher.graph import researcher_graph
from src.agents.data_extractor.graph import data_extractor_graph
from langchain_core.messages import AIMessage

class ResearcherAgentInput(BaseModel):
    location: str = Field(
        ...,
        description=(
            "A precise geographic location such as a neighborhood, district, "
            "or city (e.g., 'Malasaña, Madrid')."
        )
    )

class DataExtractorAgentInput(BaseModel):
    location: str = Field(
        ...,
        description="Location to fetch real estate data for."
    )
    operation: str = Field(
        ...,
        description="Transaction type: 'rent' or 'buy'."
    )

def extract_final_answer(state) -> str:
    for msg in reversed(state["messages"]):
        if isinstance(msg, AIMessage):
            return msg.content
    return ""

def run_researcher_agent(location: str) -> str:
    """
    Invoke the Researcher Agent graph and return its final output.
    """
    result = researcher_graph.invoke({
        "messages": [HumanMessage(content=location)]
    })
    return extract_final_answer(result)

def run_data_extractor_agent(location: str, operation: str) -> str:
    """
    Invoke the Data Extractor Agent graph and return raw market data.
    """
    prompt = f"Location: {location}\nOperation: {operation}"

    result = data_extractor_graph.invoke({
        "messages": [HumanMessage(content=prompt)]
    })
    return extract_final_answer(result)

run_researcher_agent_tool = StructuredTool(
    name="run_researcher_agent",
    func=run_researcher_agent,
    args_schema=ResearcherAgentInput,
    description=(
        "Runs the Researcher Agent to gather external contextual information "
        "about a location.\n\n"
        "Use this tool to obtain:\n"
        "- Quality of life indicators\n"
        "- Local regulations and taxes\n"
        "- Tourism pressure and sentiment\n"
        "- Socioeconomic context\n\n"
        "This tool performs web searches and regulatory lookups. "
        "It should be used when external knowledge is required."
    ),
)

run_data_extractor_agent_tool = StructuredTool(
    name="run_data_extractor_agent",
    func=run_data_extractor_agent,
    args_schema=DataExtractorAgentInput,
    description=(
        "Runs the Data Extractor Agent to retrieve real estate market data.\n\n"
        "Use this tool to obtain:\n"
        "- Live listings from Idealista (rent or buy)\n"
        "- Historical price and yield data\n"
        "- Stored market snapshots\n\n"
        "This tool interacts with APIs and databases. "
        "It should be used whenever up-to-date or historical market data is required."
    ),
)

