from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from src.database.engine import AsyncSessionLocal
from src.database.operations import get_accommodations, get_accommodation_stats, get_price_distribution
from src.database.models import SearchFilters, StatsInputs, PriceDistributionInput, AccommodationOut

async def get_accommodations_tool(
        **kwargs,
    ):
    async with AsyncSessionLocal() as session:
        filters = SearchFilters(**kwargs)
        results = await get_accommodations(session, filters)
    return [AccommodationOut.model_validate(r).model_dump() for r in results]


async def get_accommodation_stats_tool(**kwargs):
    filters = StatsInputs(**kwargs)
    async with AsyncSessionLocal() as session:
        stats = await get_accommodation_stats(session, filters, filters.metric)
    return stats

async def get_price_distribution_tool(**kwargs):
    input_data = PriceDistributionInput(**kwargs)
    async with AsyncSessionLocal() as session:
        result = await get_price_distribution(
            session=session,
            buckets=input_data.buckets,
            filters=input_data,
            group_by_neighborhood=input_data.group_by_neighborhood,
        )
    return result

search_accommodations_tool = StructuredTool(
    name="search_accommodations_tool",
    func=get_accommodations_tool,
    args_schema=SearchFilters,
    description=(
        "Searches real estate listings using structured filters.\n\n"
        "Use this tool when the user asks to:\n"
        "- See or list available properties\n"
        "- Browse apartments or houses\n"
        "- Filter listings by location, price, rooms, or features\n\n"
        "Examples:\n"
        "- 'Show me apartments under 1,200€ in Madrid'\n"
        "- 'List new developments with terrace'\n"
        "- 'What flats are available in Gràcia?'"
    ),
)


extract_accommodation_stats_tool = StructuredTool(
    name="get_accommodation_stats_tool",
    func=get_accommodation_stats_tool,
    args_schema=StatsInputs,
    description=(
        "Computes aggregate statistics over real estate listings.\n\n"
        "Use this tool when the user asks for:\n"
        "- Counts (how many listings)\n"
        "- Average, minimum, maximum, or median prices\n"
        "- Price per square meter statistics\n\n"
        "Examples:\n"
        "- 'How many flats are under 1,000€?'\n"
        "- 'What is the average price in this neighborhood?'\n"
        "- 'Max price of houses in this area'"
    ),
)


extract_price_distribution_tool = StructuredTool(
    name="get_price_distribution_tool",
    func=get_price_distribution_tool,
    args_schema=PriceDistributionInput,
    description=(
        "Computes how many listings fall into different price ranges.\n\n"
        "Use this tool when the user asks to:\n"
        "- Compare price ranges (e.g. under 1000 vs 1000–1500)\n"
        "- Analyze market distribution\n"
        "- Compare prices across neighborhoods\n\n"
        "Examples:\n"
        "- 'How many flats under 1000 vs 1000–1500?'\n"
        "- 'Compare price ranges by neighborhood'\n"
        "- 'Show price distribution for apartments'"
    ),
)
