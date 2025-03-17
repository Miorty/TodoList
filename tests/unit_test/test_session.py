from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, call
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import TodoItems
from app.schemas import TodoCreate
from app.crud import create_todo

class MyTestCase(IsolatedAsyncioTestCase):
    async def test_create_new_item(self) -> None:
        test_item = TodoCreate(title="New task for testing create")
        mock_session = AsyncMock(spec=AsyncSession)

        expected_output = TodoItems(
            title=test_item.title,
            isCompleted=test_item.isCompleted,
            created_at=test_item.createAt
        )

        output = await create_todo(test_item, mock_session)

        self.assertEqual(expected_output.title, output.title)
        self.assertEqual(expected_output.isCompleted, output.isCompleted)
        self.assertEqual(expected_output.created_at, output.created_at)

    async def test_read_task_id(self) -> None:
        test_item = TodoCreate(title="Task for testing to read")
        mock_session = AsyncMock(spec=AsyncSession)

        expected_output = TodoItems(
            title=test_item.title,
            isCompleted=test_item.isCompleted,
            created_at=test_item.createAt
        )




