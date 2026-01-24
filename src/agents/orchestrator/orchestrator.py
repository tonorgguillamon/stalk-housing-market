from langchain_openai import ChatOpenAI
from src.agents.llm_roles import LLM_Orchestrator
from src.prompts import AGENT_ORCHESTRATOR
from typing import TypedDict, List
from src.agents.orchestrator.tools import run_data_extractor_agent_tool, run_researcher_agent_tool
from langchain_core.messages import AnyMessage, SystemMessage,ToolMessage, AIMessage

from dotenv import load_dotenv

load_dotenv()

TOOLS = {
    "run_researcher_agent": run_researcher_agent_tool,
    "run_data_extractor_agent": run_data_extractor_agent_tool
}


class OrchestratorState(TypedDict):
    messages: list[AnyMessage]
    research_context: str | None
    market_data: dict | None

def inject_orchestrator_prompt(state: OrchestratorState):
    return {
        "messages": [
            SystemMessage(content=AGENT_ORCHESTRATOR)
        ] + state["messages"]
    }

async def invoke_orchestrator_llm_node(state: OrchestratorState):
    response = await LLM_Orchestrator.ainvoke(state["messages"])
    return {"messages": state["messages"] + [response]}

def needs_more_work(state: OrchestratorState) -> bool:
    last = state["messages"][-1]
    return isinstance(last, AIMessage) and bool(last.tool_calls)

async def invoke_orchestrator_tools_node(state: OrchestratorState):
    last = state["messages"][-1]

    if not isinstance(last, AIMessage) or not last.tool_calls:
        return state

    tool_messages = []
    updates = {}

    for call in last.tool_calls:
        tool_fn = TOOLS[call["name"]]
        result = await tool_fn.ainvoke(call["args"])

        if call["name"] == "run_researcher_agent":
            updates["research_context"] = result

        if call["name"] == "run_data_extractor_agent":
            updates["market_data"] = result

        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=call["id"]
            )
        )

    return {
        "messages": state["messages"] + tool_messages,
        **updates,
    }
