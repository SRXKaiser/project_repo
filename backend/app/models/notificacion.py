
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Notificacion(Base):
    __tablename__ = "notificacion"

    id_notificacion: Mapped[int] = mapped_column(
        primary_key=True
    )

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    id_proyecto: Mapped[int | None] = mapped_column(
        ForeignKey("proyectos.id_proyecto", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    tipo: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )

    mensaje: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    fecha_envio: Mapped[datetime] = mapped_column(
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
