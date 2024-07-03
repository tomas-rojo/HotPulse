from datetime import datetime
import uuid

from flask import Blueprint, Response, jsonify, render_template, request

from exceptions.queue_connection_error import QueueConnectionError
from models.task import Priority, Status, Task
from services.get_tasks import get_all
from services.enqueue_task import enqueue_task

bp = Blueprint("api", __name__)


def get_priority(priority: str) -> Priority:
    match priority.lower():
        case "low":
            return Priority.LOW
        case "medium":
            return Priority.MEDIUM
        case "high":
            return Priority.HIGH
        case _:
            raise ValueError("Invalid priority")


def generate_id() -> str:
    return str(uuid.uuid4())


@bp.route("/api", methods=["GET", "POST"])
def api() -> str | tuple[Response, int]:  # noqa
    if request.method == "POST":
        try:
            task = Task(
                id=generate_id(),
                description=request.form.get("description", default=""),
                status=Status.TODO,
                priority=get_priority(request.form.get("priority", default="")),
                created_at=datetime.now(),
            )
            enqueue_task(task)
        except ValueError as e:
            return jsonify(message=f"{e}"), 400
        except QueueConnectionError as e:
            return jsonify(message=str(e)), 503
    return render_template("index.html", tasks=get_all())
