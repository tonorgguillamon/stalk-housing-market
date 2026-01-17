from typing import TypedDict, List
import src.tools.exploration as exploration
from src.agents.llm_roles import LLM_Researcher
from src.prompts import AGENT_RESEARCHER
from langchain_core.messages import AnyMessage, SystemMessage,ToolMessage, AIMessage

# https://medium.com/pythoneers/building-ai-agent-systems-with-langgraph-9d85537a6326

TOOLS = {
    "search_tourism_revenue": exploration.search_tourism_revenue_tool,
    "search_local_taxes_regulations": exploration.search_local_taxes_regulations_tool,
    "search_quality_of_life": exploration.search_quality_of_life_tool,
    "search_socioeconomic_indexes": exploration.search_socioeconomic_indexes_tool,
}

class ResearcherState(TypedDict):
    messages: List[AnyMessage] # AnyMessage is a union type: SystemMessage, HumanMessage, AIMessage, ToolMessage

def inject_researcher_prompt(state: ResearcherState):
    return {
        "messages": [
            SystemMessage(content=AGENT_RESEARCHER)
        ] + state["messages"]
    }

async def invoke_researcher_llm_node(state: ResearcherState):
    response = await LLM_Researcher.ainvoke(state["messages"])
    return {"messages": state["messages"] + [response]}

def invoke_researcher_tool_node(state: ResearcherState):
    last = state["messages"][-1]
    tool_messages = []

    if not isinstance(last, AIMessage):
        return state

    if not last.tool_calls:
        return state

    for call in last.tool_calls:
        tool_instance = TOOLS[call["name"]]
        
        if not tool_instance:
            # unknown tool
            tool_messages.append(
                ToolMessage(
                    content=f"Error: Unknown tool {call['name']}",
                    tool_call_id=call["id"]
                )
            )
            continue
        result = tool_instance.invoke(call["args"])

        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=call["id"]
            )
        )

    return {"messages": state["messages"] + tool_messages}