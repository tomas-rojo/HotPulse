from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any, TypeVar, cast

import punq

T = TypeVar("T")


class Dependency:
    _services: punq.Container | None = None

    class Missing(Exception):
        """This exception is raised when a service is requested from the
        services container that was not (yet) added to the container."""

        pass

    @classmethod
    def reset(cls) -> None:
        """Reset the services container. This is mainly useful for testing
        purposes, when the services have to be reset after running tests."""
        cls._services = None

    @classmethod
    def add_singleton(cls, service: Callable[..., T], instance: Any) -> None:
        """Adds a singleton to the dependency container. This service must be
        the instance that must be returned by get(). Each time get() is called,
        the same instance will be returned."""
        cls._punq().register(service, instance=instance)

    @classmethod
    def add_singleton_factory(cls, service: Callable[..., T], factory: Callable[[], T]) -> None:
        """Adds a singleton to the dependency container in the form of a constructor
        function, that is used for creating a singleton instance. The singleton will be
        instantiated the first time get() is called for this factory. Each subsequent get()
        call will return the same instance."""
        cls._punq().register(service, factory=factory, scope=punq.Scope.singleton)

    @classmethod
    def add_factory(cls, service: Callable[..., T], factory: Callable[[], T]) -> None:
        """Adds a factory to the dependency container in the form of a constructor
        function. Each time get() is called, a new instance will be created by calling
        this factory function."""
        cls._punq().register(service, factory=factory)

    @classmethod
    def get(cls, service: Callable[..., T]) -> T:
        """Retrieve a previously added service from the dependency container.
        When the requested service does not exist, a Dependency.Missing exception
        is raised."""
        try:
            return cast(T, cls._punq().resolve(service))
        except punq.MissingDependencyError as e:
            raise Dependency.Missing(str(e)) from e

    @classmethod
    def get_all(cls, service: Callable[[], T]) -> Iterator[T]:
        """Retrieve a list of previously added dependencies from the dependency container
        for the provided service. When no services were added, an empty list is
        returned."""
        return cast(Iterator[T], cls._punq().resolve_all(service))

    @classmethod
    def _punq(cls) -> punq.Container:
        """Used internally for retrieving a singleton instance of the dependency
        container implementation that provides the low level support for this
        class' functionality."""
        if cls._services is None:
            cls._services = punq.Container()
        return cls._services
