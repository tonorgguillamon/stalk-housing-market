from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(
    DATABASE_URL,
    future=True
)

AsyncSessionLocal = sessionmaker(
    engine, 
    expire_on_commit=False,
    class_=AsyncSession
)

@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


# to use it:
# async with get_session() as session:
#    results = await search_accommodations(session, filters)
