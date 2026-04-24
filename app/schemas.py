from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models import CategoryModel


class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    color = fields.Str(
        allow_none=True,
        validate=validate.Regexp(r"^#(?:[0-9a-fA-F]{6})$")
    )


class PlainTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(
        allow_none=True,
        validate=validate.Length(max=500)
    )
    completed = fields.Bool(load_default=False)
    due_date = fields.DateTime(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TaskSchema(PlainTaskSchema):
    category_id = fields.Int(allow_none=True, load_default=None)
    category = fields.Nested(PlainCategorySchema, dump_only=True)

    @validates("category_id")
    def validate_category_id(self, value, **kwargs):
        if value is not None and not CategoryModel.query.get(value):
            raise ValidationError("Category does not exist.")


class CategoryTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(dump_only=True)
    completed = fields.Bool(dump_only=True)


class CategorySchema(PlainCategorySchema):
    task_count = fields.Int(dump_only=True)
    tasks = fields.List(fields.Nested(CategoryTaskSchema), dump_only=True)


class TaskListResponseSchema(Schema):
    tasks = fields.List(fields.Nested(TaskSchema))


class CategoryListResponseSchema(Schema):
    categories = fields.List(fields.Nested(CategorySchema))


class TaskCreateResponseSchema(Schema):
    task = fields.Nested(TaskSchema)
    notification_queued = fields.Bool()


class MessageSchema(Schema):
    message = fields.Str()


class ErrorSchema(Schema):
    error = fields.Str()


class ValidationErrorSchema(Schema):
    errors = fields.Dict()