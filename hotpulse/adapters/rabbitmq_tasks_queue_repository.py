from collections import OrderedDict
import pickle
from typing import Any

import pika.exceptions
from pika.channel import Channel

from exceptions.queue_connection_error import QueueConnectionError
from models.task import Task


class RabbitMqTaskQueueRepository:
    def __init__(self, url: str) -> None:
        self._url = url

    def _create_connection(self) -> pika.BlockingConnection:
        try:
            return pika.BlockingConnection(pika.URLParameters(self._url))
        except pika.exceptions.AMQPConnectionError as e:
            raise QueueConnectionError from e

    def enqueue(self, queue_id: str, task: Task) -> None:
        connection = self._create_connection()
        channel = connection.channel()
        task_json = pickle.dumps(task)
        channel.queue_declare(queue=queue_id)
        channel.basic_publish(exchange="", routing_key=queue_id, body=task_json)

    def start_queue_handling(self, queue: str) -> None:
        connection = self._create_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_consume(
            queue=queue,
            auto_ack=True,
            on_message_callback=self.callback,
            consumer_tag="default",
        )
        print(" [] Start Consuming...")
        channel.start_consuming()

    def callback(self, ch: Channel, method: Any, properties: Any, body: Any) -> None:
        task: Task = pickle.loads(body)
        print(f" [x] Received {task}")

    def dequeue(self, queue_id: str) -> Task:
        return None

    def get_all(self) -> OrderedDict[str, Task]:
        connection = self._create_connection()
        channel = connection.channel()
        messages = {}
        while True:
            method_frame, header_frame, body = channel.basic_get(queue="hotel_tasks")
            if method_frame is None:
                break
            task: Task = pickle.loads(body)
            messages[task.id] = task
        return messages
