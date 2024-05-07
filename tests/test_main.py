import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shift_task.core.config import settings
from shift_task.core.models import User

TEST_USER = dict(email="anyuser@example.com",
                 password="anyuserpassword",
                 salary=50000)


@pytest.mark.anyio
async def test_unauthorized_user_cant_view_users(client: AsyncClient):
    """
    Неавторизованный пользователь не имеет доступа к списку пользователей.
    """
    response = await client.get("/users")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Unauthorized"}
    response = await client.get("/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.anyio
async def test_superuser_can_view_users(superuser_client: AsyncClient):
    """
    Суперюзер имеет доступ к списку всех пользователей.
    """
    response = await superuser_client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert settings.first_superuser_email in response.text


@pytest.mark.parametrize("new_user_data", (TEST_USER,))
@pytest.mark.anyio
async def test_superuser_can_add_users(superuser_client: AsyncClient,
                                       new_user_data):
    """
    Суперюзер может добавить пользователя.
    """
    response = await superuser_client.post("/users", json=new_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert new_user_data.get('email') in response.text


@pytest.mark.parametrize("new_user_data",
                         ({"username": TEST_USER.get("email"),
                          "password": TEST_USER.get("password")},))
@pytest.mark.anyio
async def test_new_user_can_get_token(client: AsyncClient, new_user_data):
    """
    Пользователь при аутентификации получает действительный токен.
    """
    new_user_token = await client.post("/auth/jwt/login", data=new_user_data)
    assert new_user_token.status_code == status.HTTP_200_OK
    assert "access_token" in new_user_token.json()
    TEST_USER['access_token'] = (
        f'Bearer {new_user_token.json().get("access_token")}'
    )


@pytest.mark.anyio
async def test_new_user_can_get_salary_info(client: AsyncClient,
                                            async_db: AsyncSession):
    """
    Пользователь по токену получает информацию по своей зарплате.
    """
    response = await client.get(
        '/users/me', headers={'Authorization': TEST_USER["access_token"]}
    )
    assert response.status_code == status.HTTP_200_OK
    assert 'shift_date', 'value' in response.json()
    assert response.json()['value'] == TEST_USER.get("salary")
    new_user = await async_db.execute(
        select(User).where(User.email == TEST_USER.get('email'))
    )
    new_user = new_user.scalars().first()
    await async_db.delete(new_user)
    await async_db.commit()
