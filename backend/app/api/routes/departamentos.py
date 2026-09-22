from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.departamento import Departamento


router = APIRouter(
    prefix="/departamentos",
    tags=["Departamentos"],
)


@router.get("")
def listar_departamentos_publicos(
    db: Session = Depends(get_db),
):
    departamentos = db.scalars(
        select(Departamento)
        .order_by(Departamento.nombre)
    ).all()

    return [
        {
            "id_departamento": departamento.id_departamento,
            "nombre": departamento.nombre,
            "descripcion": departamento.descripcion,
        }
        for departamento in departamentos
    ]