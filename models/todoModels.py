from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator
from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase


# --- ORM Base ---

class Base(DeclarativeBase):
    pass


# --- Enums ---

class TodoStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# --- ORM Entity ---

class Todo(Base):
    """Maps the 'todos' table."""

    __tablename__ = "todos"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(100), nullable=False)
    description: str | None = Column(String(500), nullable=True)
    status: str = Column(String(20), nullable=False, default=TodoStatus.PENDING)
    created_at: datetime = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: datetime = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


# --- Pydantic Schemas ---

class TodoCreateRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: TodoStatus = TodoStatus.PENDING

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("title must not be blank")
        return value.strip()


class TodoUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: TodoStatus | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("title must not be blank")
        return value.strip() if value else value


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TodoStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}