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
    description: str
    priority: Priority
    status: Status = Status.TODO
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime | None = None
    closed_at: datetime | None = None
