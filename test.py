import time
from typing import Any
from flask import Flask, jsonify
import pika
from pika.channel import Channel
import multiprocessing

app = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='tasks_queue')


@app.route('/add', methods=['GET'])
def add_task():
    channel.basic_publish(exchange='', routing_key='tasks_queue', body="hello2")
    return jsonify({'message': 'Task added successfully'})


def start_dispatcher():
    channel.basic_consume(
            queue="tasks_queue",
            auto_ack=True,
            on_message_callback=callback,
            consumer_tag="default",
        )
    channel.start_consuming()


def callback(ch: Channel, method: Any, properties: Any, body: Any) -> None:
    print(f" [x] Received {body}")


def start_flask_app():
    app.run(debug=True)


if __name__ == "__main__":
    dispatcher_process = multiprocessing.Process(target=start_dispatcher)
    flask_process = multiprocessing.Process(target=start_flask_app)

    dispatcher_process.start()
    flask_process.start()

    dispatcher_process.join()
    flask_process.join()
