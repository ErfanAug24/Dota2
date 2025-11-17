from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin, intpk, user_fk
from typing import Optional
from .associations import favorite_stories_table
from ..utils.model_mixin import ModelMixin


class StoryModel(TimestampMixin, ModelMixin, Base):
    __tablename__ = "story"
    id: Mapped[intpk] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    content: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_id: Mapped[user_fk]
    user: Mapped["UserModel"] = relationship(back_populates="stories")
    comments: Mapped[list["CommentModel"]] = relationship(
        back_populates="story", init=False
    )
    likes: Mapped[list["LikeModel"]] = relationship(back_populates="story", init=False)
    favorited_by_profiles: Mapped[list["ProfileModel"]] = relationship(
        secondary=favorite_stories_table, back_populates="favorite_stories", init=False
    )
