from models.queue_id import QueueId
from models.task import Priority, Status, Task
from ports.abstract_tasks_queue_repository import AbstractTasksQueueRepository


def test_tasks_queue_repository_should_not_raise_exception_for_unknown_queue_id(
    queue_repository: AbstractTasksQueueRepository,
) -> None:
    queue_id = "nonexistent_queue_id"
    assert queue_repository.dequeue(queue_id) is None


def test_tasks_queue_repository_can_enqueue_multiple_tasks_in_sequential_order(
    queue_repository: AbstractTasksQueueRepository,
) -> None:
    task_1 = Task(id="1", description="Do the laundry", priority=Priority.LOW, status=Status.TODO)
    task_2 = Task(id="2", description="Get new TV batteries", priority=Priority.MEDIUM, status=Status.TODO)
    task_3 = Task(id="3", description="Fix curtains", priority=Priority.HIGH, status=Status.TODO)
    queue_id_1 = str(QueueId(task=task_1))
    queue_id_2 = str(QueueId(task=task_2))
    queue_id_3 = str(QueueId(task=task_3))
    queue_repository.enqueue(queue_id_1, task_1)
    queue_repository.enqueue(queue_id_2, task_2)
    queue_repository.enqueue(queue_id_3, task_3)

    # Ensure tasks are returned in FIFO order
    tasks = queue_repository.get_all()
    assert len(tasks) == 3
    assert list(tasks.keys()) == [queue_id_1, queue_id_2, queue_id_3]
    assert tasks[queue_id_1] == task_1
    assert tasks[queue_id_2] == task_2
    assert tasks[queue_id_3] == task_3


def test_queue_repository_can_enqueue_multiple_tasks_in_different_order(
    queue_repository: AbstractTasksQueueRepository,
) -> None:
    task_1 = Task(id="1", description="Do the laundry", priority=Priority.LOW, status=Status.TODO)
    task_2 = Task(id="2", description="Get new TV batteries", priority=Priority.MEDIUM, status=Status.TODO)
    task_3 = Task(id="3", description="Fix curtains", priority=Priority.HIGH, status=Status.TODO)
    queue_id_2 = str(QueueId(task=task_2))
    queue_id_1 = str(QueueId(task=task_1))
    queue_id_3 = str(QueueId(task=task_3))
    queue_repository.enqueue(queue_id_2, task_2)
    queue_repository.enqueue(queue_id_1, task_1)
    queue_repository.enqueue(queue_id_3, task_3)

    # Ensure tasks are returned in FIFO order
    tasks = queue_repository.get_all()
    assert len(tasks) == 3
    assert list(tasks.keys()) == [queue_id_2, queue_id_1, queue_id_3]
    assert tasks[queue_id_1] == task_1
    assert tasks[queue_id_2] == task_2
    assert tasks[queue_id_3] == task_3


def test_queue_repository_can_dequeue_multiple_tasks(
    queue_repository: AbstractTasksQueueRepository,
) -> None:
    task_1 = Task(id="1", description="Do the laundry", priority=Priority.LOW, status=Status.TODO)
    task_2 = Task(id="2", description="Get new TV batteries", priority=Priority.MEDIUM, status=Status.TODO)
    task_3 = Task(id="3", description="Fix curtains", priority=Priority.HIGH, status=Status.TODO)
    task_4 = Task(id="4", description="Check mails", priority=Priority.LOW, status=Status.TODO)
    queue_id_1 = str(QueueId(task=task_1))
    queue_id_2 = str(QueueId(task=task_2))
    queue_id_3 = str(QueueId(task=task_3))
    queue_id_4 = str(QueueId(task=task_4))

    # We start with 4 tasks in the queue
    queue_repository.enqueue(queue_id_2, task_2)
    queue_repository.enqueue(queue_id_1, task_1)
    queue_repository.enqueue(queue_id_4, task_4)
    queue_repository.enqueue(queue_id_3, task_3)
    tasks_pre = queue_repository.get_all()
    assert len(tasks_pre) == 4

    # Let's dequeue 2 tasks from the middle...
    queue_repository.dequeue(queue_id_1)
    queue_repository.dequeue(queue_id_4)
    tasks_post = queue_repository.get_all()

    # We should have 2 tasks remaining
    assert len(tasks_post) == len(tasks_pre) - 2
    assert list(tasks_post.keys()) == [queue_id_2, queue_id_3]

    assert tasks_post[queue_id_2] == task_2
    assert tasks_post[queue_id_3] == task_3

    # Dequeue the remaining tasks and we should have an empty queue
    queue_repository.dequeue(queue_id_2)
    queue_repository.dequeue(queue_id_3)
    tasks_final = queue_repository.get_all()
    assert len(tasks_final) == 0
