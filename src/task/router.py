from fastapi import APIRouter, status, Depends
from typing import List

from .di import get_task_repository
from .repository import TaskRepository
from .schemas import Task, TaskCreate, StatusTask, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    task_repository: TaskRepository = Depends(get_task_repository)
) -> Task:
    return await task_repository.create_task(task)


@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    task_repository: TaskRepository = Depends(get_task_repository)
):
    try:
        task_id = task_id
        return await task_repository.get_task(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID"
        )


@router.get("/", response_model=list[Task])
async def get_tasks(
    status: StatusTask | None = None,
    limit: int = 100,
    offset: int = 0,
    task_repository: TaskRepository = Depends(get_task_repository)
):
    return await task_repository.get_tasks(status, limit, offset)


@router.patch("/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    task_repository: TaskRepository = Depends(get_task_repository)
):
    try:
        task_id = task_id
        return await task_repository.update_task(task_id, task_update)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID"
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    task_repository: TaskRepository = Depends(get_task_repository)
):
    try:
        task_id = task_id
        await task_repository.delete_task(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID"
        )


@router.get("/status/{status}", response_model=list[Task])
async def get_tasks_by_status(
    status: StatusTask,
    task_repository: TaskRepository = Depends(get_task_repository)
):
    return await task_repository.get_tasks_by_status(status)