from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UsuarioRol(Base):
    __tablename__ = "usuarios_roles"

    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario", ondelete="CASCADE"),
        primary_key=True
    )

    id_rol: Mapped[int] = mapped_column(
        ForeignKey("roles.id_rol", ondelete="CASCADE"),
        primary_key=True
    )