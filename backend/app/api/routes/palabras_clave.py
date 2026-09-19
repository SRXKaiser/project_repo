from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.palabra_clave import (
    PalabraClaveCreate,
    PalabraClaveResponse,
)
from app.services.palabra_clave_service import (
    agregar_palabra_clave,
    eliminar_palabra_clave,
    listar_palabras_clave,
)


router = APIRouter(
    tags=["Palabras clave"],
)


@router.get(
    "/palabras-clave",
    response_model=list[PalabraClaveResponse],
)
def listar(
    db: Session = Depends(get_db),
):
    return listar_palabras_clave(db)


@router.post(
    "/proyectos/{id_proyecto}/palabras-clave",
    response_model=PalabraClaveResponse,
    status_code=status.HTTP_201_CREATED,
)
def agregar(
    id_proyecto: int,
    datos: PalabraClaveCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return agregar_palabra_clave(
        db=db,
        id_proyecto=id_proyecto,
        datos=datos,
        usuario=usuario,
    )


@router.delete(
    "/proyectos/{id_proyecto}/palabras-clave/{id_palabra_clave}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar(
    id_proyecto: int,
    id_palabra_clave: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    eliminar_palabra_clave(
        db=db,
        id_proyecto=id_proyecto,
        id_palabra_clave=id_palabra_clave,
        usuario=usuario,
    )