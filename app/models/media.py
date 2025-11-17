from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, TimestampMixin, intpk
from typing import Optional
from ..utils.model_mixin import ModelMixin


class MediaModel(TimestampMixin, ModelMixin, Base):
    __tablename__ = "media"
    id: Mapped[intpk] = mapped_column(init=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)
    resolution: Mapped[str] = mapped_column(String, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    file_size_kb: Mapped[float] = mapped_column(Float, nullable=False)
    mode: Mapped[str] = mapped_column(String, nullable=False)
