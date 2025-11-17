from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin, intpk, user_fk
from typing import Optional
from ..utils.model_mixin import ModelMixin


class LikeModel(TimestampMixin, ModelMixin, Base):
    __tablename__ = "like"
    id: Mapped[intpk] = mapped_column(init=False)
    user_id: Mapped[user_fk]
    user: Mapped["UserModel"] = relationship(back_populates="likes")
    story_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("story.id"), nullable=True
    )
    story: Mapped[Optional["StoryModel"]] = relationship(back_populates="likes")
    comment_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("comment.id"), nullable=True
    )
    comment: Mapped[Optional["CommentModel"]] = relationship(back_populates="likes")
