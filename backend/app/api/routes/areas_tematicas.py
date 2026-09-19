from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.area_tematica import AreaTematicaResponse
from app.services.area_tematica_service import (
    asignar_area_proyecto,
    eliminar_area_proyecto,
    listar_areas_tematicas,
)


router = APIRouter(
    tags=["Áreas temáticas"],
)


@router.get(
    "/areas-tematicas",
    response_model=list[AreaTematicaResponse],
)
def listar(
    db: Session = Depends(get_db),
):
    return listar_areas_tematicas(db)


@router.post(
    "/proyectos/{id_proyecto}/areas/{id_area}",
    response_model=AreaTematicaResponse,
    status_code=status.HTTP_201_CREATED,
)
def asignar(
    id_proyecto: int,
    id_area: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return asignar_area_proyecto(
        db=db,
        id_proyecto=id_proyecto,
        id_area=id_area,
        usuario=usuario,
    )


@router.delete(
    "/proyectos/{id_proyecto}/areas/{id_area}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar(
    id_proyecto: int,
    id_area: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    eliminar_area_proyecto(
        db=db,
        id_proyecto=id_proyecto,
        id_area=id_area,
        usuario=usuario,
    )