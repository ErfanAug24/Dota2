from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampMixin, intpk, user_fk
from ..utils.model_mixin import ModelMixin


class FollowModel(TimestampMixin, ModelMixin, Base):
    __tablename__ = "follow"
    id: Mapped[intpk] = mapped_column(init=False)
    follower_id: Mapped[user_fk] = mapped_column(
        ForeignKey("user_account.id"), nullable=False
    )
    follower: Mapped["UserModel"] = relationship(
        back_populates="following", foreign_keys=[follower_id]
    )
    followed_id: Mapped[user_fk] = mapped_column(
        ForeignKey("user_account.id"), nullable=False
    )
    followed: Mapped["UserModel"] = relationship(
        back_populates="followers", foreign_keys=[followed_id]
    )
    __table_args__ = (
        # Ensure a user cannot follow the same user more than once
        UniqueConstraint("follower_id", "followed_id", name="unique_follow"),
    )

    def __repr__(self):
        return (
            f"<Follow(follower_id={self.follower_id}, followed_id={self.followed_id})>"
        )
