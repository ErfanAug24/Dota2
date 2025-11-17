from app.extensions import ma
from marshmallow import fields
from app.models.comment import CommentModel


class CommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CommentModel
        load_instance = True  # Auto-convert to CommentModel
        include_fk = True  # Include foreign keys in load/dump

    id = fields.Integer(dump_only=True)
    content = fields.String(allow_none=True)
    user_id = fields.Integer(required=True)

    # Relationships — shallow by default
    user = fields.Nested("UserSchema", dump_only=True)
    story_id = fields.Integer(allow_none=True)
    story = fields.Nested("StorySchema", dump_only=True)
    parent_id = fields.Integer(allow_none=True)
    parent = fields.Nested("self", allow_none=True, dump_only=True)
    children = fields.List(fields.Nested("self"), dump_only=True)
    likes = fields.List(fields.Nested("LikeSchema"), dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    