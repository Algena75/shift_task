import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from shift_task.core.config import settings
from shift_task.core.db import get_async_session
from shift_task.core.models import User
from shift_task.core.user import get_user_db, get_user_manager
from shift_task.schemas.user import UserCreate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
        email: EmailStr, password: str, is_superuser: bool = False
) -> User:
    """Создаёт и возвращет экземпляр пользователя."""
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user_created = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser
                        )
                    )
                    return user_created
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    """Создаёт первого суперпользователя при запуске проекта."""
    if (settings.first_superuser_email is not None and
            settings.first_superuser_password is not None):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True,
        )
