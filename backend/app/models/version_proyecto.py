
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VersionProyecto(Base):
    __tablename__ = "version_proyecto"

    __table_args__ = (
        UniqueConstraint(
            "id_proyecto",
            "numero_version",
            name="uq_version_proyecto_numero"
        ),
        CheckConstraint(
            "numero_version > 0",
            name="ck_version_numero_positivo"
        ),
        CheckConstraint(
            "tamano_bytes >= 0",
            name="ck_version_tamano_no_negativo"
        ),
    )

    id_version: Mapped[int] = mapped_column(
        primary_key=True
    )

    id_proyecto: Mapped[int] = mapped_column(
        ForeignKey("proyectos.id_proyecto", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    numero_version: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    ruta_pdf: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    tamano_bytes: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    fecha_subida: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
