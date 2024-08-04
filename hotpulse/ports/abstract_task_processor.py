from abc import ABC, abstractmethod

from models.task import Task


class AbstractTaskProcessor(ABC):
    
    @abstractmethod
    def process_trask(self, task: Task) -> None:
        pass
