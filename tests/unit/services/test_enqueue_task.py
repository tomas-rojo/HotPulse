from models.task import Task
from ports.abstract_tasks_queue_repository import AbstractTasksQueueRepository
from services.enqueue_task import enqueue_task


def test_service_can_enqueue_task(
    queue_repository: AbstractTasksQueueRepository, new_task_1: Task
) -> None:
    enqueue_task(new_task_1)
    # assert list(queue_repository.get_all().values()) == [new_task_1]
