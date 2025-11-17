from marshmallow import fields
from ..extensions import ma


class MediaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True  # Auto-convert to MediaModel
        include_fk = True  # Include foreign keys in load/dump

    id = fields.Integer(dump_only=True)
    file_type = fields.String(required=True)
    file_path = fields.String(required=True)
    resolution = fields.String(allow_none=True)
    width = fields.Integer(allow_none=True)
    height = fields.Integer(allow_none=True)
    file_size_kb = fields.Integer(allow_none=True)
    mode = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
