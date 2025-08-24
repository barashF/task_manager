from config.database import get_db_connection
from .repository import TaskRepository

from fastapi import Depends


def get_task_repository(db = Depends(get_db_connection)):
    return TaskRepository(db)