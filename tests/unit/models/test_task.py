import re

import pytest

from models.task import Priority, Status, Task


def test_can_instantiate_a_task() -> None:
    task = Task(description="Do the laundry", priority=Priority.HIGH, status=Status.TODO
    )
    assert task.description == "Do the laundry"
    assert task.priority == Priority.HIGH
    assert task.status == Status.TODO


def test_can_not_instantiate_task_with_null_values() -> None:

    with pytest.raises(ValueError):
        Task(description=None, priority=Priority.HIGH, status=Status.TODO)  # type: ignore
        Task(description="", priority=Priority.HIGH, status=Status.TODO)

    with pytest.raises(ValueError, match=re.escape("Priority is empty or is invalid")):
        Task(description="Do the laundry", priority=None, status=Status.TODO)  # type: ignore
        Task(description="Do the laundry", priority="InvalidPriority", status=Status.TODO)  # type: ignore

    with pytest.raises(ValueError, match=re.escape("Status is empty or is invalid")):
        Task(description="Do the laundry", priority=Priority.HIGH, status=None)  # type: ignore
        Task(description="Do the laundry", priority=Priority.HIGH, status="InvalidStatus")  # type: ignore
