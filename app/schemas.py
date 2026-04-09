from marshmallow import Schema, fields, validate


class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    color = fields.Str(validate=validate.Regexp(r"^#(?:[0-9a-fA-F]{6})$"))

class PlainTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(validate=validate.Length(max=500))
    completed = fields.Bool(dump_only=True)

class TaskSchema(PlainTaskSchema):
    category_id = fields.Int(load_only=True)
    category = fields.Nested(PlainCategorySchema(), dump_only=True)

class CategorySchema(PlainCategorySchema):
    tasks = fields.List(fields.Nested(PlainTaskSchema()), dump_only=True)