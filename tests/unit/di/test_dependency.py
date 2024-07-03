from pytest import raises

from config.dependency import Dependency


class Thing:
    pass


class ThingA(Thing):
    pass


class ThingB(Thing):
    pass


class ThingC(Thing):
    pass


def test_can_add_singleton() -> None:
    Dependency.add_singleton(Thing, Thing())
    assert isinstance(Dependency.get(Thing), Thing)
    assert Dependency.get(Thing) is Dependency.get(Thing)


def test_can_add_singleton_factory() -> None:
    Dependency.add_singleton_factory(Thing, lambda: Thing())
    thing1 = Dependency.get(Thing)
    thing2 = Dependency.get(Thing)
    assert isinstance(thing1, Thing)
    assert isinstance(thing2, Thing)
    assert thing1 is thing2


def test_can_add_factory() -> None:
    Dependency.add_factory(Thing, lambda: Thing())
    thing1 = Dependency.get(Thing)
    thing2 = Dependency.get(Thing)
    assert isinstance(thing1, Thing)
    assert isinstance(thing2, Thing)
    assert thing1 is not thing2


def test_add_can_override_existing_dependencies_in_container_before_call_to_new() -> None:
    Dependency.add_singleton(str, "other dependency")
    assert Dependency.get(str) == "other dependency"

    Dependency.add_singleton(Thing, ThingA())
    Dependency.add_factory(Thing, ThingB)

    thing = Dependency.get(Thing)
    assert isinstance(thing, ThingB)


def test_cannot_override_existing_dependencies_in_container_after_call_to_new() -> None:
    Dependency.add_singleton(Thing, ThingA())
    thing1 = Dependency.get(Thing)
    Dependency.add_singleton(Thing, ThingB())
    thing2 = Dependency.get(Thing)

    assert thing1 is thing2


def test_can_return_all_registered_dependencies_for_a_service() -> None:
    Dependency.add_singleton(Thing, ThingA())
    Dependency.add_singleton(Thing, ThingB())

    things = list(Dependency.get_all(Thing))
    assert len(things) == 2
    assert isinstance(things[0], ThingA)
    assert isinstance(things[1], ThingB)


def test_can_return_all_registered_dependencies_for_a_service_also_when_added_after_get() -> None:
    Dependency.add_singleton(Thing, ThingA())
    thing1 = Dependency.get(Thing)
    Dependency.add_factory(Thing, ThingB)
    thing2 = Dependency.get(Thing)
    Dependency.add_singleton_factory(Thing, ThingC)
    thing3 = Dependency.get(Thing)

    # The instance returned by get() is the one that was returned the first time.
    assert thing1 is thing2
    assert thing2 is thing3

    # But when retrieving all dependencies, then all three instances are provided.
    things = list(Dependency.get_all(Thing))
    assert len(things) == 3
    assert isinstance(things[0], ThingA)
    assert isinstance(things[1], ThingB)
    assert isinstance(things[2], ThingC)


def test_reset_clears_out_the_dependency_container() -> None:
    Dependency.add_singleton(ThingA, ThingA())
    Dependency.add_singleton(str, "Hello, world!")
    Dependency.add_singleton(int, 73)

    assert isinstance(Dependency.get(ThingA), ThingA)
    assert Dependency.get(str) == "Hello, world!"
    assert Dependency.get(int) == 73

    Dependency.reset()

    with raises(Dependency.Missing):
        Dependency.get(ThingA)
    with raises(Dependency.Missing):
        Dependency.get(str)
    with raises(Dependency.Missing):
        Dependency.get(int)
