from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import require_admin
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.responsable_departamento import (
    AsignarResponsableRequest,
    ResponsableDepartamentoResponse,
    ResponsableDetalleResponse,
)
from app.services.responsable_departamento_service import (
    asignar_responsable,
    listar_responsables_activos,
    obtener_responsable_departamento,
    retirar_responsable,
)


router = APIRouter(
    prefix="/admin/departamentos",
    tags=["Administración - Responsables"],
)


@router.get(
    "/responsables",
    response_model=list[ResponsableDetalleResponse],
)
def listar(
    db: Session = Depends(get_db),
    administrador: Usuario = Depends(require_admin),
):
    return listar_responsables_activos(
        db=db,
    )


@router.get(
    "/{id_departamento}/responsable",
    response_model=ResponsableDetalleResponse,
)
def obtener(
    id_departamento: int,
    db: Session = Depends(get_db),
    administrador: Usuario = Depends(require_admin),
):
    return obtener_responsable_departamento(
        db=db,
        id_departamento=id_departamento,
    )


@router.put(
    "/{id_departamento}/responsable",
    response_model=ResponsableDepartamentoResponse,
)
def asignar(
    id_departamento: int,
    datos: AsignarResponsableRequest,
    db: Session = Depends(get_db),
    administrador: Usuario = Depends(require_admin),
):
    return asignar_responsable(
        db=db,
        id_departamento=id_departamento,
        id_usuario_docente=datos.id_usuario_docente,
    )


@router.delete(
    "/{id_departamento}/responsable",
    response_model=ResponsableDepartamentoResponse,
)
def retirar(
    id_departamento: int,
    db: Session = Depends(get_db),
    administrador: Usuario = Depends(require_admin),
):
    return retirar_responsable(
        db=db,
        id_departamento=id_departamento,
    )