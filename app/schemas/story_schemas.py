from app.extensions import ma
from marshmallow import fields, validate
from app.models import StoryModel


class StorySchema(ma.SQLAlchemySchema):
    class Meta:
        model = StoryModel
        load_instance = True  # Auto-convert to StoryModel
        include_fk = True  # Include user_id in load/dump

    id = fields.Integer(dump_only=True)
    title = fields.String(
        required=True,
        validate=validate.Length(min=3, max=255),
        error_messages={"required": "Title is required."},
    )
    slug = fields.String(dump_only=True)  # Usually auto-generated from title
    content = fields.String(allow_none=True)

    user_id = fields.Integer(required=True)

    # Relationships — shallow by default
    comments = fields.Nested("CommentSchema", many=True, dump_only=True)
    likes = fields.Nested("LikeSchema", many=True, dump_only=True)
    favorited_by_profiles = fields.Nested(
        "ProfileSchema", many=True, dump_only=True, exclude=("favorite_stories",)
    )


class CreateStorySchema(ma.Schema):
    title = fields.String(required=True, validate=validate.Length(min=3, max=255))
    content = fields.String(allow_none=True)
    user_id = fields.Integer(required=True)
