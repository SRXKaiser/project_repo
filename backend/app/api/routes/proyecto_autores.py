from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.proyecto_autor import (
    ProyectoAutorCreate,
    ProyectoAutorResponse,
)
from app.services.proyecto_autor_service import (
    agregar_participante,
    eliminar_participante,
    listar_participantes,
)


router = APIRouter(
    prefix="/proyectos",
    tags=["Participantes de proyectos"],
)


@router.get(
    "/{id_proyecto}/participantes",
    response_model=list[ProyectoAutorResponse],
)
def listar(
    id_proyecto: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return listar_participantes(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
    )


@router.post(
    "/{id_proyecto}/participantes",
    response_model=ProyectoAutorResponse,
    status_code=status.HTTP_201_CREATED,
)
def agregar(
    id_proyecto: int,
    datos: ProyectoAutorCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return agregar_participante(
        db=db,
        id_proyecto=id_proyecto,
        datos=datos,
        usuario_actual=usuario,
    )


@router.delete(
    "/{id_proyecto}/participantes/{id_usuario}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar(
    id_proyecto: int,
    id_usuario: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    eliminar_participante(
        db=db,
        id_proyecto=id_proyecto,
        id_usuario=id_usuario,
        usuario_actual=usuario,
    )