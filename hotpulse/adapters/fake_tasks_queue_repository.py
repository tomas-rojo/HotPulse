import contextlib
from collections import OrderedDict, defaultdict

from models.task import Task
from ports.abstract_tasks_queue_repository import AbstractTasksQueueRepository


class FakeTaskQueueRepository(AbstractTasksQueueRepository):

    def __init__(self) -> None:
        self._hotel_tasks_queue: dict[str, OrderedDict[str, Task]] = defaultdict(OrderedDict)

    def enqueue(self, queue_id: str, task: Task) -> None:
        self._hotel_tasks_queue[queue_id][task.id] = task

    def dequeue(self, queue_id: str) -> None:
        with contextlib.suppress(KeyError):
            del self._hotel_tasks_queue[queue_id]

    def get_all_hotel_tasks(self) -> OrderedDict[str, Task]:
        try:
            return self._hotel_tasks_queue["hotel_tasks"].copy()
        except KeyError:
            return OrderedDict()
