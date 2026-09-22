from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import puede_consultar_proyecto_privado
from app.models.enums import TipoParticipacion
from app.models.proyecto_autor import ProyectoAutor
from app.models.usuario import Usuario
from app.schemas.proyecto_autor import ProyectoAutorCreate
from app.services.proyecto_service import verificar_proyecto_editable


def listar_participantes(
    db: Session,
    id_proyecto: int,
    usuario: Usuario,
) -> list[ProyectoAutor]:

    if not puede_consultar_proyecto_privado(
        db=db,
        usuario=usuario,
        id_proyecto=id_proyecto,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a los participantes de este proyecto",
        )

    consulta = (
        select(ProyectoAutor)
        .where(
            ProyectoAutor.id_proyecto == id_proyecto
        )
        .order_by(
            ProyectoAutor.orden_autoria.asc().nulls_last()
        )
    )

    return list(
        db.scalars(consulta).all()
    )


def agregar_participante(
    db: Session,
    id_proyecto: int,
    datos: ProyectoAutorCreate,
    usuario_actual: Usuario,
) -> ProyectoAutor:

    proyecto = verificar_proyecto_editable(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario_actual,
    )

    usuario_nuevo = db.get(
        Usuario,
        datos.id_usuario,
    )

    if usuario_nuevo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario especificado no existe",
        )

    existente = db.scalar(
        select(ProyectoAutor).where(
            ProyectoAutor.id_proyecto == id_proyecto,
            ProyectoAutor.id_usuario == datos.id_usuario,
        )
    )

    if existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El usuario ya participa en este proyecto",
        )

    # Para AUTOR exigimos orden de autoría.
    if (
        datos.tipo_participacion
        == TipoParticipacion.AUTOR
        and datos.orden_autoria is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Los participantes de tipo AUTOR "
                "requieren orden_autoria"
            ),
        )

    # ASESOR y COLABORADOR no utilizan orden de autoría.
    orden_autoria = datos.orden_autoria

    if datos.tipo_participacion != TipoParticipacion.AUTOR:
        orden_autoria = None

    # Evitar dos autores con el mismo orden.
    if orden_autoria is not None:
        orden_existente = db.scalar(
            select(ProyectoAutor).where(
                ProyectoAutor.id_proyecto == id_proyecto,
                ProyectoAutor.tipo_participacion
                == TipoParticipacion.AUTOR,
                ProyectoAutor.orden_autoria
                == orden_autoria,
            )
        )

        if orden_existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Ya existe un autor con ese "
                    "orden de autoría"
                ),
            )

    participante = ProyectoAutor(
        id_proyecto=proyecto.id_proyecto,
        id_usuario=datos.id_usuario,
        tipo_participacion=datos.tipo_participacion,
        orden_autoria=orden_autoria,
    )

    try:
        db.add(participante)
        db.commit()
        db.refresh(participante)

        return participante

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se pudo agregar el participante porque "
                "existe un conflicto con los datos del proyecto"
            ),
        )

    except Exception:
        db.rollback()
        raise


def eliminar_participante(
    db: Session,
    id_proyecto: int,
    id_usuario: int,
    usuario_actual: Usuario,
) -> None:

    proyecto = verificar_proyecto_editable(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario_actual,
    )

    participante = db.scalar(
        select(ProyectoAutor).where(
            ProyectoAutor.id_proyecto == id_proyecto,
            ProyectoAutor.id_usuario == id_usuario,
        )
    )

    if participante is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario no participa en este proyecto",
        )

    # Nunca permitimos quitar al creador desde este endpoint.
    if id_usuario == proyecto.creado_por:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se puede eliminar al creador "
                "del proyecto"
            ),
        )

    try:
        db.delete(participante)
        db.commit()

    except Exception:
        db.rollback()
        raise