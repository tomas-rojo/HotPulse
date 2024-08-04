from models.task import Task
from ports.abstract_department_plugin_processor import AbstractDepartmentTasksProcessorPlugin


class FrontDeskTasksPluginProcessor(AbstractDepartmentTasksProcessorPlugin):
        def __init__(self) -> None:
            super().__init__(plugin_id="front-desk", description="Front Desk tasks processor")

        def process(self, task: Task) -> bool:
            pass
