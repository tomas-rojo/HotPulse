import time
from dataclasses import dataclass, field

from models.task import Task


def make_timestamp() -> int:
    return int(time.time() * 10000000)


@dataclass(kw_only=True, slots=True, frozen=True)
class QueueId:
    task: Task
    current_epoch_time: int = field(default_factory=make_timestamp)

    def __str__(self) -> str:
        hash_task_fragment = str(hash(self.task))[:8]
        return f"{self.current_epoch_time}_{hash_task_fragment}"
