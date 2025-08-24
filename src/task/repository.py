from asyncpg import Connection
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import HTTPException

from .schemas import TaskCreate, Task, StatusTask, TaskUpdate


class TaskRepository:
    def __init__(self, db_context: Connection):
        self.db_context = db_context
    
    async def create_task(self, task: TaskCreate) -> Task:
        query = """
            INSERT INTO tasks (title, description, status)
            VALUES ($1, $2, $3)
            RETURNING id, title, description, status, created_at, updated_at
        """
        row = await self.db_context.fetchrow(
            query,
            task.title,
            task.description,
            task.status
        )
        return Task(**dict(row))
    
    async def get_task(self, task_id: UUID) -> Task:
        query = """
            SELECT id, title, description, status, created_at, updated_at
            FROM tasks
            WHERE id = $1
        """
        row = await self.db_context.fetchrow(query, task_id)
        
        if not row:
            raise HTTPException(
                status_code=404, 
                detail=f"Task with ID {task_id} not found"
            )
            
        return Task(**dict(row))
    
    async def get_tasks(self, status: Optional[StatusTask] = None, limit: int = 100, offset: int = 0) -> List[Task]:
        where_clauses = []
        params = []
        
        if status:
            where_clauses.append("status = $1")
            params.append(status.value)
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT id, title, description, status, created_at, updated_at
            FROM tasks
            WHERE {where_clause}
            ORDER BY created_at DESC
            LIMIT ${len(params) + 1}
            OFFSET ${len(params) + 2}
        """
        
        params.extend([limit, offset])
        rows = await self.db_context.fetch(query, *params)
        return [Task(**dict(row)) for row in rows]
    
    async def update_task(self, task_id: UUID, task_update: TaskUpdate) -> Task:
        await self.get_task(task_id)
        
        update_data = task_update.model_dump(exclude_unset=True)
        
        if not update_data:
            return await self.get_task(task_id)
        
        set_clause = ", ".join([f"{field} = ${i+1}" for i, field in enumerate(update_data.keys())])
        query = f"""
            UPDATE tasks
            SET {set_clause}
            WHERE id = ${len(update_data) + 1}
            RETURNING id, title, description, status, created_at, updated_at
        """
        
        params = list(update_data.values()) + [task_id]
        
        row = await self.db_context.fetchrow(query, *params)
        return Task(**dict(row))
    
    async def delete_task(self, task_id: UUID) -> None:
        await self.get_task(task_id)
        
        query = "DELETE FROM tasks WHERE id = $1"
        await self.db.execute(query, task_id)
    
    async def get_tasks_by_status(self, status: StatusTask) -> List[Task]:
        return await self.get_tasks(status=status)
    