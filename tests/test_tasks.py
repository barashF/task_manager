import pytest
from httpx import AsyncClient
from uuid import UUID, uuid4

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    response = await client.post(
        "/tasks",
        json={"title": "Test Task", "description": "Test Description"}
    )
    
    assert response.status_code == 201
    
    task = response.json()
    assert "id" in task
    assert UUID(task["id"])

@pytest.mark.asyncio
async def test_get_task(client: AsyncClient, test_task_id: str):
    response = await client.get(f"/tasks/{test_task_id}")
    
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == "Test Task"

@pytest.mark.asyncio
async def test_update_task(client: AsyncClient, test_task_id: str):
    response = await client.patch(
        f"/tasks/{test_task_id}",
        json={"title": "Updated Task", "status": "in_progress"}
    )
    
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == "Updated Task"
    assert task["status"] == "in_progress"

@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient, test_task_id: str):
    response = await client.delete(f"/tasks/{test_task_id}")
    
    assert response.status_code == 204