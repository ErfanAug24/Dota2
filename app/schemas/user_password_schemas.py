from marshmallow import (
    Schema,
    fields,
    validates,
    validates_schema,
    ValidationError,
    validate,
)
from ..extensions import ma
import re


def validate_password(password: str):
    """Common password validator."""
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Za-z]", password):
        raise ValidationError("Password must include at least one letter.")
    if not re.search(r"\d", password):
        raise ValidationError("Password must include at least one number.")
    return password


class UserPasswordSchema(ma.SQLAlchemySchema):
    class Meta:
        load_instance = True  # Allow deserialization into UserPasswordModel

    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    password_hash = fields.String(required=True, validate=validate.Length(min=8))
    user = fields.Nested("UserSchema", dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ChangePasswordSchema(Schema):
    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate_password)

    @validates_schema
    def validate_not_same(self, data, **kwargs):
        if data.get("current_password") == data.get("new_password"):
            raise ValidationError(
                {
                    "new_password": [
                        "New password cannot be the same as the current password."
                    ]
                }
            )
