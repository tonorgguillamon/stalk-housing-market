from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field
from langchain_tavily import TavilySearch

class QualityOfLifeInput(BaseModel):
    location: str = Field(
        ..., 
        description=(
            "A precise neighborhood, district, or address (e.g. "
            "'Ciudad Jardin neighborhood, Malaga')."
        )
    )

class SocioeconomicIndexesInput(BaseModel):
    location: str = Field(
        ...,
        description=(
            "A precise geographic area (district, city, neighborhood), e.g., "
            "'Lavapies district, Madrid, Spain'."
        )
    )

class TourismRevenueInput(BaseModel):
    location: str = Field(
        ...,
        description=(
            "A specific city or neighborhood (e.g., 'Puerta Purchena, Almeria')."
        )
    )
    property_type: str = Field(
        "apartment",
        description="The type of property to analyze (e.g., apartment, studio, house)."
    )

class LocalTaxesRegulationsInput(BaseModel):
    location: str = Field(
        ...,
        description=(
            "The specific municipality or city council (e.g., 'Seville City Council')."
        )
    )
    property_use_case: str = Field(
        "living",
        description=(
            "The intended use case: 'living', 'residential rental', "
            "'short-term touristic accommodation', etc."
        )
    )


tavily_search = TavilySearch(max_results=20) #, include_raw_content=True)

def search_quality_of_life(location: str):
    query_amenities = (
        f"Ratings and public satisfaction with schools, hospitals, "
        f"and public transport in {location}"
    )
    
    query_vibe = (
        f"Local forum reviews, noise complaints, and bar/restaurant density "
        f"to assess atmosphere in {location}"
    )
    
    query_commercial = (
        f"Average prices in local businesses and hotel/short-term rental "
        f"presence in {location}"
    )

    all_results = []
    all_results.append(tavily_search.invoke({"query": query_amenities}))
    all_results.append(tavily_search.invoke({"query": query_vibe}))
    all_results.append(tavily_search.invoke({"query": query_commercial}))

    return all_results

def search_socioeconomic_indexes(location: str):
    query_criminality_index = f"Official latest crime index in {location}"
    query_unemployment_index = f"Official latest unemployment rates in {location}"
    query_inmigration_index = (
        f"Statistics for immigration data, and country/continent of origin, in {location}"
    )
    query_population_index = (
        f"Population density and average household income in {location}"
    )

    all_results = []
    all_results.append(tavily_search.invoke({"query": query_criminality_index}))
    all_results.append(tavily_search.invoke({"query": query_unemployment_index}))
    all_results.append(tavily_search.invoke({"query": query_inmigration_index}))
    all_results.append(tavily_search.invoke({"query": query_population_index}))

    return all_results

def search_tourism_revenue(location: str, property_type: str = "apartment"):
    full_query = (
        f"Average daily rate and occupancy rate for short-term rental {property_type} "
        f"in {location}. Search for 'Airbnb data' or "
        f"'Booking.com market analysis' for {location}."
    )
    return tavily_search.invoke({"query": full_query})
    
def search_local_taxes_regulations(location: str, property_use_case: str = 'living'):
    query_fixed_fees = (
        f"Official current IBI tax rate and municipal fees (waste management, sewage) "
        f"for {location} City Council"
    )

    query_use_case_regs = (
        f"Specific regulations, licenses, and rental revenue tax implications for "
        f"'{property_use_case}' in the municipality of {location}. Include tourist "
        f"tax regulations if applicable."
    )

    all_results = []
    all_results.append(tavily_search.invoke({"query": query_fixed_fees}))
    all_results.append(tavily_search.invoke({"query": query_use_case_regs}))

    return all_results

search_quality_of_life_tool = StructuredTool(
    name="search_quality_of_life",
    func=search_quality_of_life,
    args_schema=QualityOfLifeInput,
    description=(
        "Searches multiple sources (e.g., Google Maps, forums, local news) to "
        "assess the quality of life in a specific location.\n\n"
        "Focus areas:\n"
        "1. Amenities (schools, hospitals, transport)\n"
        "2. Vibe & density (restaurant/bar density, noise complaints)\n"
        "3. Tourist/commercial impact (hotels, rentals)\n\n"
        "Returns summarized search snippets for analysis."
    ),
)

search_socioeconomic_indexes_tool = StructuredTool(
    name="search_socioeconomic_indexes",
    func=search_socioeconomic_indexes,
    args_schema=SocioeconomicIndexesInput,
    description=(
        "Retrieves official and numerical socioeconomic indicators for a specific location. "
        "Use this tool when the user requests factual data such as:\n\n"
        "1. Crime index/rates (official statistics)\n"
        "2. Demographic data: population density, unemployment rate, household income\n"
        "3. Immigration and migration statistics\n"
        "4. Poverty or inequality metrics\n\n"
        "Input must be a precise area, not a vague region."
    ),
)

search_tourism_revenue_tool = StructuredTool(
    name="search_tourism_revenue",
    func=search_tourism_revenue,
    args_schema=TourismRevenueInput,
    description=(
        "Estimates tourism appeal and short-term rental revenue potential for a given area. "
        "Useful when evaluating:\n\n"
        "1. Average daily rental rates (ADR)\n"
        "2. Occupancy levels or seasonal patterns\n"
        "3. Listing density and market saturation\n\n"
        "Input must specify the exact location and optionally the property type."
    ),
)

search_local_taxes_regulations_tool = StructuredTool(
    name="search_local_taxes_regulations",
    func=search_local_taxes_regulations,
    args_schema=LocalTaxesRegulationsInput,
    description=(
        "Retrieves official local government taxes, fees, and regulations for a specific "
        "location and property use case.\n\n"
        "Use this tool when searching for:\n"
        "- Property ownership taxes (IBI)\n"
        "- Municipal fees (waste, sewage)\n"
        "- Short-term rental license requirements or tourist taxes\n"
        "- Rental income taxation or sale-tax implications\n\n"
        "Input must specify both the municipality and the property use case."
    ),
)

if __name__ == "__main__":
    #print(search_local_taxes_regulations.invoke({"location": "barrio de lavapies en madrid", "property_use_case":"living"}))

    print(search_socioeconomic_indexes.invoke({"location": "barrio de lavapies en madrid"}))