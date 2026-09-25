from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import (
    UsuarioBusquedaResponse,
    UsuarioContextoResponse,
    UsuarioResponse,
)
from app.services.usuario_service import (
    buscar_usuarios,
    obtener_departamentos_responsable,
    usuario_es_administrador,
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)


@router.get(
    "/me",
    response_model=UsuarioContextoResponse,
)
def obtener_mi_usuario(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return UsuarioContextoResponse(
        id_usuario=usuario.id_usuario,
        nombre=usuario.nombre,
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
        correo=usuario.correo,
        tipo_usuario=usuario.tipo_usuario,
        estado_cuenta=usuario.estado_cuenta,
        fecha_registro=usuario.fecha_registro,
        ultimo_acceso=usuario.ultimo_acceso,
        es_administrador=usuario_es_administrador(
            db=db,
            id_usuario=usuario.id_usuario,
        ),
        departamentos_responsable=(
            obtener_departamentos_responsable(
                db=db,
                id_usuario=usuario.id_usuario,
            )
        ),
    )


@router.get(
    "/buscar",
    response_model=list[UsuarioBusquedaResponse],
)
def buscar(
    q: str = Query(
        ...,
        min_length=2,
        max_length=150,
    ),
    limite: int = Query(
        default=10,
        ge=1,
        le=20,
    ),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return buscar_usuarios(
        db=db,
        buscar=q,
        limite=limite,
    )