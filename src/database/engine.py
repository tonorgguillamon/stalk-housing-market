from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # checks broken connections before using them
    pool_size=10,         # persistent connections kept open
    max_overflow=20,      # extra burst connections
    pool_timeout=30,      # seconds to wait for a free connection
    pool_recycle=1800,    # recycle connections every 30 min
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)
@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

async def close_engine() -> None:
    await engine.dispose()


# to use it:
# async with get_session() as session:
#    results = await search_accommodations(session, filters)
