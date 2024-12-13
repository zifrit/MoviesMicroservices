from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer
from src.models.base import IdCUDMixin, Base



class Movie(IdCUDMixin):
    __tablename__ = 'movies'

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(Integer)
