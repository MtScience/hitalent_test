from fastapi import APIRouter, Query
from typing import Annotated, Literal

from src.api.models import CreateDepartment, CreateEmployee

router = APIRouter()


@router.post("")
def create_department(payload: CreateDepartment):
    pass


@router.post("/{id}/employees")
def create_employee(id: str, payload: CreateEmployee):
    pass


@router.get("/{id}")
def get_department(
    id: int,
    depth: Annotated[int, Query(ge=1, le=5)] = 1,
    include_employees: bool = True
):
    pass


@router.patch("/{id}")
def update_department(id: int):
    pass


@router.delete("/{id}")
def delete_department(
    id: int,
    mode: Literal["cascade", "reassign"],
    reassign_to_department_id: int | None = None,
):
    pass
