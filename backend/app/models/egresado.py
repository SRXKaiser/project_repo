from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Egresado(Base):
    __tablename__ = "egresados"

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        primary_key=True
    )

    num_control: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    id_carrera: Mapped[int] = mapped_column(
        ForeignKey("carreras.id_carrera"),
        nullable=False
    )

    anio_egreso: Mapped[int] = mapped_column(
        nullable=False
    )