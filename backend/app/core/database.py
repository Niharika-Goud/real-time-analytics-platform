from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


# Create async SQLAlchemy engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)


# Async database session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


# Base model class for all database tables
class Base(DeclarativeBase):
    pass


# Dependency injection for database session
async def get_db():

    async with AsyncSessionLocal() as session:

        yield session