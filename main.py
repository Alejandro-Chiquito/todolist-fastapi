from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="todo-list.api",
    description="This is a simple todo list API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(todo_router, prefix="/todos", tags=["todos"])