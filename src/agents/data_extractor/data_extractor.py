import asyncio
from typing import TypedDict, List
import src.tools.historical_extraction as historical_extraction
from src.agents.llm_roles import LLM_Data
from src.prompts import AGENT_RESEARCHER, AGENT_DATA_EXTRACTOR
from langchain_core.messages import AnyMessage, SystemMessage,ToolMessage, AIMessage

TOOLS = {
    "search_accommodations": historical_extraction.search_accommodations_tool,
    "get_accommodation_stats": historical_extraction.extract_accommodation_stats_tool,
    "get_price_distribution": historical_extraction.extract_price_distribution_tool,
}

class DataExtractorState(TypedDict):
    messages: List[AnyMessage]

def inject_data_extractor_prompt(state: DataExtractorState):
    return {
        "messages": [
            SystemMessage(content=AGENT_DATA_EXTRACTOR)
        ] + state["messages"]
    }

async def invoke_data_extractor_llm_node(state: DataExtractorState):
    response = await LLM_Data.ainvoke(state["messages"])
    return {"messages": state["messages"] + [response]}

async def invoke_data_extractor_tool_node(state: DataExtractorState):
    last = state["messages"][-1]
    tool_messages = []

    if not isinstance(last, AIMessage):
        return state

    if not last.tool_calls:
        return state

    for call in last.tool_calls:
        tool_instance = TOOLS.get(call["name"])
        
        if not tool_instance:
            # unknown tool
            tool_messages.append(
                ToolMessage(
                    content=f"Error: Unknown tool {call['name']}",
                    tool_call_id=call["id"]
                )
            )
            continue

        result = await tool_instance.ainvoke(call["args"])

        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=call["id"]
            )
        )

    return {"messages": state["messages"] + tool_messages}