from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from shift_task.core.user import current_superuser, current_user
from shift_task.main import lifespan
from shift_task.schemas.user import UserSalaryCreate
from shift_task.core.config import settings

try:
    from shift_task.main import app
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружен объект приложения `app`.'
        'Проверьте и поправьте: он должен быть доступен в модуле `shift_task.main`.',
    )

try:
    from shift_task.core.db import Base, get_async_session
except (NameError, ImportError):
    raise AssertionError(
        'Не обнаружены объекты `Base, get_async_session`. '
        'Проверьте и поправьте: они должны быть доступны в модуле '
        '`shift_task.core.db`.',
    )


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

user = UserSalaryCreate(
    email="testuser@example.com",
    password="aaa",
    is_superuser=False,
    salary=20000
)
superuser = UserSalaryCreate(
    email="testsuperuser@example.com",
    password="bbb",
    is_superuser=True,
    salary=20000
)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def async_db_engine():
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield engine
    finally:
        print('SESSION IS CLOSED')
        # async with engine.begin() as conn:
        #     await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def async_db(async_db_engine):
    testing_session_local = async_sessionmaker(async_db_engine,
                                               expire_on_commit=False,
                                               class_=AsyncSession)
    async with testing_session_local() as session:
        await session.begin()

        yield session

        await session.rollback()


@pytest.fixture(scope='session')
async def client():
    async with lifespan(app):
        async with AsyncClient(app=app,
                               base_url="http://localhost") as client:
            yield client


@pytest.fixture(scope='function')
async def user_client(client):
    app.dependency_overrides[current_user] = lambda: user
    del app.dependency_overrides[current_superuser]
    return client


@pytest.fixture(scope='function')
async def superuser_client(client):
    app.dependency_overrides[current_superuser] = lambda: superuser
    return client
