from __future__ import annotations

import datetime as dt
from dataclasses import dataclass


@dataclass
class DepartmentDTO:
    id: int
    name: str
    created_at: dt.datetime
    parent_id: int | None = None


@dataclass
class EmployeeDTO:
    id: int
    department_id: int
    full_name: str
    position: str
    created_at: dt.datetime
    hired_at: dt.date | None = None


@dataclass
class SubdepartmentsDTO:
    department: DepartmentDTO
    subdepartments: list[DepartmentDTO | SubdepartmentsDTO]
