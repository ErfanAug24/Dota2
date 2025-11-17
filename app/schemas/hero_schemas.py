from app.extensions import ma
from marshmallow import fields
from app.models.hero import HeroModel


class HeroSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HeroModel
        load_instance = True  # Auto-convert to HeroModel
        include_fk = True  # Include foreign keys in load/dump

    id = fields.Integer(dump_only=True)
    localized_name = fields.String(required=True)
    primary_attr = fields.String(allow_none=True)
    attack_type = fields.String(allow_none=True)
    roles = fields.List(fields.String(), allow_none=True)
    favorited_by_profiles = fields.List(fields.Nested("ProfileSchema"), dump_only=True)

    # Relationships — shallow by default
    connections = fields.List(fields.Nested("self"), dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
