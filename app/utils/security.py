from ..extensions import bcrypt


def generate_password_hash(password: str) -> str:
    return bcrypt.generate_password_hash(password, rounds=14).decode("utf-8")
