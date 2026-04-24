import os
from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import redis
from rq import Queue

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Task Manager API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["REDIS_URL"] = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    db.init_app(app)
    migrate.init_app(app, db)

    redis_conn = redis.from_url(app.config["REDIS_URL"])
    app.queue = Queue("default", connection=redis_conn)

    api = Api(app)

    from app.routes.categories import blp as CategoryBlueprint
    from app.routes.tasks import blp as TaskBlueprint

    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(TaskBlueprint)

    return app