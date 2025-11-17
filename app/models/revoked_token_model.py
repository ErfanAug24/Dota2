from .base import Base, TimestampMixin, intpk, user_fk
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..utils.model_mixin import ModelMixin


class RevokedTokenModel(TimestampMixin, ModelMixin, Base):
    __tablename__ = "revoked_token"
    id: Mapped[intpk] = mapped_column(init=False)
    jti: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    ttype: Mapped[str] = mapped_column(String(30), nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=True)
    user_id: Mapped[user_fk]
    user: Mapped["UserModel"] = relationship(back_populates="revoked_tokens")
