from app.core.database import AsyncSessionLocal


# Dependency injection for database session
async def get_db():

    async with AsyncSessionLocal() as session:

        yield session