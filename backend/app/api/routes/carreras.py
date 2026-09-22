from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.carrera import Carrera


router = APIRouter(
    prefix="/carreras",
    tags=["Carreras"],
)


@router.get("")
def listar_carreras_publicas(
    db: Session = Depends(get_db),
):
    carreras = db.scalars(
        select(Carrera)
        .where(Carrera.activa.is_(True))
        .order_by(Carrera.nombre)
    ).all()

    return [
        {
            "id_carrera": carrera.id_carrera,
            "nombre": carrera.nombre,
            "siglas": carrera.siglas,
            "id_departamento": carrera.id_departamento,
        }
        for carrera in carreras
    ]