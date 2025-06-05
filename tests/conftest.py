from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.email import Base
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
async def db_session():
    # Тестовая БД в памяти
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncTestingSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncTestingSessionLocal() as session:
        yield session
