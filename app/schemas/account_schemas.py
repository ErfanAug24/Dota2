from marshmallow import fields, validate
from ..extensions import ma
from marshmallow_enum import EnumField
from ..models.account import AccountModel
from ..utils.statics import CountryEnum, LanguageEnum


class AccountSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AccountModel
        load_instance = True  # Allow deserialization into AccountModel

    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    avatar_id = fields.Integer(allow_none=True)

    # Text fields
    bio = fields.String(allow_none=True, validate=validate.Length(max=500))
    real_name = fields.String(allow_none=True, validate=validate.Length(max=100))
    custom_url = fields.String(allow_none=True, validate=validate.Length(max=100))
    phonenumber = fields.String(allow_none=True, validate=validate.Length(max=20))

    # Enum fields
    country = EnumField(CountryEnum, by_value=True, allow_none=True)
    language = EnumField(LanguageEnum, by_value=True, required=True)

    # Date field
    birth_date = fields.Date(allow_none=True)
