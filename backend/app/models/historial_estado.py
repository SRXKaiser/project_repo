from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import EstadoProyecto


class HistorialEstado(Base):
    __tablename__ = "historial_estados"

    id_historial: Mapped[int] = mapped_column(
        primary_key=True
    )

    id_proyecto: Mapped[int] = mapped_column(
        ForeignKey("proyectos.id_proyecto", ondelete="CASCADE"),
        nullable=False
    )

    estado_anterior: Mapped[EstadoProyecto | None] = mapped_column(
        Enum(
            EstadoProyecto,
            name="estado_proyecto_enum",
            create_type=False
        ),
        nullable=True
    )

    estado_nuevo: Mapped[EstadoProyecto] = mapped_column(
        Enum(
            EstadoProyecto,
            name="estado_proyecto_enum",
            create_type=False
        ),
        nullable=False
    )

    cambiado_por: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario"),
        nullable=False
    )

    fecha_cambio: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    comentario: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )