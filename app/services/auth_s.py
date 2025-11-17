from ..extensions import bcrypt, redis_client
from ..models import UserModel, UserPasswordModel, RevokedTokenModel
from ..schemas import ChangePasswordSchema, UserRegistrationSchema, UserLoginSchema
from ..tasks.email_tasks import send_email
from ..utils.security import generate_password_hash
from ..utils.common_funcs import UserInput
import uuid
from typing import Dict, Any


class UserAuthentication:

    def sign_up(
        self, username: str, email: str, password: str, fullname: str = None
    ) -> UserModel:
        data = {
            "username": username,
            "email": email,
            "password": password,
            "fullname": fullname,
        }
        errors = UserInput(
            UserRegistrationSchema,
            data,
        ).validate()
        data.pop("password")
        if errors:
            raise ValueError(errors)
        self._check_singularity(data)
        hash_password = generate_password_hash(password)
        user = UserModel.create(**data)
        UserPasswordModel.create(
            user_id=user.id, hashed_password=hash_password, user=user
        )
        send_email(
            to_email=email,
            body="Welcome to Lorehub!",
            from_email="ershirkhanei261384@gmail.com",
        )
        return user

    def sign_in(self, email: str, password: str) -> UserModel:
        errors = UserInput(
            UserLoginSchema, data={"email": email, "password": password}
        ).validate()
        if errors:
            raise ValueError(errors)
        user = self._check_existence(email=email)
        if self._verify_password(user, password):
            return user
        raise ValueError("Wrong password.")

    @staticmethod
    def sign_out(jti: str, user_id: int) -> RevokedTokenModel:
        user = UserModel.get(user_id)
        existing = RevokedTokenModel.filter_by(jti=jti, user_id=user_id).one_or_none()
        if existing:
            return existing
        return RevokedTokenModel.create(
            jti=jti, ttype="access", reason="logout", user_id=user_id, user=user
        )

    # Bug : it can raise only one error per call
    def _check_singularity(self, data: Dict[str, Any]):
        errors = {}
        for key, value in data.items():
            if self._exists(**{key: value}):
                errors[key] = f"{key} '{value}' already exists."
        if errors:
            raise ValueError(errors)

    @staticmethod
    def _exists(**kwargs) -> bool:
        return UserModel.filter_by(**kwargs).one_or_none() is not None

    @staticmethod
    def _check_existence(**kwargs):
        user = UserModel.filter_by(**kwargs).one_or_none()
        if user is None:
            raise LookupError(
                "No user found with " + ", ".join(f"{k}={v}" for k, v in kwargs.items())
            )
        return user

    @staticmethod
    def _verify_password(user: UserModel, password: str) -> bool:
        """Check if the given password matches the user’s current password."""
        current_hash = UserPasswordService.get_last_user_password(user.id)
        return bcrypt.check_password_hash(current_hash, password)

    @staticmethod
    def _is_password_reused(user_id: int, new_password: str, limit: int = 3) -> bool:
        recent_passwords = (
            UserPasswordModel.filter_by(user_id=user_id)
            .order_by(UserPasswordModel.created.desc())
            .limit(limit)
            .all()
        )
        for old_pass in recent_passwords:
            if bcrypt.check_password_hash(old_pass.hashed_password, new_password):
                return True  # reused
        return False


class UserPasswordService(UserAuthentication):
    def initiate_password_reset(self, email: str) -> str:
        user = self._check_existence(**{"email": email})
        reset_token = str(uuid.uuid4().hex)
        redis_client.setex(f"password_reset_{user.email}", 900, reset_token)
        send_email(
            subject="Lorehub Password Reset",
            body=f"Your password reset token is: {reset_token}",
            to_email=user.email,
            from_email="ershirkhanei261384@gmail.com",
        )
        return reset_token

    def reset_password(
        self, email: str, token: str, new_password: str
    ) -> UserPasswordModel:
        user = self._check_existence(**{"email": email})
        if not self.validate_reset_token(email, token):
            raise ValueError("Invalid or expired reset token.")
        if self._is_password_reused(user.id, new_password):
            raise ValueError("New password cannot be the same with the last password.")
        redis_client.delete(f"password_reset_{email}")
        new_password_hash = generate_password_hash(new_password)
        return UserPasswordModel.create(
            user_id=user.id,
            user=user,
            hashed_password=new_password_hash,
        )

    def change_password(
        self, email: str, current_password: str, new_password: str
    ) -> UserPasswordModel:
        data = {
            "current_password": current_password,
            "new_password": new_password,
        }
        errors = UserInput(ChangePasswordSchema, data).validate()
        if errors:
            raise ValueError(errors)
        user = self._check_existence(**{"email": email})
        if not self._verify_password(user, current_password):
            raise ValueError("Wrong password.")
        if self._is_password_reused(user.id, new_password):
            raise ValueError("New password cannot be the same with the last password.")
        new_password_hash = generate_password_hash(new_password)
        return UserPasswordModel.create(
            user_id=user.id,
            user=user,
            hashed_password=new_password_hash,
        )

    @staticmethod
    def validate_reset_token(email: str, token: str) -> bool:
        redis_key = f"password_reset_{email}"
        stored_token = redis_client.get(redis_key)
        if stored_token and stored_token == token:
            return True
        return False

    @staticmethod
    def get_last_user_password(user_id: int) -> str:
        record = (
            UserPasswordModel.filter_by(user_id=user_id)
            .order_by(UserPasswordModel.created.desc())
            .first()
        )
        if not record:
            raise LookupError(f"No password found for user_id={user_id}")
        return record.hashed_password
