from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shift_task.core.models import Salary


async def get_shift_salary_date(session: AsyncSession,
                                user_id: int | None = None) -> datetime:
    """
    Функция устанавливает дату повышения зарплаты, если она не была
    установлена при создании пользователя. Также проверяет дату для ранее
    созданной записи: если дата прошла, то устанавливает новую дату.
    """
    shift_date = None
    if user_id:
        salary = session.execute(
            select(Salary).where(Salary.user_id == user_id)
        )
        salary = salary.scalars().first()
        shift_date = salary.shift_date
    if shift_date is None or shift_date < datetime.now():
        shift_date = datetime(day=31, month=12, year=datetime.now().year)
    return shift_date
