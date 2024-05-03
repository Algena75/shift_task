from datetime import datetime
from typing import Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shift_task.core.config import MROT
from shift_task.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Наследуется от модели пользователя из библиотеки FastAPI Users. Расширена
    связью One-To-One с таблицей зарплат.
    """
    salary: Mapped['Salary'] = relationship(back_populates='user',
                                            lazy='selectin',
                                            cascade='delete')

    def to_dict(self):
        return dict(
            id=self.id,
            email=self.email,
            is_superuser=self.is_superuser,
            salary=dict(
                value=self.salary.value,
                shift_date=self.salary.shift_date
            ) if self.salary else None
        )


class Salary(Base):
    """Таблица зарплат."""
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='salary',
                                        lazy='selectin')
    shift_date: Mapped[Optional[datetime]]
    value: Mapped[int] = mapped_column(Integer, default=MROT)

    __table_args__ = (UniqueConstraint("user_id"),)

    def __repr__(self) -> str:
        return f'Зарплата: {self.value} руб.'
