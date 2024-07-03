from abc import ABC, abstractmethod
from collections import OrderedDict

from models.task import Task


class AbstractTasksQueueRepository(ABC):
    """The component responsible for storing and retrieving tasks from the queue"""

    @abstractmethod
    def enqueue(self, queue_id: str, task: Task) -> None:
        raise NotImplementedError

    @abstractmethod
    def dequeue(self, queue_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> OrderedDict[str, Task]:
        raise NotImplementedError
