from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy import MetaData, String, Column
from typing_extensions import Annotated
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


intpk = Annotated[int, mapped_column(primary_key=True)]
str30 = Annotated[str, mapped_column(String(30))]
user_fk = Annotated[int, mapped_column(ForeignKey("user_account.id"))]


class TimestampMixin(MappedAsDataclass):
    __abstract__ = True
    created: Mapped[datetime] = mapped_column(
        default_factory=lambda: datetime.now(timezone.utc), init=False
    )
    updated: Mapped[datetime] = mapped_column(
        default_factory=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        init=False,
    )


class Base(DeclarativeBase, MappedAsDataclass):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
