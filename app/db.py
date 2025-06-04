from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.database_url, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


# Зависимость для использования в эндпоинтах
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
