
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ResumenGenerado(Base):
    __tablename__ = "resumen_generado"

    id_resumen: Mapped[int] = mapped_column(
        primary_key=True
    )

    id_proyecto: Mapped[int] = mapped_column(
        ForeignKey("proyectos.id_proyecto", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    id_version: Mapped[int | None] = mapped_column(
        ForeignKey("version_proyecto.id_version", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    contenido: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    correo_destino: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    fecha_generacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    estado_envio: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="PENDIENTE",
        server_default="PENDIENTE"
    )
