from os import environ

from pytest import raises

from config.dependency import Dependency
from config.environment import Environment


def test_missing_environment_var_raises_exception() -> None:
    environ.pop("APP_ENVIRONMENT", None)
    with raises(SystemError, match="Environment variable APP_ENVIRONMENT is not set"):
        Environment.bootstrap()


def test_unknown_environment_raises_exception() -> None:
    environ["APP_ENVIRONMENT"] = "pr0ducti0n"
    with raises(
        SystemError, match="Invalid value 'pr0ducti0n' for environment variable APP_ENVIRONMENT"
    ):
        Environment.bootstrap()


def test_can_bootstrap_environment() -> None:
    environ["APP_ENVIRONMENT"] = "development"
    Environment.bootstrap()
    assert Dependency.get("env_label") == "development"
