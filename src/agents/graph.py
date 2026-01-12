from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from src.agents.researcher import ResearcherState, inject_researcher_prompt, invoke_researcher_llm_node, invoke_researcher_tool_node
from langchain_core.messages import HumanMessage, AIMessage

graph = StateGraph(ResearcherState)

def has_tool_calls(state: ResearcherState):
    last = state["messages"][-1]
    return isinstance(last, AIMessage) and bool(last.tool_calls)

# system prompt -> llm -> decides what to do: END or calling tools -> if tools were called, now it goes to llm to allow iteration
graph.add_node("init", inject_researcher_prompt)
graph.add_node("llm", invoke_researcher_llm_node)
graph.add_node("tools", invoke_researcher_tool_node)

graph.set_entry_point("init")
graph.add_edge("init", "llm")

graph.add_conditional_edges(
    "llm",
    has_tool_calls,
    {
        True: "tools",
        False: END,
    }
)

graph.add_edge("tools", "llm")

researcher_graph = graph.compile()

# TEST
query = "what do you think about the area of Purta Purchena, in Almeria (Spain)"

final_state = researcher_graph.invoke({
    "messages": [HumanMessage(content=query)]
})

print(final_state)