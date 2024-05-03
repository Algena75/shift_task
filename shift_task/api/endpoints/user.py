from typing import Dict, List, Union

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shift_task.api.utils import get_shift_salary_date
from shift_task.api.validators import (check_salary_value,
                                       check_shift_salary_date,
                                       check_user_exists)
from shift_task.core.db import get_async_session
from shift_task.core.init_db import create_user
from shift_task.core.models import Salary, User
from shift_task.core.user import (auth_backend, current_superuser,
                                  current_user, fastapi_users)
from shift_task.schemas.salary import SalaryDB
from shift_task.schemas.user import UserSalaryCreate, UserSalaryRead

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)


@router.post(
    '/users',
    tags=['users'],
    dependencies=[Depends(current_superuser)],
    response_model=UserSalaryRead,
    status_code=201
)
async def create_new_user(
    new_user: UserSalaryCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Dict:
    """Добавление пользователей доступно только суперпользователям."""
    new_user = new_user.model_dump()
    await check_user_exists(new_user, session)
    check_salary_value(new_user.get('salary'))
    salary_dict = dict(value=new_user.pop('salary'))
    shift_date = new_user.pop('shift_date')
    if shift_date is not None:
        check_shift_salary_date(shift_date)
    else:
        shift_date = await get_shift_salary_date(session=session)
    user_in = await create_user(
        email=new_user.get('email'),
        password=new_user.get('password'),
        is_superuser=new_user.get('is_superuser'),
    )
    salary_dict.update(user_id=user_in.id, shift_date=shift_date.date())
    salary_in = Salary(**salary_dict)
    session.add(salary_in)
    await session.commit()
    session.refresh(user_in)
    return user_in


@router.get(
    '/users/me',
    tags=['users'],
    response_model=Union[SalaryDB, Dict]
)
async def get_salary_info(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
) -> Union[Salary, Dict]:
    """
    Функция показа зарплаты авторизованному пользователю. Зарплата первого
    суперпользователя в данной реализации не устанавливается.
    """
    salary = await session.execute(
        select(Salary).where(Salary.user_id == user.id)
    )
    salary = salary.scalars().first()
    if user.id == 1 and salary is None:
        return {'message': 'Зарплата для первого суперюзера еще не назначена'}
    return salary


@router.get(
    '/users',
    tags=['users'],
    dependencies=[Depends(current_superuser)],
    response_model=List[UserSalaryRead]
)
async def get_all_users(
    session: AsyncSession = Depends(get_async_session),
) -> List[Dict]:
    """
    Функция возвращает список всех пользователей. Доступна только
    суперпользователям.
    """
    all_users = await session.execute(select(User))
    return [item.to_dict() for item in all_users.scalars().all()]
