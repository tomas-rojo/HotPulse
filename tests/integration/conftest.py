import os
from collections.abc import Generator

from pytest import fixture

from config.environment import Environment


@fixture(autouse=True)
def setup_integration_environment() -> Generator[None, None, None]:
    """Initializes and cleans up the dependency injection container that
    is used for setting up the integration testing dependencies."""
    os.environ["APP_ENVIRONMENT"] = "integration"
    Environment.bootstrap()
    yield
    Environment.teardown()
