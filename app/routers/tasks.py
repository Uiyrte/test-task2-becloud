from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    path="/",
    response_model=TaskRead,
    status_code=201,
    summary="Создать задачу",
    description="Создаёт новую задачу со статусом по умолчанию `todo`.",
)
def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> Task:
    return crud.create_task(db, task)


@router.get(
    path="/{task_id}",
    response_model=TaskRead,
    summary="Получить задачу по ID",
    description="Возвращает задачу по её идентификатору или 404, "
    "если задача не найдена.",
)
def read_task(task_id: int, db: Session = Depends(get_db)) -> Task:
    db_task = crud.read_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.get(
    path="/",
    response_model=list[TaskRead],
    summary="Получить список задач",
    description="Возвращает список всех задач.",
)
def read_all_tasks(db: Session = Depends(get_db)) -> list[Task]:
    return crud.read_all_tasks(db)


@router.patch(
    path="/{task_id}",
    response_model=TaskRead,
    summary="Обновить задачу",
    description="Частично обновляет задачу: можно передать только "
    "изменяемые поля (title, description, status).",
)
def update_task(
    task_id: int, task: TaskUpdate, db: Session = Depends(get_db)
) -> Task:
    db_task = crud.update_task(db, task_id, task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete(
    path="/{task_id}",
    status_code=204,
    summary="Удалить задачу",
    description="Удаляет задачу по её идентификатору или возвращает 404, "
    "если задача не найдена.",
)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    db_task = crud.delete_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
