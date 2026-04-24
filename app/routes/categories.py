from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app import db
from app.models import CategoryModel
from app.schemas import (
    CategorySchema,
    CategoryListResponseSchema,
    MessageSchema,
)

blp = Blueprint("categories", __name__, url_prefix="", description="Category endpoints")


@blp.route("/categories")
class CategoryList(MethodView):
    @blp.response(200, CategoryListResponseSchema)
    def get(self):
        categories = CategoryModel.query.all()

        result = []
        for category in categories:
            category.task_count = len(category.tasks)
            result.append(category)

        return {"categories": result}

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        category = CategoryModel(**category_data)

        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Category with this name already exists.")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Database error")

        category.task_count = 0
        return category


@blp.route("/categories/<int:category_id>")
class Category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id, description="Category not found")
        category.task_count = len(category.tasks)
        return category

    @blp.response(200, MessageSchema)
    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id, description="Category not found")

        if len(category.tasks) > 0:
            abort(
                400,
                message="Cannot delete category with existing tasks. Move or delete tasks first."
            )

        try:
            db.session.delete(category)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="Database error")

        return {"message": "Category deleted"}