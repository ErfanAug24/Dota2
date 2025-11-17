from marshmallow import fields
from ..extensions import ma


class LikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True  # Auto-convert to LikeModel
        include_fk = True  # Include foreign keys in load/dump

    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    comment_id = fields.Integer(required=True)

    # Relationships — shallow by default
    user = fields.Nested("UserSchema", dump_only=True)
    comment = fields.Nested("CommentSchema", dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
