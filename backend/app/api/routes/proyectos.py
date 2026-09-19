from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.proyecto import (
    ProyectoCreate,
    ProyectoDetalleResponse,
    ProyectoResponse,
    ProyectoUpdate,
)
from app.services.proyecto_service import (
    actualizar_proyecto,
    crear_proyecto,
    eliminar_proyecto,
    listar_mis_proyectos,
    listar_proyectos,
    obtener_detalle_publico,
    obtener_mi_proyecto_detalle,
    obtener_proyecto_publico,
)




router = APIRouter(
    prefix="/proyectos",
    tags=["Proyectos"],
)


@router.post(
    "",
    response_model=ProyectoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear(
    datos: ProyectoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return crear_proyecto(
        db=db,
        datos=datos,
        usuario=usuario,
    )


@router.get(
    "",
    response_model=list[ProyectoResponse],
)
def listar(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    return listar_proyectos(
        db=db,
        skip=skip,
        limit=limit,
    )

@router.get(
    "/mis-proyectos",
    response_model=list[ProyectoResponse],
)
def mis_proyectos(
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return listar_mis_proyectos(
        db=db,
        usuario=usuario,
        skip=skip,
        limit=limit,
    )

@router.get(
    "/mis-proyectos/{id_proyecto}",
    response_model=ProyectoDetalleResponse,
)
def mi_proyecto_detalle(
    id_proyecto: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return obtener_mi_proyecto_detalle(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
    )


@router.get(
    "/{id_proyecto}/detalle",
    response_model=ProyectoDetalleResponse,
)
def detalle_publico(
    id_proyecto: int,
    db: Session = Depends(get_db),
):
    return obtener_detalle_publico(
        db=db,
        id_proyecto=id_proyecto,
    )

@router.get(
    "/{id_proyecto}",
    response_model=ProyectoResponse,
)
def obtener(
    id_proyecto: int,
    db: Session = Depends(get_db),
):
    return obtener_proyecto_publico(
        db=db,
        id_proyecto=id_proyecto,
    )

@router.put(
    "/{id_proyecto}",
    response_model=ProyectoResponse,
)
def actualizar(
    id_proyecto: int,
    datos: ProyectoUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return actualizar_proyecto(
        db=db,
        id_proyecto=id_proyecto,
        datos=datos,
        usuario=usuario,
    )


@router.delete(
    "/{id_proyecto}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar(
    id_proyecto: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    eliminar_proyecto(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
    )