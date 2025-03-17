from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    isCompleted: Optional[bool] = False
    createAt: Optional[datetime] = Field(default=datetime.now())


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    isCompleted: Optional[bool] = None
    createAt: Optional[datetime] = None
