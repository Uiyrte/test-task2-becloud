from typing import Optional

from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    return db_task


def read_task(db: Session, task_id: int) -> Optional[Task]:
    db_task = db.get(Task, task_id)
    return db_task


def update_task(db: Session, task_id: int, task: TaskUpdate) -> Optional[Task]:
    db_task = db.get(Task, task_id)
    if db_task is None:
        return None
    for field, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> Optional[Task]:
    db_task = db.get(Task, task_id)
    if db_task is None:
        return None
    db.delete(db_task)
    db.commit()
    return db_task
