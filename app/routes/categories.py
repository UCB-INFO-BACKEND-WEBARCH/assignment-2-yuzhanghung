from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app import db
from models import CategoryModel
from schemas import CategorySchema

blp = Blueprint("categories", __name__, description="categories")


@blp.route("/categories")
class CategoryList(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()
    
    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        category = CategoryModel(**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="Category name already exists"
            )
        except SQLAlchemyError:
            abort(500, message="Database error")

        return category


    


@blp.route("/categories/<int:category_id>")
class Category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        return category
    

    def delete(self, category_id):
        category = CategoryModel.query.get_or_404(category_id)
        if category.tasks and len(category.tasks) > 0:
            abort(
                400,
                message="Cannot delete category with existing tasks. Move or delete tasks first."
            )
            
        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted"}, 200

