import os
from collections.abc import Generator
from datetime import datetime

from pytest import fixture

from config.environment import Environment
from models.task import Priority, Status, Task


@fixture
def new_task_1() -> Task:
    return Task(
        id="task_1",
        description="Task 1",
        status=Status.TODO,
        priority=Priority.LOW,
        created_at=datetime.strptime("01/01/24 00:00:00", "%m/%d/%y %H:%M:%S"),
    )


@fixture(autouse=True)
def setup_unit_test_environment() -> Generator[None, None, None]:
    """Initializes and cleans up the dependency injection container that
    is used for setting up the unit testing dependencies."""
    os.environ["APP_ENVIRONMENT"] = "development"
    Environment.bootstrap()
    yield
    Environment.teardown()
