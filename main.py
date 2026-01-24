from langchain_core.messages import HumanMessage
from src.agents.orchestrator.graph import orchestrator_graph
import asyncio
from dotenv import load_dotenv

async def main():
    load_dotenv()
    
    result = await orchestrator_graph.ainvoke({
        "messages": [
            HumanMessage(
                content="Analyze investment potential in Malasaña, Madrid"
            )
        ],
        "research_context": None,
        "market_data": None,
    })
    print(result)

if __name__ == '__main__':
    asyncio.run(main())