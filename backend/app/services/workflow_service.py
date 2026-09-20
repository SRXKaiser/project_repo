from datetime import date, datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import (
    es_administrador,
    es_jefe_departamento,
    puede_consultar_proyecto_privado,
)
from app.models.archivo import Archivo
from app.models.enums import EstadoProyecto, TipoParticipacion
from app.models.historial_estado import HistorialEstado
from app.models.proyecto import Proyecto
from app.models.proyecto_area import ProyectoArea
from app.models.proyecto_autor import ProyectoAutor
from app.models.proyecto_palabra_clave import ProyectoPalabraClave
from app.models.responsable_departamento import ResponsableDepartamento
from app.models.usuario import Usuario


def obtener_proyecto_workflow(
    db: Session,
    id_proyecto: int,
) -> Proyecto:

    proyecto = db.get(
        Proyecto,
        id_proyecto,
    )

    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado",
        )

    return proyecto


def registrar_cambio_estado(
    db: Session,
    proyecto: Proyecto,
    estado_nuevo: EstadoProyecto,
    usuario: Usuario,
    comentario: str | None = None,
) -> HistorialEstado:

    estado_anterior = proyecto.estado

    historial = HistorialEstado(
        id_proyecto=proyecto.id_proyecto,
        estado_anterior=estado_anterior,
        estado_nuevo=estado_nuevo,
        cambiado_por=usuario.id_usuario,
        comentario=(
            comentario.strip()
            if comentario and comentario.strip()
            else None
        ),
    )

    proyecto.estado = estado_nuevo

    db.add(historial)

    return historial


def verificar_creador(
    proyecto: Proyecto,
    usuario: Usuario,
) -> None:

    if proyecto.creado_por != usuario.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Solo el creador del proyecto "
                "puede realizar esta acción"
            ),
        )


def verificar_requisitos_revision(
    db: Session,
    id_proyecto: int,
) -> None:
    """
    Verifica que un proyecto tenga la información mínima
    necesaria antes de enviarse a revisión.
    """

    # Debe existir al menos un AUTOR.
    autor = db.scalar(
        select(ProyectoAutor).where(
            ProyectoAutor.id_proyecto == id_proyecto,
            ProyectoAutor.tipo_participacion
            == TipoParticipacion.AUTOR,
        )
    )

    if autor is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El proyecto debe tener al menos un autor",
        )

    # Debe tener al menos un área temática.
    area = db.scalar(
        select(ProyectoArea).where(
            ProyectoArea.id_proyecto == id_proyecto,
        )
    )

    if area is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "El proyecto debe tener al menos "
                "un área temática"
            ),
        )

    # Debe tener al menos una palabra clave.
    palabra_clave = db.scalar(
        select(ProyectoPalabraClave).where(
            ProyectoPalabraClave.id_proyecto == id_proyecto,
        )
    )

    if palabra_clave is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "El proyecto debe tener al menos "
                "una palabra clave"
            ),
        )

    # Debe tener al menos un archivo PDF.
    archivo = db.scalar(
        select(Archivo).where(
            Archivo.id_proyecto == id_proyecto,
            Archivo.tipo_mime == "application/pdf",
        )
    )

    if archivo is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "El proyecto debe tener al menos "
                "un archivo PDF"
            ),
        )


def enviar_a_revision(
    db: Session,
    id_proyecto: int,
    usuario: Usuario,
    comentario: str | None = None,
) -> Proyecto:

    proyecto = obtener_proyecto_workflow(
        db=db,
        id_proyecto=id_proyecto,
    )

    verificar_creador(
        proyecto=proyecto,
        usuario=usuario,
    )

    if proyecto.estado != EstadoProyecto.BORRADOR:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Solo un proyecto en estado BORRADOR "
                "puede enviarse a revisión"
            ),
        )

    verificar_requisitos_revision(
        db=db,
        id_proyecto=id_proyecto,
    )

    try:
        registrar_cambio_estado(
            db=db,
            proyecto=proyecto,
            estado_nuevo=EstadoProyecto.EN_REVISION,
            usuario=usuario,
            comentario=comentario,
        )

        db.commit()
        db.refresh(proyecto)

        return proyecto

    except Exception:
        db.rollback()
        raise


