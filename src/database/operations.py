from sqlalchemy import select, case, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Accommodation, SearchFilters

# Usage example:
# filters = SearchFilters(**agent_parameters)
# results = await search_accommodations(async_session, filters)

async def get_accommodations(
    session: AsyncSession,
    filters: SearchFilters,
):
    stmt = select(Accommodation)

    f = filters

    # location
    if f.country:
        stmt = stmt.where(Accommodation.country == f.country)
    if f.province:
        stmt = stmt.where(Accommodation.province == f.province)
    if f.munipality:
        stmt = stmt.where(Accommodation.munipality == f.munipality)
    if f.district:
        stmt = stmt.where(Accommodation.district == f.district)
    if f.neighborhood:
        stmt = stmt.where(Accommodation.neighborhood == f.neighborhood)

    # attributes
    if f.propertyType:
        stmt = stmt.where(Accommodation.propertyType == f.propertyType)
    if f.terrace is not None:
        stmt = stmt.where(Accommodation.terrace == f.terrace)
    if f.garage is not None:
        stmt = stmt.where(Accommodation.garage == f.garage)
    if f.hasLift is not None:
        stmt = stmt.where(Accommodation.hasLift == f.hasLift)
    if f.newDevelopment is not None:
        stmt = stmt.where(Accommodation.newDevelopment == f.newDevelopment)

    # numeric
    if f.min_price is not None:
        stmt = stmt.where(Accommodation.price >= f.min_price)
    if f.max_price is not None:
        stmt = stmt.where(Accommodation.price <= f.max_price)
    if f.min_rooms is not None:
        stmt = stmt.where(Accommodation.rooms >= f.min_rooms)
    if f.max_rooms is not None:
        stmt = stmt.where(Accommodation.rooms <= f.max_rooms)

    # time
    if f.published_after:
        stmt = stmt.where(Accommodation.datePublication >= f.published_after)

    stmt = stmt.order_by(Accommodation.datePublication.desc())
    stmt = stmt.limit(f.limit)

    result = await session.scalars(stmt)
    return result.all()


async def get_accommodation_stats(
    session: AsyncSession,
    filters: SearchFilters,
    metric: str,
):
    METRICS = {
        "count": func.count(Accommodation.id),
        "avg_price": func.avg(Accommodation.price),
        "median_price": func.percentile_cont(0.5).within_group(Accommodation.price),
        "avg_price_per_m2": func.avg(Accommodation.pricePerM2),
        "min_price": func.min(Accommodation.price),
        "max_price": func.max(Accommodation.price),
    }

    if metric not in METRICS:
        raise ValueError("Unsupported metric")

    stmt = select(METRICS[metric].label(metric))

    f = filters

    # Expanded filters exactly as in search_accommodations:
    if f.country:
        stmt = stmt.where(Accommodation.country == f.country)
    if f.province:
        stmt = stmt.where(Accommodation.province == f.province)
    if f.munipality:
        stmt = stmt.where(Accommodation.munipality == f.munipality)
    if f.district:
        stmt = stmt.where(Accommodation.district == f.district)
    if f.neighborhood:
        stmt = stmt.where(Accommodation.neighborhood == f.neighborhood)

    if f.propertyType:
        stmt = stmt.where(Accommodation.propertyType == f.propertyType)
    if f.terrace is not None:
        stmt = stmt.where(Accommodation.terrace == f.terrace)
    if f.garage is not None:
        stmt = stmt.where(Accommodation.garage == f.garage)
    if f.hasLift is not None:
        stmt = stmt.where(Accommodation.hasLift == f.hasLift)
    if f.newDevelopment is not None:
        stmt = stmt.where(Accommodation.newDevelopment == f.newDevelopment)

    if f.min_price is not None:
        stmt = stmt.where(Accommodation.price >= f.min_price)
    if f.max_price is not None:
        stmt = stmt.where(Accommodation.price <= f.max_price)
    if f.min_rooms is not None:
        stmt = stmt.where(Accommodation.rooms >= f.min_rooms)
    if f.max_rooms is not None:
        stmt = stmt.where(Accommodation.rooms <= f.max_rooms)

    if f.published_after:
        stmt = stmt.where(Accommodation.datePublication >= f.published_after)

    result = await session.execute(stmt)
    row = result.one()

    return {metric: row[0]}


async def get_price_distribution(
    session: AsyncSession,
    buckets: list[tuple[float, float]],
    filters: SearchFilters,
    group_by_neighborhood: bool = False,
):
    cases = []

    for low, high in buckets:
        cases.append(
            func.count(
                case(
                    (Accommodation.price.between(low, high), 1)
                )
            ).label(f"{low}_{high}")
        )

    if group_by_neighborhood:
        stmt = select(Accommodation.neighborhood, *cases).group_by(Accommodation.neighborhood)
    else:
        stmt = select(*cases)

    if filters.propertyType:
        stmt = stmt.where(Accommodation.propertyType == filters.propertyType)

    # Apply neighborhood filter only if NOT grouping by neighborhood
    if not group_by_neighborhood and filters.neighborhood:
        stmt = stmt.where(Accommodation.neighborhood == filters.neighborhood)

    result = await session.execute(stmt)
    rows = result.all()

    if group_by_neighborhood:
        return {
            row.neighborhood: {k: value for k, value in row._mapping.items() if k != "neighborhood"}
            for row in rows
        }
    else:
        return dict(rows[0]._mapping) if rows else {}