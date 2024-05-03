from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shift_task.core.config import MROT
from shift_task.core.models import User


def check_shift_salary_date(
        shift_date: datetime,
) -> None:
    """Дата повышения зарплаты должна быть в будущем."""
    if shift_date.date() <= datetime.now().date():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Дата повышения зарплаты не может быть в прошлом!',
        )


async def check_user_exists(
        new_user: User,
        session: AsyncSession,
) -> None:
    """Проверка повторного добавления пользователя с электронной почтой."""
    exist_user = await session.execute(
        select(User).where(User.email == new_user['email'])
    )
    exist_user = exist_user.scalars().first()
    if exist_user is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                f'Пользователь с почтой {new_user["email"]} уже существует!'
            )
        )


def check_salary_value(
        salary_value: int,
) -> None:
    """Проверяет зарплату на соответствие МРОТ."""
    if salary_value <= MROT:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Зарплата не может быть меньше МРОТ!'
        )
