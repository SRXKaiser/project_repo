from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.area_tematica import AreaTematica
from app.models.proyecto_area import ProyectoArea
from app.models.usuario import Usuario
from app.services.proyecto_service import verificar_proyecto_editable


def listar_areas_tematicas(
    db: Session,
) -> list[AreaTematica]:

    consulta = (
        select(AreaTematica)
        .order_by(AreaTematica.nombre)
    )

    return list(
        db.scalars(consulta).all()
    )


def asignar_area_proyecto(
    db: Session,
    id_proyecto: int,
    id_area: int,
    usuario: Usuario,
) -> AreaTematica:

    verificar_proyecto_editable(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
    )

    area = db.get(
        AreaTematica,
        id_area,
    )

    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Área temática no encontrada",
        )

    relacion = db.scalar(
        select(ProyectoArea).where(
            ProyectoArea.id_proyecto == id_proyecto,
            ProyectoArea.id_area == id_area,
        )
    )

    if relacion is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El proyecto ya tiene asignada esta área temática",
        )

    try:
        relacion = ProyectoArea(
            id_proyecto=id_proyecto,
            id_area=id_area,
        )

        db.add(relacion)
        db.commit()

        return area

    except Exception:
        db.rollback()
        raise


def eliminar_area_proyecto(
    db: Session,
    id_proyecto: int,
    id_area: int,
    usuario: Usuario,
) -> None:

    verificar_proyecto_editable(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
    )

    relacion = db.scalar(
        select(ProyectoArea).where(
            ProyectoArea.id_proyecto == id_proyecto,
            ProyectoArea.id_area == id_area,
        )
    )

    if relacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El proyecto no tiene asignada esta área temática",
        )

    try:
        db.delete(relacion)
        db.commit()

    except Exception:
        db.rollback()
        raise