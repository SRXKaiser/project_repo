from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.enums import EstadoCuenta
from app.models.usuario import Usuario

bearer_scheme = HTTPBearer()
from collections.abc import Callable
from app.models.enums import TipoUsuario
from sqlalchemy import select
from app.models.rol import Rol
from app.models.usuario_rol import UsuarioRol

from app.models.docente import Docente
from app.models.responsable_departamento import ResponsableDepartamento

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Usuario:

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        subject = payload.get("sub")

        if subject is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )

        try:
            id_usuario = int(subject)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado",
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )

    usuario = db.get(Usuario, id_usuario)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El usuario del token no existe",
        )

    if usuario.estado_cuenta != EstadoCuenta.ACTIVA:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta no está activa",
        )

    return usuario

def require_user_types(
    *tipos_permitidos: TipoUsuario,
) -> Callable:

    def dependency(
        usuario: Usuario = Depends(get_current_user),
    ) -> Usuario:

        if usuario.tipo_usuario not in tipos_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción",
            )

        return usuario

    return dependency

def es_administrador(
    db: Session,
    usuario: Usuario,
) -> bool:

    resultado = db.scalar(
        select(UsuarioRol)
        .join(
            Rol,
            UsuarioRol.id_rol == Rol.id_rol
        )
        .where(
            UsuarioRol.id_usuario == usuario.id_usuario,
            Rol.nombre == "ADMINISTRADOR",
        )
    )

    return resultado is not None

def require_admin(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Usuario:

    if not es_administrador(db, usuario):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador",
        )

    return usuario

def es_jefe_departamento(
    db: Session,
    usuario: Usuario,
    id_departamento: int,
) -> bool:

    if usuario.tipo_usuario != TipoUsuario.DOCENTE:
        return False

    docente = db.get(
        Docente,
        usuario.id_usuario
    )

    if docente is None:
        return False

    responsable = db.scalar(
        select(ResponsableDepartamento).where(
            ResponsableDepartamento.id_usuario_docente
            == usuario.id_usuario,

            ResponsableDepartamento.id_departamento
            == id_departamento,

            ResponsableDepartamento.activo.is_(True),
        )
    )

    return responsable is not None