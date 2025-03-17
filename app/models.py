from sqlalchemy import Integer, String, Column, DateTime, Boolean
from sqlalchemy.orm import declarative_base

# Базовый класс для моделей
Base = declarative_base()


# Сущность TodoItem
class TodoItems(Base):
    __tablename__ = "TodoItems"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    isCompleted = Column(Boolean)
    created_at = Column(DateTime)
