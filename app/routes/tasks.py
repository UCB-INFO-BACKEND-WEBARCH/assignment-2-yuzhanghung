from datetime import datetime, timedelta, timezone

from flask import current_app, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import TaskModel
from app.schemas import (
    TaskSchema,
    TaskListResponseSchema,
    TaskCreateResponseSchema,
    MessageSchema,
)
from app.jobs import send_due_soon_reminder

blp = Blueprint("tasks", __name__, url_prefix="", description="Task endpoints")


def should_queue_notification(due_date):
    if due_date is None:
        return False

    now = datetime.now(timezone.utc)

    if due_date.tzinfo is None:
        due_date = due_date.replace(tzinfo=timezone.utc)

    return now < due_date <= now + timedelta(hours=24)


@blp.route("/tasks")
class TaskList(MethodView):
    @blp.response(200, TaskListResponseSchema)
    def get(self):
        completed = request.args.get("completed")
        query = TaskModel.query

        if completed is not None:
            if completed.lower() == "true":
                query = query.filter(TaskModel.completed.is_(True))
            elif completed.lower() == "false":
                query = query.filter(TaskModel.completed.is_(False))

        return {"tasks": query.all()}

    @blp.arguments(TaskSchema)
    @blp.response(201, TaskCreateResponseSchema)
    def post(self, task_data):
        task = TaskModel(**task_data)
        notification_queued = False

        try:
            db.session.add(task)
            db.session.commit()

            if should_queue_notification(task.due_date):
                current_app.queue.enqueue(send_due_soon_reminder, task.title)
                notification_queued = True

        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Database error")

        return {
            "task": task,
            "notification_queued": notification_queued
        }


@blp.route("/tasks/<int:task_id>")
class Task(MethodView):
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        return TaskModel.query.get_or_404(task_id, description="Task not found")

    @blp.arguments(TaskSchema(partial=True))
    @blp.response(200, TaskSchema)
    def put(self, task_data, task_id):
        task = TaskModel.query.get_or_404(task_id, description="Task not found")

        for key, value in task_data.items():
            setattr(task, key, value)

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Database error")

        return task

    @blp.response(200, MessageSchema)
    def delete(self, task_id):
        task = TaskModel.query.get_or_404(task_id, description="Task not found")

        try:
            db.session.delete(task)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Database error")

        return {"message": "Task deleted"}