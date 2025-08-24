from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID
from datetime import datetime


class StatusTask(str, Enum):
    CREATED = 'created'
    IN_PROGREsS = 'in_progress'
    COMPLETED = 'completed'


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    status: StatusTask = StatusTask.CREATED


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    status: StatusTask | None = None


class Task(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True