from marshmallow import fields, validate, Schema

username_pattern = r"^(?=.{3,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"
email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"


class UserRegistrationSchema(Schema):
    username = fields.Str(
        required=True,
        error_messages={
            "required": "Username is required.",
            "null": "Username cannot be null!",
        },
        validate=validate.Regexp(
            username_pattern,
            error="Username must be 3-20 characters long, can include letters, numbers, underscores, and periods, but cannot start or end with an underscore or period, nor have consecutive underscores or periods.",
        ),
    )
    email = fields.Str(
        required=True,
        error_messages={
            "required": "Email is required.",
            "null": "Email cannot be null!",
        },
        validate=validate.Regexp(
            email_pattern,
            error="Invalid email format.",
        ),
    )
    fullname = fields.Str(
        allow_none=True, error_messages={"null": "Username cannot be null!"}
    )
    password = fields.Str(
        required=True,
        error_messages={
            "required": "Password is required.",
            "null": "Username cannot be null!",
        },
        validate=validate.Regexp(
            password_pattern,
            error="Password must be at least 8 characters long and include at least one letter and one number.",
        ),
        load_only=True,
    )


class UserLoginSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email is required.",
            "null": "Username cannot be null!",
        },
        validate=validate.Regexp(
            email_pattern,
            error="Invalid email format.",
        ),
    )
    password = fields.Str(
        required=True,
        error_messages={
            "required": "Password is required.",
            "null": "Username cannot be null!",
        },
        validate=validate.Regexp(
            password_pattern,
            error="Password must be at least 8 characters long and include at least one letter and one number.",
        ),
    )
