from fastapi import FastAPI
from src.api.router import router as departments_router

description = """
Тестовое задание для Hitalent. API позволяет:

- создавать отделы;
- изменять отделы;
- удалять отделы (с возможностью каскадного удаления вложенных отделов и работников либо с переназначением их в другой
  отдел);
- получать информацию об отделе со списком его под-отделов и сотрудников;
- создавать сотрудников.

При этом отслеживается отсутствие циклов в дереве отделов.
"""
app = FastAPI(
    title="Hitalent test task",
    description=description,
    version="0.0.1",
)
app.include_router(departments_router, prefix="/departments", tags=["Departments"])
