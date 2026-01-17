from langchain_openai import ChatOpenAI
import src.tools.exploration as exploration
import src.tools.historical_extraction as historical_extraction


LLM_Orchestrator = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

LLM_Researcher = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
    ).bind_tools([
        exploration.search_tourism_revenue_tool,
        exploration.search_local_taxes_regulations_tool,
        exploration.search_quality_of_life_tool,
        exploration.search_socioeconomic_indexes_tool
])

LLM_Data = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
).bind_tools([
    historical_extraction.search_accommodations_tool,
    historical_extraction.extract_price_distribution_tool,
    historical_extraction.extract_accommodation_stats_tool
])

LLM_Analyst = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5
)
