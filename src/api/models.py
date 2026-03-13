from __future__ import annotations

import datetime as dt
from pydantic import BaseModel, Field


class CreateDepartment(BaseModel):
    name: str
    parent_id: int | None = Field(default=None)


class UpdateDepartment(BaseModel):
    name: str | None = Field(default=None)
    parent_id: int | None = Field(default=None)


class CreateEmployee(BaseModel):
    full_name: str
    position: str
    hired_at: dt.date | None = Field(default=None)


class DepartmentResponse(BaseModel):
    id: int
    name: str
    parent_id: int | None = Field(default=None)
    created_at: dt.datetime


class EmployeeResponse(BaseModel):
    id: int
    department_id: int
    full_name: str
    position: str
    hired_at: dt.date | None = Field(default=None)
    created_at: dt.datetime


class DepartmentRetrievalResponse(BaseModel):
    department: DepartmentResponse
    children: list[DepartmentResponse] = Field(default_factory=list)
    employees: list[EmployeeResponse] | None = Field(default=None)
