from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Estudiante(Base):
    __tablename__ = "estudiantes"

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

    semestre: Mapped[int | None] = mapped_column(
        nullable=True
    )