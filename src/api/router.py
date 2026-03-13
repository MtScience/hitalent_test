from dataclasses import asdict
from fastapi import APIRouter, Query, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.errors import NonexistentDepartmentError, NothingToUpdate, DepartmentLoop
from src.postgres.base import get_async_session
from src.api.models import (
    CreateDepartment,
    UpdateDepartment,
    CreateEmployee,
    DepartmentResponse,
    EmployeeResponse,
    DepartmentRetrievalResponse,
)
from src.api.validation import DeletionQueryParams
import src.postgres.queries as queries

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_department(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    payload: CreateDepartment,
):
    data = await queries.create_department(session, **payload.model_dump())
    return DepartmentResponse(**asdict(data))


@router.post(
    "/{id}/employees",
    status_code=status.HTTP_201_CREATED,
)
async def create_employee(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: int,
    payload: CreateEmployee
):
    try:
        data = await queries.create_employee(session, dept_id=id, **payload.model_dump())
        return EmployeeResponse(**asdict(data))
    except NonexistentDepartmentError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/{id}")
async def get_department(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: int,
    depth: Annotated[int, Query(ge=1, le=5)] = 1,
    include_employees: bool = True
):
    dept = await queries.get_department(session, id)
    if dept is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    dept_response = DepartmentResponse(**asdict(dept))

    employees_response = None
    if include_employees:
        employees = (await queries.get_employees(session, id))
        employees_response = [EmployeeResponse(**asdict(employee)) for employee in employees]

    children = await queries.get_subdepartments(session, id, depth)
    children_response = [DepartmentResponse(**asdict(dept)) for dept in children]

    return DepartmentRetrievalResponse(
        department=dept_response,
        employees=employees_response,
        children=children_response,
    )


@router.patch("/{id}")
async def update_department(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: int,
    payload: UpdateDepartment,
):
    try:
        data = await queries.update_department(session, id=id, **payload.model_dump())
        return DepartmentResponse(**asdict(data))
    except NothingToUpdate:
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
    except DepartmentLoop:
        return Response(status_code=status.HTTP_409_CONFLICT)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_department(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    id: int,
    params: Annotated[DeletionQueryParams, Query()]
):
    try:
        await queries.delete_department(session, id, params.mode, params.reassign_id)
    except DepartmentLoop:
        return Response(status_code=status.HTTP_409_CONFLICT)
    except ValueError:
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
