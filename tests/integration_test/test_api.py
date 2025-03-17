import pytest
from httpx import AsyncClient
from app.models import TodoItems
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession


# Тест на создание задачи
@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    response = await client.post(
        "/api/todo/",
        json={
            "title": "Task1",
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Task1"
    assert data["isCompleted"] == False


# Тест на обработку некорректных данных
@pytest.mark.asyncio
async def test_create_task_invalid(client: AsyncClient):
    response = await client.post(
        "/api/todo/",
        json={
            "title": 12,
            "isCompleted": False,
            "createAt": "2025-03-03T16:16:56.166605",
        },
    )
    assert response.status_code == 422


# Тест на поиск задачи по id
@pytest.mark.asyncio
async def test_read_task_id(session: AsyncSession, client: AsyncClient):
    # Сначала нужно добавить данные в бд
    task = TodoItems(title="task2", isCompleted=False, created_at=datetime.now())
    session.add(task)
    await session.commit()

    response = await client.get(f"/api/todo/{task.id}")

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == task.id
    assert data["title"] == task.title
    assert data["isCompleted"] == task.isCompleted
    assert data["created_at"] == task.created_at.isoformat()


# Тест на поиск не существующей задачи
@pytest.mark.asyncio
async def test_read_task_not_found(client: AsyncClient):
    response = await client.get("/api/todo/100")
    assert response.status_code == 404


# Тест на вывод всех задач
@pytest.mark.asyncio
async def test_read_tasks(session: AsyncSession, client: AsyncClient):
    task1 = TodoItems(id=1, title="task1", isCompleted=False, created_at=datetime.now())
    session.add(task1)

    task2 = TodoItems(id=2, title="task2", isCompleted=True, created_at=datetime.now())
    session.add(task2)

    await session.commit()

    response = await client.get("/api/todo/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2

    assert data[0]["title"] == task1.title
    assert data[0]["isCompleted"] == False
    assert data[0]["created_at"] == task1.created_at.isoformat()

    assert data[1]["title"] == task2.title
    assert data[1]["isCompleted"] == True
    #assert data[1]["created_at"] == task2.created_at.isoformat()


# Тест на удаление задачи
@pytest.mark.asyncio
async def test_del_task(session: AsyncSession, client: AsyncClient):
    # Создать данные в базу
    task = TodoItems(
        id=1, title="Test delete task", isCompleted=False, created_at=datetime.now()
    )
    session.add(task)
    await session.commit()

    response = await client.delete("/api/todo/1")

    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Task deleted"


# Тест на удаление задачи, которой не существует
@pytest.mark.asyncio
async def test_del_task_not_found(session: AsyncSession, client: AsyncClient):
    response = await client.delete("api/todo/2")
    assert response.status_code == 404


# Тест на обновление задачи
@pytest.mark.asyncio
async def test_update_task(session: AsyncSession, client: AsyncClient):
    task = TodoItems(
        id=3, title="Task to check update", isCompleted=False, created_at=datetime.now()
    )
    session.add(task)
    await session.commit()

    response = await client.put(f"/api/todo/3", json={"isCompleted": True})

    data = response.json()

    assert response.status_code == 200
    #assert data["id"] == 3
    assert data["title"] == task.title
    assert data["isCompleted"] == True


# Тест на обновление задачи, которой не существует
@pytest.mark.asyncio
async def test_update_task_not_found(session: AsyncSession, client: AsyncClient):
    response = await client.put("'api/todo/1")
    assert response.status_code == 404


# Тест на обновление задачи с невалидными данными
@pytest.mark.asyncio
async def test_update_task_invalid(session: AsyncSession, client: AsyncClient):
    task = TodoItems(
        id=1, title="Task to check update", isCompleted=False, created_at=datetime.now()
    )
    session.add(task)
    await session.commit()

    response = await client.put(
        "/api/todo/1",
        json={
            "title": 12,
            "isCompleted": True,
        },
    )

    assert response.status_code == 422
