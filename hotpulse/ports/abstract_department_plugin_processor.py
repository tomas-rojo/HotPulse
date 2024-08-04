from models.task import Task


class AbstractDepartmentTasksProcessorPlugin:
    """This base class defines the interface for implementing a trap
    processing plugin for the SNMP trap receiver application.

    The plugin can selectively process specific types of traps,
    separating the concerns of "what to do with SNMP traps" from
    "capturing and queueing SNMP traps for subsequent processing."
    """

    def __init__(self, department_name: str, description: str) -> None:
        self._department_name = department_name
        self._description = description

    @property
    def department_name(self) -> str:
        """A unique identifier for this plugin."""
        return self._department_name

    @property
    def description(self) -> str:
        """A human-friendly description for this plugin."""
        return self._description

    def process(self, task: Task) -> bool:
        """Can be implemented for processing traps.

        Returns True if the plugin performed some action on the trap, False otherwise.
        This return value is only used for reporting purposes.

        Must raise a TemporaryException when an error occurs for which a retry
        might fix the issue (e.g. when some network service is unavailable).

        Can raise a FatalException when an error occurs for which a retry
        will not fix the issue. Any other exception will be interpreted as a
        fatal exception as well."""

        return False
