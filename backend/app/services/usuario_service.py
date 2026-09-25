from datetime import date

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.enums import EstadoCuenta
from app.models.responsable_departamento import ResponsableDepartamento
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.usuario_rol import UsuarioRol


def buscar_usuarios(
    db: Session,
    buscar: str,
    limite: int = 10,
) -> list[Usuario]:

    termino_limpio = buscar.strip()

    if len(termino_limpio) < 2:
        return []

    termino = f"%{termino_limpio.lower()}%"

    consulta = (
        select(Usuario)
        .where(
            Usuario.estado_cuenta == EstadoCuenta.ACTIVA,
            or_(
                func.lower(Usuario.nombre).like(termino),
                func.lower(
                    Usuario.apellido_paterno
                ).like(termino),
                func.lower(Usuario.correo).like(termino),
            ),
        )
        .order_by(
            Usuario.apellido_paterno.asc(),
            Usuario.nombre.asc(),
        )
        .limit(limite)
    )

    return list(
        db.scalars(consulta).all()
    )


def usuario_es_administrador(
    db: Session,
    id_usuario: int,
) -> bool:

    id_rol = db.scalar(
        select(Rol.id_rol)
        .join(
            UsuarioRol,
            UsuarioRol.id_rol == Rol.id_rol,
        )
        .where(
            UsuarioRol.id_usuario == id_usuario,
            Rol.nombre == "ADMINISTRADOR",
        )
        .limit(1)
    )

    return id_rol is not None


def obtener_departamentos_responsable(
    db: Session,
    id_usuario: int,
) -> list[int]:

    hoy = date.today()

    consulta = (
        select(
            ResponsableDepartamento.id_departamento
        )
        .where(
            ResponsableDepartamento.id_usuario_docente
            == id_usuario,
            ResponsableDepartamento.activo.is_(True),
            ResponsableDepartamento.fecha_inicio <= hoy,
            (
                ResponsableDepartamento.fecha_fin.is_(None)
                | (
                    ResponsableDepartamento.fecha_fin
                    >= hoy
                )
            ),
        )
        .order_by(
            ResponsableDepartamento.id_departamento
        )
    )

    return list(
        db.scalars(consulta).all()
    )