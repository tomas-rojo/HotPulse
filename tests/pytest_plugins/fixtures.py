from pytest import fixture

from config.dependency import Dependency
from ports.abstract_tasks_queue_repository import AbstractTasksQueueRepository


@fixture
def queue_repository() -> AbstractTasksQueueRepository:
    return Dependency.get(AbstractTasksQueueRepository)
