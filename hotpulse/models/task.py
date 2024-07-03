import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Status(Enum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3


@dataclass(frozen=True, slots=True)
class Task:
    id: str
    description: str
    priority: Priority
    status: Status = Status.TODO
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime | None = None
    closed_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.description:
            raise ValueError("Description is empty")
        if not self.priority or not isinstance(self.priority, Priority):
            raise ValueError("Priority is empty or is invalid")
        if not self.status or not isinstance(self.status, Status):
            raise ValueError("Status is empty or is invalid")
