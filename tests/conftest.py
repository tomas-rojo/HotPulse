from datetime import datetime

from pytest import fixture

from adapters.fake_tasks_queue_repository import FakeTaskQueueRepository
from models.task import Priority, Status, Task


@fixture
def queue_repository() -> FakeTaskQueueRepository:
    return FakeTaskQueueRepository()


@fixture
def new_task_1() -> Task:
    return Task(
        description="Task 1",
        status=Status.TODO,
        priority=Priority.LOW,
        created_at=datetime.strptime("01/01/24 00:00:00", "%m/%d/%y %H:%M:%S"),
    )
