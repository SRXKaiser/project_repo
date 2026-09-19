from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.proyecto import ProyectoResponse
from app.schemas.workflow import (
    CambioEstadoRequest,
    HistorialEstadoResponse,
)
from app.services.workflow_service import (
    aprobar_proyecto,
    enviar_a_revision,
    listar_historial,
    listar_pendientes_revision,
    publicar_proyecto,
    rechazar_proyecto,
    regresar_a_borrador,
    solicitar_cambios,
)


router = APIRouter(
    prefix="/proyectos",
    tags=["Workflow de proyectos"],
)

@router.get(
    "/revision/pendientes",
    response_model=list[ProyectoResponse],
)
def pendientes_revision(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return listar_pendientes_revision(
        db=db,
        usuario=usuario,
    )


@router.post(
    "/{id_proyecto}/aprobar",
    response_model=ProyectoResponse,
)
def aprobar(
    id_proyecto: int,
    datos: CambioEstadoRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return aprobar_proyecto(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
        comentario=datos.comentario,
    )


@router.post(
    "/{id_proyecto}/solicitar-cambios",
    response_model=ProyectoResponse,
)
def cambios(
    id_proyecto: int,
    datos: CambioEstadoRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return solicitar_cambios(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
        comentario=datos.comentario,
    )


@router.post(
    "/{id_proyecto}/rechazar",
    response_model=ProyectoResponse,
)
def rechazar(
    id_proyecto: int,
    datos: CambioEstadoRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return rechazar_proyecto(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
        comentario=datos.comentario,
    )
@router.post(
    "/{id_proyecto}/enviar-revision",
    response_model=ProyectoResponse,
)
def enviar_revision(
    id_proyecto: int,
    datos: CambioEstadoRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return enviar_a_revision(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
        comentario=datos.comentario,
    )


@router.post(
    "/{id_proyecto}/regresar-borrador",
    response_model=ProyectoResponse,
)
def volver_borrador(
    id_proyecto: int,
    datos: CambioEstadoRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return regresar_a_borrador(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
        comentario=datos.comentario,
    )

@router.post(
    "/{id_proyecto}/publicar",
    response_model=ProyectoResponse,
)
def publicar(
    id_proyecto: int,
    datos: CambioEstadoRequest,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return publicar_proyecto(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
        comentario=datos.comentario,
    )

@router.get(
    "/{id_proyecto}/historial",
    response_model=list[HistorialEstadoResponse],
)
def historial(
    id_proyecto: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return listar_historial(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
    )

