from models.task import Priority, Status, Task


def test_can_instantiate_a_task() -> None:

    task = Task(description="Do the laundry", priority=Priority.HIGH, status=Status.TODO)
    assert task.description == "Do the laundry"
    assert task.priority == Priority.HIGH
    assert task.status == Status.TODO
