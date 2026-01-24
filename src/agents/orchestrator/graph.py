"""
User
 ↓
Orchestrator Agent (LLM)
 ↓ chooses via tools (the end-tools are abstract to the orchestrator. This agents doesn't need to understand how they work)
 ├─ run_researcher() --> Researcher Graph --> web tools
 ├─ run_data_extractor() --> Data Graph --> API + DB
 └─ run_analyst() --> Analyst Graph --> scoring
"""
from langgraph.graph import StateGraph, END
from src.agents.orchestrator.orchestrator import needs_more_work, inject_orchestrator_prompt, invoke_orchestrator_llm_node, invoke_orchestrator_tools_node, OrchestratorState

graph = StateGraph(OrchestratorState)

graph.add_node("init", inject_orchestrator_prompt)
graph.add_node("llm", invoke_orchestrator_llm_node)
graph.add_node("tools", invoke_orchestrator_tools_node)

graph.set_entry_point("init")
graph.add_edge("init", "llm")

graph.add_conditional_edges(
    "llm",
    needs_more_work,
    {
        True: "tools",
        False: END,
    },
)

graph.add_edge("tools", "llm")

orchestrator_graph = graph.compile()