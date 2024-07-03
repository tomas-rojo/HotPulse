import threading
import time

import pika
from flask import Flask

from adapters.rabbitmq_tasks_queue_repository import RabbitMqTaskQueueRepository
from models.task import Priority, Status, Task

# Flask app
app = Flask(__name__)


@app.route("/")
def hello():
    queue_repository = RabbitMqTaskQueueRepository("amqp://guest:guest@localhost:5672")
    task = Task(
        id="id_1",
        description="test",
        priority=Priority.MEDIUM,
        status=Status.TODO,
    )
    queue_repository.enqueue("hello", task)
    return "Hello, World!"


def run_flask():
    app.run(debug=True, use_reloader=False)


# RabbitMQ consumer
def consume() -> None:
    queue_repository = RabbitMqTaskQueueRepository("amqp://guest:guest@localhost:5672")
    queue_repository.start_queue_handling(queue="hello")


if __name__ == "__main__":
    # Create threads
    flask_thread = threading.Thread(target=run_flask)
    rabbitmq_thread = threading.Thread(target=consume)

    # Start threads
    flask_thread.start()
    rabbitmq_thread.start()

    # Join threads to the main thread
    flask_thread.join()
    rabbitmq_thread.join()
