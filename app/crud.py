from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from app.models import TodoItems
from app.schemas import TodoCreate, TodoUpdate

from datetime import datetime

# class TodoService():
#     def __init__ (self):

# Получение всех задач
async def get_all_tasks(db: AsyncSession):
    result = await db.execute(select(TodoItems))
    return result.scalars().all()


# Создание задачи
async def create_todo(todo: TodoCreate, db: AsyncSession) -> TodoItems:
    new_task = TodoItems(
        title=todo.title,
        isCompleted=todo.isCompleted,
        created_at=todo.createAt or datetime.now(),
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


# Получение задачи по ID
async def get_task(id: int, db: AsyncSession):
    result = await db.execute(select(TodoItems).where(TodoItems.id == id))
    return result.scalars().first()


# Удаление задачи
async def delete_task(id: int, db: AsyncSession):
    result = await db.execute(select(TodoItems).where(TodoItems.id == id))
    task = result.scalars().first()
    if task:
        await db.delete(task)
        await db.commit()
        return {"message": "Task deleted"}
    return None


# Обновление задачи
async def update_todo(id: int, todo_update: TodoUpdate, db: AsyncSession):
    result = await db.execute(select(TodoItems).where(TodoItems.id == id))
    task = result.scalars().first()

    if not task:
        return None

    if todo_update.title is not None:
        task.title = todo_update.title
    if todo_update.isCompleted is not None:
        task.isCompleted = todo_update.isCompleted
    if todo_update.createAt is not None:
        task.created_at = todo_update.createAt

    await db.commit()
    await db.refresh(task)
    return task
