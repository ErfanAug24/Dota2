from .base import Base, intpk, user_fk, TimestampMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..utils.model_mixin import ModelMixin


class UserPasswordModel(TimestampMixin, ModelMixin, Base):
    __tablename__ = "user_password"
    id: Mapped[intpk] = mapped_column(init=False)
    user_id: Mapped[user_fk]
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="passwords"
    )
