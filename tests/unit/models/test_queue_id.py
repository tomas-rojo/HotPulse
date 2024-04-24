from models.queue_id import QueueId
from models.task import Task


def test_queue_id_creation(new_task_1: Task) -> None:
    queue_id = QueueId(task=new_task_1)
    assert queue_id.task == new_task_1
    assert queue_id.current_epoch_time is not None


def test_queue_id_str_format(new_task_1: Task) -> None:
    queue_id = QueueId(task=new_task_1)
    hash_task_fragment = str(hash(new_task_1))[:8]
    assert str(queue_id) == f"{queue_id.current_epoch_time}_{hash_task_fragment}"
