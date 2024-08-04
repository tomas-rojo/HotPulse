from typing import Iterable
from models.task import Task
from ports.abstract_department_plugin_processor import AbstractDepartmentTasksProcessorPlugin
from ports.abstract_task_processor import AbstractTaskProcessor


class TaskProcessort(AbstractTaskProcessor):
    

    def __init__(self) -> None:
        plugins: Iterable[AbstractDepartmentTasksProcessorPlugin]
    
    def process_task(self, task: Task) -> None:
        pass
