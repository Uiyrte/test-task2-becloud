from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class StatusState(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    status: StatusState = StatusState.todo
    created_at: datetime


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: StatusState | None = None
