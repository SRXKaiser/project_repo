
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class RecuperacionAcceso(Base):
    __tablename__ = "recuperacion_acceso"

    id_recuperacion: Mapped[int] = mapped_column(
        primary_key=True
    )

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    token_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        unique=True
    )

    fecha_expiracion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    usado: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false"
    )
