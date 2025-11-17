from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin, intpk, user_fk
from typing import Optional
from datetime import datetime
from ..utils.statics import CountryEnum, LanguageEnum
from ..utils.model_mixin import ModelMixin


class AccountModel(TimestampMixin, ModelMixin, Base):
    __tablename__ = "account"
    id: Mapped[intpk] = mapped_column(init=False)
    bio: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(Enum(CountryEnum), nullable=True)
    custom_url: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True, unique=True
    )
    phonenumber: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    real_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    user_id: Mapped[user_fk]
    user: Mapped["UserModel"] = relationship(back_populates="account")
    avatar_id: Mapped[int] = mapped_column(ForeignKey("media.id"), nullable=True)
    avatar: Mapped[Optional["MediaModel"]] = relationship("MediaModel")

    profile: Mapped["ProfileModel"] = relationship(
        back_populates="account", uselist=False
    )
    language: Mapped[Optional[str]] = mapped_column(
        Enum(LanguageEnum), default=LanguageEnum.ENGLISH, nullable=False
    )
    birth_date: Mapped[Optional[datetime]] = mapped_column(default=None, nullable=True)