def regresar_a_borrador(
    db: Session,
    id_proyecto: int,
    usuario: Usuario,
    comentario: str | None = None,
) -> Proyecto:

    proyecto = obtener_proyecto_workflow(
        db=db,
        id_proyecto=id_proyecto,
    )

    verificar_creador(
        proyecto=proyecto,
        usuario=usuario,
    )

    if proyecto.estado != EstadoProyecto.REQUIERE_CAMBIOS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Solo un proyecto que REQUIERE_CAMBIOS "
                "puede regresar a BORRADOR"
            ),
        )

    try:
        registrar_cambio_estado(
            db=db,
            proyecto=proyecto,
            estado_nuevo=EstadoProyecto.BORRADOR,
            usuario=usuario,
            comentario=comentario,
        )

        db.commit()
        db.refresh(proyecto)

        return proyecto

    except Exception:
        db.rollback()
        raise


def listar_historial(
    db: Session,
    id_proyecto: int,
    usuario: Usuario,
) -> list[HistorialEstado]:

    obtener_proyecto_workflow(
        db=db,
        id_proyecto=id_proyecto,
    )

    if not puede_consultar_proyecto_privado(
        db=db,
        usuario=usuario,
        id_proyecto=id_proyecto,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "No tienes acceso al historial "
                "de este proyecto"
            ),
        )

    consulta = (
        select(HistorialEstado)
        .where(
            HistorialEstado.id_proyecto == id_proyecto
        )
        .order_by(
            HistorialEstado.fecha_cambio.asc(),
            HistorialEstado.id_historial.asc(),
        )
    )

    return list(
        db.scalars(consulta).all()
    )


def verificar_permiso_revision(
    db: Session,
    proyecto: Proyecto,
    usuario: Usuario,
) -> None:

    if es_administrador(
        db=db,
        usuario=usuario,
    ):
        return

    if es_jefe_departamento(
        db=db,
        usuario=usuario,
        id_departamento=proyecto.id_departamento,
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=(
            "No tienes permisos para revisar "
            "este proyecto"
        ),
    )


def aprobar_proyecto(
    db: Session,
    id_proyecto: int,
    usuario: Usuario,
    comentario: str | None = None,
) -> Proyecto:

    proyecto = obtener_proyecto_workflow(
        db=db,
        id_proyecto=id_proyecto,
    )

    verificar_permiso_revision(
        db=db,
        proyecto=proyecto,
        usuario=usuario,
    )

    if proyecto.estado != EstadoProyecto.EN_REVISION:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Solo un proyecto EN_REVISION "
                "puede aprobarse"
            ),
        )

    try:
        registrar_cambio_estado(
            db=db,
            proyecto=proyecto,
            estado_nuevo=EstadoProyecto.APROBADO,
            usuario=usuario,
            comentario=comentario,
        )

        db.commit()
        db.refresh(proyecto)

        return proyecto

    except Exception:
        db.rollback()
        raise


def solicitar_cambios(
    db: Session,
    id_proyecto: int,
    usuario: Usuario,
    comentario: str | None,
) -> Proyecto:

    proyecto = obtener_proyecto_workflow(
        db=db,
        id_proyecto=id_proyecto,
    )

    verificar_permiso_revision(
        db=db,
        proyecto=proyecto,
        usuario=usuario,
    )

    if proyecto.estado != EstadoProyecto.EN_REVISION:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Solo un proyecto EN_REVISION "
                "puede requerir cambios"
            ),
        )

    if not comentario or not comentario.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Debes indicar qué cambios "
                "requiere el proyecto"
            ),
        )

    try:
        registrar_cambio_estado(
            db=db,
            proyecto=proyecto,
            estado_nuevo=EstadoProyecto.REQUIERE_CAMBIOS,
            usuario=usuario,
            comentario=comentario,
        )

        db.commit()
        db.refresh(proyecto)

        return proyecto

    except Exception:
        db.rollback()
        raise


