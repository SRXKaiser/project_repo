from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.palabra_clave import PalabraClave
from app.models.proyecto_palabra_clave import ProyectoPalabraClave
from app.models.usuario import Usuario
from app.schemas.palabra_clave import PalabraClaveCreate
from app.services.proyecto_service import verificar_proyecto_editable


def listar_palabras_clave(
    db: Session,
) -> list[PalabraClave]:

    consulta = (
        select(PalabraClave)
        .order_by(PalabraClave.nombre)
    )

    return list(
        db.scalars(consulta).all()
    )


def agregar_palabra_clave(
    db: Session,
    id_proyecto: int,
    datos: PalabraClaveCreate,
    usuario: Usuario,
) -> PalabraClave:

    verificar_proyecto_editable(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
    )

    nombre = datos.nombre.strip()

    palabra = db.scalar(
        select(PalabraClave).where(
            func.lower(PalabraClave.nombre)
            == nombre.lower()
        )
    )

    try:
        # Reutilizamos la palabra si ya existe.
        if palabra is None:
            palabra = PalabraClave(
                nombre=nombre
            )

            db.add(palabra)
            db.flush()

        relacion = db.scalar(
            select(ProyectoPalabraClave).where(
                ProyectoPalabraClave.id_proyecto
                == id_proyecto,

                ProyectoPalabraClave.id_palabra_clave
                == palabra.id_palabra_clave,
            )
        )

        if relacion is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El proyecto ya tiene esta palabra clave",
            )

        relacion = ProyectoPalabraClave(
            id_proyecto=id_proyecto,
            id_palabra_clave=palabra.id_palabra_clave,
        )

        db.add(relacion)
        db.commit()
        db.refresh(palabra)

        return palabra

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise


def eliminar_palabra_clave(
    db: Session,
    id_proyecto: int,
    id_palabra_clave: int,
    usuario: Usuario,
) -> None:

    verificar_proyecto_editable(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
    )

    relacion = db.scalar(
        select(ProyectoPalabraClave).where(
            ProyectoPalabraClave.id_proyecto
            == id_proyecto,

            ProyectoPalabraClave.id_palabra_clave
            == id_palabra_clave,
        )
    )

    if relacion is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El proyecto no tiene esta palabra clave",
        )

    try:
        db.delete(relacion)
        db.commit()

    except Exception:
        db.rollback()
        raise