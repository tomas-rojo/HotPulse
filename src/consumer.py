from adapters.rabbitmq_tasks_queue_repository import RabbitMqTaskQueueRepository

if __name__ == "__main__":
    # Create a RabbitMQTasksQueueRepository instance
    queue_repository = RabbitMqTaskQueueRepository("amqp://guest:guest@localhost:5672")
    queue_repository.start_queue_handling(queue="hotel_tasks")
