from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import EstadoCuenta, TipoUsuario


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(
        primary_key=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    apellido_paterno: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    apellido_materno: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    correo: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    tipo_usuario: Mapped[TipoUsuario] = mapped_column(
        Enum(TipoUsuario, name="tipo_usuario_enum"),
        nullable=False
    )

    estado_cuenta: Mapped[EstadoCuenta] = mapped_column(
        Enum(EstadoCuenta, name="estado_cuenta_enum"),
        nullable=False,
        default=EstadoCuenta.ACTIVA
    )

    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    ultimo_acceso: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )