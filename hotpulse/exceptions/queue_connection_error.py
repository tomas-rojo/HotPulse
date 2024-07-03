class QueueConnectionError(Exception):
    def __init__(self) -> None:
        super().__init__("There was a problem trying to connect to the queue")