def rechazar_proyecto(
    db: Session,
    id_proyecto: int,
    usuario: Usuario,
    comentario: str | None,
) -> Proyecto:

    proyecto = obtener_proyecto_workflow(
        db=db,
        id_proyecto=id_proyecto,
    )

    verificar_permiso_revision(
        db=db,
        proyecto=proyecto,
        usuario=usuario,
    )

    if proyecto.estado != EstadoProyecto.EN_REVISION:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Solo un proyecto EN_REVISION "
                "puede rechazarse"
            ),
        )

    if not comentario or not comentario.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Debes indicar el motivo "
                "del rechazo"
            ),
        )

    try:
        registrar_cambio_estado(
            db=db,
            proyecto=proyecto,
            estado_nuevo=EstadoProyecto.RECHAZADO,
            usuario=usuario,
            comentario=comentario,
        )

        db.commit()
        db.refresh(proyecto)

        return proyecto

    except Exception:
        db.rollback()
        raise


def listar_pendientes_revision(
    db: Session,
    usuario: Usuario,
) -> list[Proyecto]:

    # Administrador:
    # puede ver todos los proyectos pendientes.
    if es_administrador(
        db=db,
        usuario=usuario,
    ):
        consulta = (
            select(Proyecto)
            .where(
                Proyecto.estado
                == EstadoProyecto.EN_REVISION
            )
            .order_by(
                Proyecto.fecha_creacion.asc()
            )
        )

        return list(
            db.scalars(consulta).all()
        )

    # Responsable de departamento:
    # obtenemos los departamentos activos
    # de los que es responsable.
    hoy = date.today()
    departamentos = list(
        db.scalars(
            select(
                ResponsableDepartamento.id_departamento
            )
            .where(
                ResponsableDepartamento.id_usuario_docente
                == usuario.id_usuario,

                ResponsableDepartamento.activo.is_(True),

                ResponsableDepartamento.fecha_inicio <= hoy,

                (
                    ResponsableDepartamento.fecha_fin.is_(None)
                    | (ResponsableDepartamento.fecha_fin >= hoy)
                ),
            )
        ).all()
    )   

    if not departamentos:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "No tienes permisos para revisar proyectos"
            ),
        )

    consulta = (
        select(Proyecto)
        .where(
            Proyecto.estado
            == EstadoProyecto.EN_REVISION,

            Proyecto.id_departamento.in_(
                departamentos
            ),
        )
        .order_by(
            Proyecto.fecha_creacion.asc()
        )
    )

    return list(
        db.scalars(consulta).all()
    )


def publicar_proyecto(
    db: Session,
    id_proyecto: int,
    usuario: Usuario,
    comentario: str | None = None,
) -> Proyecto:

    proyecto = obtener_proyecto_workflow(
        db=db,
        id_proyecto=id_proyecto,
    )

    verificar_permiso_revision(
        db=db,
        proyecto=proyecto,
        usuario=usuario,
    )

    if proyecto.estado != EstadoProyecto.APROBADO:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Solo un proyecto APROBADO "
                "puede publicarse"
            ),
        )

    try:
        registrar_cambio_estado(
            db=db,
            proyecto=proyecto,
            estado_nuevo=EstadoProyecto.PUBLICADO,
            usuario=usuario,
            comentario=comentario,
        )

        proyecto.fecha_publicacion = datetime.now(
            timezone.utc
        )

        db.commit()
        db.refresh(proyecto)

        return proyecto

    except Exception:
        db.rollback()
        raise