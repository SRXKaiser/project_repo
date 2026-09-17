from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ResponsableDepartamento(Base):
    __tablename__ = "responsables_departamento"

    id_responsable: Mapped[int] = mapped_column(
        primary_key=True
    )

    id_departamento: Mapped[int] = mapped_column(
        ForeignKey("departamentos.id_departamento"),
        nullable=False
    )

    id_usuario_docente: Mapped[int] = mapped_column(
        ForeignKey("docentes.id_usuario"),
        nullable=False
    )

    fecha_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    fecha_fin: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )