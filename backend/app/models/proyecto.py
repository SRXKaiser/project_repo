from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import EstadoProyecto


class Proyecto(Base):
    __tablename__ = "proyectos"

    id_proyecto: Mapped[int] = mapped_column(
        primary_key=True
    )

    titulo: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        index=True
    )

    resumen: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    fecha_publicacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    estado: Mapped[EstadoProyecto] = mapped_column(
        Enum(EstadoProyecto, name="estado_proyecto_enum"),
        nullable=False,
        default=EstadoProyecto.BORRADOR
    )

    id_departamento: Mapped[int] = mapped_column(
        ForeignKey("departamentos.id_departamento"),
        nullable=False
    )

    creado_por: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario"),
        nullable=False
    )