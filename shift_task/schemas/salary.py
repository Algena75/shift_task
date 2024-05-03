from datetime import datetime

from pydantic import BaseModel, Field


class SalaryDB(BaseModel):
    """Pydantic-схема для отображения данных о зарплате."""
    salary: int = Field(alias='value')
    shift_date: datetime

    class Config:
        from_attributes = True
