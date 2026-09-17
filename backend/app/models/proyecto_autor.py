from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import TipoParticipacion


class ProyectoAutor(Base):
    __tablename__ = "proyectos_autores"

    id_proyecto: Mapped[int] = mapped_column(
        ForeignKey("proyectos.id_proyecto", ondelete="CASCADE"),
        primary_key=True
    )

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario"),
        primary_key=True
    )

    tipo_participacion: Mapped[TipoParticipacion] = mapped_column(
        Enum(TipoParticipacion, name="tipo_participacion_enum"),
        nullable=False,
        default=TipoParticipacion.AUTOR
    )

    orden_autoria: Mapped[int | None] = mapped_column(
        nullable=True
    )