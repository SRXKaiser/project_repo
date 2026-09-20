from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.admin_catalogo import (
    AreaTematicaCreate,
    AreaTematicaUpdate,
    CarreraCreate,
    CarreraEstadoRequest,
    CarreraResponse,
    CarreraUpdate,
    DepartamentoCreate,
    DepartamentoResponse,
    DepartamentoUpdate,
)
from app.schemas.area_tematica import AreaTematicaResponse
from app.services.admin_catalogo_service import (
    actualizar_area,
    actualizar_carrera,
    actualizar_departamento,
    cambiar_estado_carrera,
    crear_area,
    crear_carrera,
    crear_departamento,
    listar_carreras,
    listar_departamentos,
)


router = APIRouter(
    prefix="/admin/catalogos",
    tags=["Administración - Catálogos"],
    dependencies=[Depends(require_admin)],
)


# Departamentos

@router.get(
    "/departamentos",
    response_model=list[DepartamentoResponse],
)
def departamentos(
    db: Session = Depends(get_db),
):
    return listar_departamentos(db)


@router.post(
    "/departamentos",
    response_model=DepartamentoResponse,
    status_code=status.HTTP_201_CREATED,
)
def nuevo_departamento(
    datos: DepartamentoCreate,
    db: Session = Depends(get_db),
):
    return crear_departamento(db, datos)


@router.patch(
    "/departamentos/{id_departamento}",
    response_model=DepartamentoResponse,
)
def editar_departamento(
    id_departamento: int,
    datos: DepartamentoUpdate,
    db: Session = Depends(get_db),
):
    return actualizar_departamento(
        db,
        id_departamento,
        datos,
    )


# Carreras

@router.get(
    "/carreras",
    response_model=list[CarreraResponse],
)
def carreras(
    db: Session = Depends(get_db),
):
    return listar_carreras(db)


@router.post(
    "/carreras",
    response_model=CarreraResponse,
    status_code=status.HTTP_201_CREATED,
)
def nueva_carrera(
    datos: CarreraCreate,
    db: Session = Depends(get_db),
):
    return crear_carrera(db, datos)


@router.patch(
    "/carreras/{id_carrera}",
    response_model=CarreraResponse,
)
def editar_carrera(
    id_carrera: int,
    datos: CarreraUpdate,
    db: Session = Depends(get_db),
):
    return actualizar_carrera(
        db,
        id_carrera,
        datos,
    )


@router.patch(
    "/carreras/{id_carrera}/estado",
    response_model=CarreraResponse,
)
def estado_carrera(
    id_carrera: int,
    datos: CarreraEstadoRequest,
    db: Session = Depends(get_db),
):
    return cambiar_estado_carrera(
        db,
        id_carrera,
        datos.activa,
    )


# Areas tematicas

@router.post(
    "/areas-tematicas",
    response_model=AreaTematicaResponse,
    status_code=status.HTTP_201_CREATED,
)
def nueva_area(
    datos: AreaTematicaCreate,
    db: Session = Depends(get_db),
):
    return crear_area(db, datos)


@router.patch(
    "/areas-tematicas/{id_area}",
    response_model=AreaTematicaResponse,
)
def editar_area(
    id_area: int,
    datos: AreaTematicaUpdate,
    db: Session = Depends(get_db),
):
    return actualizar_area(
        db,
        id_area,
        datos,
    )