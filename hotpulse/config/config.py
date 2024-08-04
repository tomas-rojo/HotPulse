from adapters.fake_tasks_queue_repository import FakeTaskQueueRepository
from adapters.rabbitmq_tasks_queue_repository import RabbitMqTaskQueueRepository
from config.dependency import Dependency
from ports.abstract_tasks_queue_repository import AbstractTasksQueueRepository


class BaseConfig:
    def set_env_label(self, label: str) -> None:
        Dependency.add_singleton("env_label", label)


class DevelopmentConfig(BaseConfig):
    def bootstrap(self) -> None:
        Dependency.add_singleton_factory(AbstractTasksQueueRepository, FakeTaskQueueRepository)
        self.set_env_label("development")


class TestingConfig(BaseConfig):
    def bootstrap(self) -> None:
        Dependency.add_factory(
            AbstractTasksQueueRepository,
            lambda: RabbitMqTaskQueueRepository("amqp://guest:guest@127.0.0.1:5672"),
        )
        self.set_env_label("testing")
