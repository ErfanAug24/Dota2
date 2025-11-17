from .base import Base, TimestampMixin, intpk
from .associations import favorite_heroes_table, hero_connections_table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import JSON
from ..utils.model_mixin import ModelMixin
from sqlalchemy import Enum as SqlEnum
from ..utils.statics import Dota2HeroAttributes, Dota2HeroFactions


class HeroModel(TimestampMixin, ModelMixin, Base):
    __tablename__ = "hero"

    id: Mapped[intpk] = mapped_column(init=False)

    localized_name: Mapped[str] = mapped_column(String(100))  # e.g. "Anti-Mage"

    primary_attr: Mapped[Dota2HeroAttributes] = mapped_column(
        SqlEnum(Dota2HeroAttributes, name="dota2_hero_attributes_enum"),
        nullable=False,
    )

    faction: Mapped[Dota2HeroFactions] = mapped_column(
        SqlEnum(Dota2HeroFactions, name="dota2_hero_factions_enum"), nullable=False
    )

    attack_type: Mapped[str] = mapped_column(String(10))  # "Melee" or "Ranged"

    roles: Mapped[list[str]] = mapped_column(MutableList.as_mutable(JSON))

    connections: Mapped[list["HeroModel"]] = relationship(
        "HeroModel",
        secondary=hero_connections_table,
        primaryjoin=id == hero_connections_table.c.hero_id,
        secondaryjoin=id == hero_connections_table.c.connected_hero_id,
        backref="connected_to",
    )

    favorited_by_profiles: Mapped[list["ProfileModel"]] = relationship(
        "ProfileModel",
        secondary=favorite_heroes_table,
        back_populates="favorite_heroes",
    )
