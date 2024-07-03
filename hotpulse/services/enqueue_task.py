from config.dependency import Dependency
from models.task import Task
from ports.abstract_tasks_queue_repository import AbstractTasksQueueRepository


def enqueue_task(task: Task) -> None:
    queue_repository: AbstractTasksQueueRepository = Dependency.get(AbstractTasksQueueRepository)
    queue_repository.enqueue(task.id, task)
