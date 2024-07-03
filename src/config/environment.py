from os import environ
from typing import Callable

from config.config import DevelopmentConfig, TestingConfig
from config.dependency import Dependency


class Environment:
    """This helper can be used to create an environment-specific
    DI configuration, based on the environment variable APP_ENVIRONMENT."""

    environments: dict[str, Callable[[], None]] = {
        "development": DevelopmentConfig().bootstrap,
        "integration": TestingConfig().bootstrap,
    }

    @staticmethod
    def bootstrap() -> None:
        """Bootstraps the DI configuration."""
        environment_name = Environment.get_environment_name()
        return Environment.create_config(environment_name)

    @staticmethod
    def get_environment_name() -> str:
        if environment_name := environ.get("APP_ENVIRONMENT", None):
            return environment_name
        else:
            raise SystemError("Environment variable APP_ENVIRONMENT is not set")

    @staticmethod
    def create_config(environment_name: str) -> None:
        try:
            Environment.environments[environment_name]()
        except KeyError as e:
            raise SystemError(
                f"Invalid value {e.__str__()} for environment variable APP_ENVIRONMENT"
            ) from None

    @staticmethod
    def teardown() -> None:
        Dependency.reset()
