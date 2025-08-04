import pytest
from httpx import AsyncClient
from src.app.main import app
from src.app.core.database import AsyncSessionLocal, get_db
from src.app.core.config import get_settings

# os.environ["MODE"] = "TEST"
settings = get_settings()


# @pytest.fixture(scope="session", autouse=True)
# async def prepare_database():
#     """Создаёт таблицы в тестовой БД перед запуском тестов."""
#     engine = create_async_engine(settings.DATABASE_URL, future=True, echo=False)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     yield
#     await engine.dispose()


@pytest.fixture
async def db_session():
    """Фикстура для работы с основной БД с откатом изменений после теста."""
    async with AsyncSessionLocal() as session:
        async with session.begin():
            yield session
            await session.rollback()


@pytest.fixture
async def async_client(db_session):
    """HTTP-клиент FastAPI для тестов, использующий фиктивную сессию."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
