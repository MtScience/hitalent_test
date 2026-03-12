from datetime import date
from pydantic import BaseModel, Field


class CreateDepartment(BaseModel):
    name: str
    parent_id: int | None = Field(default=None)


class CreateEmployee(BaseModel):
    full_name: str
    position: str
    hired_at: date | None = Field(default=None)
