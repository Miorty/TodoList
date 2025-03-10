from fastapi import status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import create_todo, get_all_tasks, get_task, delete_task, update_todo
from app.schemas import TodoCreate, TodoUpdate
from app.cache import get_cache, cache_task
from app.databaseTD import get_db
import redis
import json

router = APIRouter(prefix="/api/todo")

# Получение всех задач
@router.get("/")
async def read_tasks(
    db: AsyncSession = Depends(get_db),
    cache: redis = Depends(get_cache),
):
    cached_tasks = await cache.get("todos")

    if cached_tasks:
        return json.loads(cached_tasks)

    tasks = await get_all_tasks(db)

    task_list = [await cache_task(task) for task in tasks]
    await cache.set("todos", json.dumps(task_list), ex=120)

    return task_list


# Добавление новой задачи
@router.post("/")
async def create_task(
    todo: TodoCreate,
    db: AsyncSession = Depends(get_db),
    cache: redis = Depends(get_cache),
):
    try:
        task = await create_todo(todo, db)
        task_dict = await cache_task(task)
        await cache.set(f"todo:{id}", json.dumps(task_dict), ex=120)
        await cache.delete("todos")
        # return HTTPException(status_code=status.HTTP_201_CREATED)
        return task

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

# Получение задани по ID
@router.get("/{id}")
async def read_task(
    id: int, db: AsyncSession = Depends(get_db), cache: redis = Depends(get_cache)
):
    cached_item = await cache.get(f"todo:{id}")
    if cached_item:
        return json.loads(cached_item)

    task = await get_task(id, db)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task_dict = await cache_task(task)
    await cache.set(f"todo:{id}", json.dumps(task_dict), ex=120)
    return task


# Удаление задачи
@router.delete("/{id}")
async def del_task(
    id: int,
    db: AsyncSession = Depends(get_db),
    cache: redis = Depends(get_cache),
):
    task = await delete_task(id, db)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    await cache.delete(f"todo:{id}")
    await cache.delete("todos")
    return task


# Обновление задачи
@router.put("/{id}")
async def update_task(
    id: int,
    todo: TodoUpdate,
    db: AsyncSession = Depends(get_db),
    cache: redis = Depends(get_cache),
):
    task = await update_todo(id, todo, db)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    await cache.delete(f"todo:{id}")
    await cache.delete("todos")

    task_dict = await cache_task(task)
    await cache.set(f"todo:{id}", json.dumps(task_dict), ex=120)

    return task
