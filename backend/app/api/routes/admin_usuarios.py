from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.db.database import get_db
from app.models.enums import EstadoCuenta, TipoUsuario
from app.models.usuario import Usuario
from app.schemas.admin_usuario import (
    CambiarEstadoCuentaRequest,
    UsuarioAdminResponse,
)
from app.services.admin_usuario_service import (
    cambiar_estado_cuenta,
    listar_usuarios,
    obtener_usuario_admin,
)


router = APIRouter(
    prefix="/admin/usuarios",
    tags=["Administración - Usuarios"],
)


@router.get(
    "",
    response_model=list[UsuarioAdminResponse],
)
def listar(
    buscar: str | None = None,
    tipo_usuario: TipoUsuario | None = None,
    estado_cuenta: EstadoCuenta | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    administrador: Usuario = Depends(require_admin),
):
    return listar_usuarios(
        db=db,
        buscar=buscar,
        tipo_usuario=tipo_usuario,
        estado_cuenta=estado_cuenta,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{id_usuario}",
    response_model=UsuarioAdminResponse,
)
def obtener(
    id_usuario: int,
    db: Session = Depends(get_db),
    administrador: Usuario = Depends(require_admin),
):
    return obtener_usuario_admin(
        db=db,
        id_usuario=id_usuario,
    )


@router.patch(
    "/{id_usuario}/estado",
    response_model=UsuarioAdminResponse,
)
def cambiar_estado(
    id_usuario: int,
    datos: CambiarEstadoCuentaRequest,
    db: Session = Depends(get_db),
    administrador: Usuario = Depends(require_admin),
):
    return cambiar_estado_cuenta(
        db=db,
        id_usuario=id_usuario,
        nuevo_estado=datos.estado_cuenta,
        administrador=administrador,
    )