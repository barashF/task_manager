import pytest
from httpx import AsyncClient
from src.application.app import create_app


app = create_app()


@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def test_task_id(client: AsyncClient):
    response = await client.post(
        "/tasks",
        json={"title": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == 201
    return response.json()["id"]