from .base import Base, intpk, TimestampMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from ..utils.model_mixin import ModelMixin


class UserModel(TimestampMixin, ModelMixin, Base):
    __tablename__ = "user_account"
    id: Mapped[intpk] = mapped_column(init=False)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    fullname: Mapped[Optional[str]] = mapped_column(String(120))
    revoked_tokens: Mapped[list["RevokedTokenModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", init=False
    )
    passwords: Mapped[list["UserPasswordModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", init=False
    )
    likes: Mapped[list["LikeModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", init=False
    )
    account: Mapped["AccountModel"] = relationship(
        "AccountModel",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        init=False,
    )
    comments: Mapped[list["CommentModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", init=False
    )

    following: Mapped[list["FollowModel"]] = relationship(
        "FollowModel",
        foreign_keys="FollowModel.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan",
        init=False,
    )

    followers: Mapped[list["FollowModel"]] = relationship(
        "FollowModel",
        foreign_keys="FollowModel.followed_id",
        back_populates="followed",
        cascade="all, delete-orphan",
        init=False,
    )
    stories: Mapped[list["StoryModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", init=False
    )
