
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EstudiantePerfil(Base):
    __tablename__ = "estudiante_perfil"

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("estudiantes.id_usuario", ondelete="CASCADE"),
        primary_key=True
    )

    generacion: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    habilidad: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    intereses: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    imagen_perfil: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
