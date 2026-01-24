from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from src.agents.data_extractor.data_extractor import DataExtractorState, inject_data_extractor_prompt, invoke_data_extractor_llm_node, invoke_data_extractor_tool_node
from langchain_core.messages import HumanMessage
from src.agents.generic_actions import has_tool_calls

graph = StateGraph(DataExtractorState)

# system prompt -> llm -> decides what to do: END or calling tools -> if tools were called, now it goes to llm to allow iteration
graph.add_node("init", inject_data_extractor_prompt)
graph.add_node("llm", invoke_data_extractor_llm_node)
graph.add_node("tools", invoke_data_extractor_tool_node)

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

data_extractor_graph = graph.compile()