import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shift_task.core.models import User


@pytest.mark.anyio
async def test_superuser_can_view_users(superuser_client: AsyncClient):
    response = await superuser_client.get("/users")
    # await print(response.json())
    assert response.status_code == 200
    assert 'admin@admin.ru' in response.text


@pytest.mark.anyio
async def test_user_cant_view_users(user_client: AsyncClient):
    response = await user_client.get("/users")
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.parametrize("new_user_data", ({"email": "testuser@example.com",
                                            "password": "testuserpassword",
                                            "salary": 50000},))
@pytest.mark.anyio
async def test_superuser_can_add_users(superuser_client: AsyncClient,
                                       new_user_data):
    response = await superuser_client.post("/users", json=new_user_data)
    assert response.status_code == 201
    assert new_user_data.get('email') in response.text


@pytest.mark.parametrize("new_user_data", ({"username": "testuser@example.com",
                                            "password": "testuserpassword"},))
@pytest.mark.anyio
async def test_new_user_can_get_token(user_client: AsyncClient,
                                      async_db: AsyncSession, new_user_data):
    new_user_token = await user_client.post("/auth/jwt/login",
                                            data=new_user_data)
    assert new_user_token.status_code == 200
    assert "access_token" in new_user_token.json()

    user_to_delete = await async_db.execute(
        select(User).where(User.email == new_user_data.get('username'))
    )
    user_to_delete = user_to_delete.scalars().first()
    await async_db.delete(user_to_delete)
    await async_db.commit()
