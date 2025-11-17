from sqlalchemy import MetaData, String, Table, Column
from sqlalchemy import ForeignKey
from .base import Base

favorite_heroes_table = Table(
    "favorite_heroes",
    Base.metadata,
    Column("profile_id", ForeignKey("profile.id"), primary_key=True),
    Column("hero_id", ForeignKey("hero.id"), primary_key=True),
)

favorite_stories_table = Table(
    "favorite_stories",
    Base.metadata,
    Column("profile_id", ForeignKey("profile.id"), primary_key=True),
    Column("story_id", ForeignKey("story.id"), primary_key=True),
)

hero_connections_table = Table(
    "hero_connections",
    Base.metadata,
    Column("hero_id", ForeignKey("hero.id"), primary_key=True),
    Column("connected_hero_id", ForeignKey("hero.id"), primary_key=True),
)