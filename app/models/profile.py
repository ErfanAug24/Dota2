from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..utils.model_mixin import ModelMixin
from .base import Base, TimestampMixin, intpk
from .associations import favorite_heroes_table


class ProfileModel(TimestampMixin, ModelMixin, Base):
    __tablename__ = "profile"
    id: Mapped[intpk] = mapped_column(init=False)
    account_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("account.id"), unique=True
    )
    # Favorite heroes and stories
    favorite_heroes: Mapped[list["HeroModel"]] = relationship(
        secondary=favorite_heroes_table, back_populates="favorited_by_profiles"
    )
    favorite_stories: Mapped[list["StoryModel"]] = relationship(
        secondary="favorite_stories", back_populates="favorited_by_profiles"
    )

    # Profile information
    account: Mapped["AccountModel"] = relationship(back_populates="profile")

