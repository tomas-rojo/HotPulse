from collections import OrderedDict

from config.dependency import Dependency
from models.task import Task
from ports.abstract_tasks_queue_repository import AbstractTasksQueueRepository


def get_all() -> OrderedDict[str, Task]:
    queue_repository: AbstractTasksQueueRepository = Dependency.get(AbstractTasksQueueRepository)
    return queue_repository.get_all_hotel_tasks()
