from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin, intpk, user_fk
from typing import Optional
from ..utils.model_mixin import ModelMixin


class CommentModel(TimestampMixin, ModelMixin, Base):
    __tablename__ = "comment"
    id: Mapped[intpk] = mapped_column(init=False)
    content: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    user_id: Mapped[user_fk]
    user: Mapped["UserModel"] = relationship(back_populates="comments")
    story_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("story.id"), nullable=True
    )
    story: Mapped[Optional["StoryModel"]] = relationship(back_populates="comments")
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("comment.id"), nullable=True
    )

    parent: Mapped[Optional["CommentModel"]] = relationship(
        "CommentModel",
        remote_side=[id],
        back_populates="children",
        uselist=False,
    )
    children: Mapped[list["CommentModel"]] = relationship(
        "CommentModel",
        back_populates="parent",
        cascade="all, delete-orphan",
        uselist=True,
        init=False,
    )
    likes: Mapped[list["LikeModel"]] = relationship(
        back_populates="comment", init=False
    )
