from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Docente(Base):
    __tablename__ = "docentes"

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        primary_key=True
    )

    num_empleado: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True
    )

    id_departamento: Mapped[int] = mapped_column(
        ForeignKey("departamentos.id_departamento"),
        nullable=False
    )