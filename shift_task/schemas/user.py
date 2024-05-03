from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, Field

from shift_task.core.config import MROT
from shift_task.schemas.salary import SalaryDB


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserSalaryCreate(BaseModel):
    """Преобразует JSON в объект Python."""
    email: EmailStr
    password: str
    is_superuser: bool = Field(default=False)
    salary: int = Field(..., gt=MROT)
    shift_date: Optional[datetime] = None
    id: Optional[int] = None


class UserSalaryRead(BaseModel):
    """Схема для отображения данных о пользователе."""
    id: int
    is_superuser: bool
    email: str
    salary: Optional[SalaryDB] = None
