from langgraph.graph import StateGraph, END
from src.agents.researcher.researcher import ResearcherState, inject_researcher_prompt, invoke_researcher_llm_node, invoke_researcher_tool_node
from src.agents.generic_actions import has_tool_calls

graph = StateGraph(ResearcherState)

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