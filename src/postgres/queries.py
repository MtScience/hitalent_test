import datetime as dt
from typing import Literal

from sqlalchemy import select, update, exists, delete, insert, literal_column, CTE
from sqlalchemy.ext.asyncio import AsyncSession

from src.errors import NonexistentDepartmentError, NothingToUpdate
from src.dto.dto import DepartmentDTO, EmployeeDTO, SubdepartmentsDTO
from src.postgres.models import Department, Employee


def _create_department_subtree_ids_cte(id: int) -> CTE:
    dept_cte = (
        select(
            Department.id,
            Department.parent_id,
        )
        .where(Department.id == id)
        .cte(name="dept_cte", recursive=True)
    )
    dept_cte_alias = dept_cte.alias("dept_cte_alias")
    dept_cte = dept_cte.union_all(
        select(
            Department.id,
            Department.parent_id
        )
        .join(dept_cte_alias, Department.parent_id == dept_cte_alias.c.id)
    )

    return dept_cte

async def create_department(
    session: AsyncSession,
    name: str,
    parent_id : int | None = None,
) -> DepartmentDTO:
    query = (
        insert(Department)
        .values(name=name, parent_id=parent_id)
        .returning(Department)
    )

    new_department = await session.scalar(query)
    return new_department.to_dto()


async def update_department(
    session: AsyncSession,
    id: int,
    name: str | None = None,
    parent_id : int | None = None,
) -> DepartmentDTO:
    query = None
    match (name, parent_id):
        case (None, None):
            raise NothingToUpdate
        case (str(), None):
            query = (
                update(Department)
                .values(name=name)
                .where(Department.id == id)
                .returning(Department)
            )
        case (_, int()):
            subdept_cte = _create_department_subtree_ids_cte(id)
            subdept_ids_query = select(subdept_cte.c.id)
            subdept_ids = (await session.scalars(subdept_ids_query)).all()
            if parent_id in subdept_ids:
                raise ValueError("Cannot make a department its own subdepartment.")

            values = {"parent_id": parent_id}
            if name:
                values["name"] = name
            query = (
                update(Department)
                .values(**values)
                .where(Department.id == id)
                .returning(Department)
            )

    result = await session.scalar(query)
    return result.to_dto()


async def create_employee(
    session: AsyncSession,
    full_name: str,
    position: str,
    dept_id: int,
    hired_at: dt.date | None,
) -> EmployeeDTO:
    dept_exists = await session.scalar(
        exists()
        .where(Department.id == dept_id)
        .select()
    )
    if not dept_exists:
        raise NonexistentDepartmentError

    query = (
        insert(Employee)
        .values(
            full_name=full_name,
            position=position,
            hired_at=hired_at,
            department_id=dept_id,
        )
        .returning(Employee)
    )
    new_employee = await session.scalar(query)
    return new_employee.to_dto()


async def get_employees(
    session: AsyncSession,
    dept_id: int,
) -> list[EmployeeDTO]:
    query = (
        select(Employee)
        .where(Employee.department_id == dept_id)
        .order_by(Employee.full_name.asc())
    )
    result = (await session.scalars(query)).all()

    return [emp.to_dto() for emp in result]


async def get_department(
    session: AsyncSession,
    id: int,
) -> DepartmentDTO | None:
    query = select(Department).where(Department.id == id)
    dept = await session.scalar(query)

    return dept.to_dto() if dept else None


async def delete_department(
    session: AsyncSession,
    id: int,
    mode: Literal["cascade", "reassign"],
    reassign_to: int | None = None,
) -> None:
    if mode == "reassign":
        queries = [
            update(Employee).values(department_id=reassign_to).where(Employee.department_id == id),
            update(Department).values(parent_id=reassign_to).where(Department.parent_id == id),
            delete(Department).where(Department.id == id),
        ]
        for query in queries:
            await session.execute(query)
    elif mode == "cascade":
        dept_cte = _create_department_subtree_ids_cte(id)
        dept_ids_subquery = select(dept_cte.c.id)
        queries = [
            delete(Employee).where(Employee.department_id.in_(dept_ids_subquery)),
            delete(Department).where(Department.id.in_(dept_ids_subquery)),
        ]
        for query in queries:
            await session.execute(query)
    else:
        raise ValueError("Invalid mode")


async def get_subdepartments(
    session: AsyncSession,
    dept_id: int,
    depth: int,
) -> list[DepartmentDTO | SubdepartmentsDTO]:
    depts_cte = (
        select(
            Department.id,
            Department.parent_id,
            literal_column("1").label("depth")
        )
        .where(Department.parent_id == dept_id)
        .cte(name="depts_cte", recursive=True)
    )
    depts_cte_alias = depts_cte.alias("depts_cte_alias")
    depts_cte = depts_cte.union_all(
        select(
            Department.id,
            Department.parent_id,
            (depts_cte_alias.c.depth + 1).label("depth")
        )
        .join(depts_cte_alias, Department.parent_id == depts_cte_alias.c.id)
    )

    query = (
        select(Department)
        .where(
            Department.id.in_(
                select(depts_cte.c.id)
                .where(depts_cte.c.depth <= depth)
            )
        )
    )

    subdepartments = (await session.scalars(query)).all()

    return [subdept.to_dto() for subdept in subdepartments]
