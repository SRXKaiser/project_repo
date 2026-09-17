from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ProyectoPalabraClave(Base):
    __tablename__ = "proyectos_palabras_clave"

    id_proyecto: Mapped[int] = mapped_column(
        ForeignKey("proyectos.id_proyecto", ondelete="CASCADE"),
        primary_key=True
    )

    id_palabra_clave: Mapped[int] = mapped_column(
        ForeignKey(
            "palabras_clave.id_palabra_clave",
            ondelete="CASCADE"
        ),
        primary_key=True
    )