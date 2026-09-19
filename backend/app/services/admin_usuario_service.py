from fastapi import HTTPException, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.enums import EstadoCuenta, TipoUsuario
from app.models.usuario import Usuario


def listar_usuarios(
    db: Session,
    buscar: str | None = None,
    tipo_usuario: TipoUsuario | None = None,
    estado_cuenta: EstadoCuenta | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[Usuario]:

    consulta = select(Usuario)

    if buscar:
        termino = f"%{buscar.strip().lower()}%"

        consulta = consulta.where(
            or_(
                func.lower(Usuario.nombre).like(termino),
                func.lower(Usuario.apellido_paterno).like(termino),
                func.lower(Usuario.correo).like(termino),
            )
        )

    if tipo_usuario is not None:
        consulta = consulta.where(
            Usuario.tipo_usuario == tipo_usuario
        )

    if estado_cuenta is not None:
        consulta = consulta.where(
            Usuario.estado_cuenta == estado_cuenta
        )

    consulta = (
        consulta
        .order_by(
            Usuario.fecha_registro.desc()
        )
        .offset(skip)
        .limit(limit)
    )

    return list(
        db.scalars(consulta).all()
    )


def obtener_usuario_admin(
    db: Session,
    id_usuario: int,
) -> Usuario:

    usuario = db.get(
        Usuario,
        id_usuario,
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return usuario


def cambiar_estado_cuenta(
    db: Session,
    id_usuario: int,
    nuevo_estado: EstadoCuenta,
    administrador: Usuario,
) -> Usuario:

    usuario = obtener_usuario_admin(
        db=db,
        id_usuario=id_usuario,
    )

    if usuario.id_usuario == administrador.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No puedes cambiar el estado "
                "de tu propia cuenta"
            ),
        )

    if usuario.estado_cuenta == nuevo_estado:
        return usuario

    try:
        usuario.estado_cuenta = nuevo_estado

        db.commit()
        db.refresh(usuario)

        return usuario

    except Exception:
        db.rollback()
        raise