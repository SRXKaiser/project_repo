from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ProyectoArea(Base):
    __tablename__ = "proyectos_areas"

    id_proyecto: Mapped[int] = mapped_column(
        ForeignKey("proyectos.id_proyecto", ondelete="CASCADE"),
        primary_key=True
    )

    id_area: Mapped[int] = mapped_column(
        ForeignKey("areas_tematicas.id_area", ondelete="CASCADE"),
        primary_key=True
    )