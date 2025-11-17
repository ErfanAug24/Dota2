from app.extensions import ma
from marshmallow import fields
from app.models.follow import FollowModel

class FollowSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FollowModel
        load_instance = True  # Auto-convert to FollowModel
        include_fk = True  # Include foreign keys in load/dump

    id = fields.Integer(dump_only=True)
    follower_id = fields.Integer(required=True)
    followed_id = fields.Integer(required=True)

    # Relationships — shallow by default
    follower = fields.Nested("UserSchema", dump_only=True)
    followed = fields.Nested("UserSchema", dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    