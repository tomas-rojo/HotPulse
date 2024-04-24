import contextlib
from collections import OrderedDict

from models.task import Task
from ports.abstract_tasks_queue_repository import AbstractTasksQueueRepository


class FakeTaskQueueRepository(AbstractTasksQueueRepository):

    def __init__(self) -> None:
        self._received_traps: OrderedDict[str, Task] = OrderedDict()
        super().__init__()

    def enqueue(self, queue_id: str, task: Task) -> None:
        self._received_traps[queue_id] = task

    def dequeue(self, queue_id: str) -> None:
        with contextlib.suppress(KeyError):
            del self._received_traps[queue_id]

    def get_all(self) -> OrderedDict[str, Task]:
        return self._received_traps.copy()
