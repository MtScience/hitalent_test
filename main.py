from fastapi import FastAPI
from src.api.router import router as departments_router

app = FastAPI()
app.include_router(departments_router, prefix="/departments", tags=["Departments"])
