from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Archivo(Base):
    __tablename__ = "archivos"

    id_archivo: Mapped[int] = mapped_column(
        primary_key=True
    )

    id_proyecto: Mapped[int] = mapped_column(
        ForeignKey("proyectos.id_proyecto", ondelete="CASCADE"),
        nullable=False
    )

    nombre_original: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    nombre_almacenado: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    tipo_mime: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    tamanio: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    ruta_archivo: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    fecha_subida: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    subido_por: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario"),
        nullable=False
    )