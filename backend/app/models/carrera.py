from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Carrera(Base):
    __tablename__ = "carreras"

    id_carrera: Mapped[int] = mapped_column(
        primary_key=True
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    siglas: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    activa: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    id_departamento: Mapped[int] = mapped_column(
        ForeignKey("departamentos.id_departamento"),
        nullable=False
    )