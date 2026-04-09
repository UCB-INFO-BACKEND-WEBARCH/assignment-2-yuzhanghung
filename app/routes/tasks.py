from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app import db
from models import TaskModel
from schemas import TaskSchema

from app.jobs import notify_task_created

blp = Blueprint("tasks", __name__, description="task")

@blp.route("/tasks")
class TaskList(MethodView):
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        return TaskModel.query.all()
    
    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, task_data):
        task = TaskModel(**task_data)

        try:
            db.session.add(task)
            db.session.commit()
            current_app.queue.enqueue(
                notify_task_created,
                task.title
            )
        except IntegrityError:
            abort(
                400,
                message="Error creating task"
            )
        except SQLAlchemyError:
            abort(500, message="Database error")

        return task
        

        
    

@blp.route("/tasks/<int:task_id>")
class Task(MethodView):
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        return task

    @blp.arguments(TaskSchema)
    @blp.response(200, TaskSchema)
    def put(self, task_data, task_id):
        task = TaskModel.query.get_or_404(task_id)
        if task:
            task.title = task_data["title"]
            task.description = task_data.get("description")
            task.completed = task_data.get("completed", task.completed)
            task.category_id = task_data.get("category_id")
        else:
            task = TaskModel(id=task_id, **task_data)

        db.session.add(task)
        db.session.commit()

        return task
    
    def delete(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted"}, 200
    



    

    
