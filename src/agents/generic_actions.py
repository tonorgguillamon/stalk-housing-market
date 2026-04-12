from typing import TypedDict, List
from langchain_core.messages import AnyMessage, SystemMessage,ToolMessage, AIMessage
import inspect

class AgentState(TypedDict):
    messages: List[AnyMessage] # AnyMessage is a union type: SystemMessage, HumanMessage, AIMessage, ToolMessage

def has_tool_calls(state):
    last = state["messages"][-1]
    return isinstance(last, AIMessage) and bool(last.tool_calls)

def inject_prompt(state, agent_prompt):
    return {
        "messages": [
            SystemMessage(content=agent_prompt)
        ] + state["messages"]
    }

async def invoke_llm_node(state, LLM_agent):
    response = await LLM_agent.ainvoke(state["messages"])
    return {"messages": state["messages"] + [response]}

async def invoke_tool_node(state, toolbox: dict[str]):
    last = state["messages"][-1]
    tool_messages = []

    if not isinstance(last, AIMessage):
        return state

    if not last.tool_calls:
        return state

    for call in last.tool_calls:
        tool_instance = toolbox[call["name"]]
        
        if not tool_instance:
            # unknown tool
            tool_messages.append(
                ToolMessage(
                    content=f"Error: Unknown tool {call['name']}",
                    tool_call_id=call["id"]
                )
            )
            continue
        
        if hasattr(tool_instance, "ainvoke") and inspect.iscoroutinefunction(tool_instance.ainvoke):
            result = await tool_instance.ainvoke(call["args"])
        else:
            result = tool_instance.invoke(call["args"])

        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=call["id"]
            )
        )

    return {"messages": state["messages"] + tool_messages}