from marshmallow import Schema, fields, validate
from ..extensions import ma

class ProfileSchema(ma.SQLAlchemySchema):
    class Meta:
        load_instance = True  # Allow deserialization into ProfileModel

    id = fields.Integer(dump_only=True)
    account_id = fields.Integer(required=True)
    favorite_heroes = fields.List(fields.Nested("HeroSchema"), dump_only=True)
    favorite_stories = fields.List(fields.Nested("StorySchema"), dump_only=True)
    followers = fields.List(fields.Nested("FollowSchema"), dump_only=True)
    following = fields.List(fields.Nested("FollowSchema"), dump_only=True)
    account = fields.Nested("AccountSchema", dump_only=True)
    stories = fields.List(fields.Nested("StorySchema"), dump_only=True)
    comments = fields.List(fields.Nested("CommentSchema"), dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)