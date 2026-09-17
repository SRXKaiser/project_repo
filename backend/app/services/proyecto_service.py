from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.departamento import Departamento
from app.models.enums import EstadoProyecto, TipoParticipacion
from app.models.proyecto import Proyecto
from app.models.proyecto_autor import ProyectoAutor
from app.models.usuario import Usuario
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate

def crear_proyecto(
    db: Session,
    datos: ProyectoCreate,
    usuario: Usuario,
) -> Proyecto:

    # Verificar que el departamento exista.
    departamento = db.get(
        Departamento,
        datos.id_departamento
    )

    if departamento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El departamento especificado no existe",
        )

    proyecto = Proyecto(
        titulo=datos.titulo.strip(),
        resumen=datos.resumen.strip(),
        estado=EstadoProyecto.BORRADOR,
        id_departamento=datos.id_departamento,
        creado_por=usuario.id_usuario,
    )

    try:
        db.add(proyecto)

        # Necesitamos el ID antes de crear ProyectoAutor.
        db.flush()

        autor = ProyectoAutor(
            id_proyecto=proyecto.id_proyecto,
            id_usuario=usuario.id_usuario,
            tipo_participacion=TipoParticipacion.AUTOR,
            orden_autoria=1,
        )

        db.add(autor)

        db.commit()
        db.refresh(proyecto)

        return proyecto

    except Exception:
        db.rollback()
        raise


def listar_proyectos(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> list[Proyecto]:

    consulta = (
        select(Proyecto)
        .where(
            Proyecto.estado == EstadoProyecto.APROBADO
        )
        .order_by(Proyecto.fecha_publicacion.desc())
        .offset(skip)
        .limit(limit)
    )

    return list(
        db.scalars(consulta).all()
    )


def obtener_proyecto(
    db: Session,
    id_proyecto: int,
) -> Proyecto:

    proyecto = db.get(
        Proyecto,
        id_proyecto
    )

    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado",
        )

    return proyecto

def obtener_proyecto_publico(
    db: Session,
    id_proyecto: int,
) -> Proyecto:

    proyecto = db.scalar(
        select(Proyecto).where(
            Proyecto.id_proyecto == id_proyecto,
            Proyecto.estado == EstadoProyecto.APROBADO,
        )
    )

    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado",
        )

    return proyecto

def actualizar_proyecto(
    db: Session,
    id_proyecto: int,
    datos: ProyectoUpdate,
    usuario: Usuario,
) -> Proyecto:

    proyecto = obtener_proyecto(
        db=db,
        id_proyecto=id_proyecto,
    )

    # Solo el creador puede modificarlo.
    if proyecto.creado_por != usuario.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar este proyecto",
        )

    # Solo los borradores pueden editarse.
    if proyecto.estado != EstadoProyecto.BORRADOR:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Solo se pueden modificar proyectos en estado BORRADOR",
        )

    cambios = datos.model_dump(
        exclude_unset=True
    )

    if "id_departamento" in cambios:
        departamento = db.get(
            Departamento,
            cambios["id_departamento"],
        )

        if departamento is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El departamento especificado no existe",
            )

    if "titulo" in cambios:
        cambios["titulo"] = cambios["titulo"].strip()

    if "resumen" in cambios:
        cambios["resumen"] = cambios["resumen"].strip()

    for campo, valor in cambios.items():
        setattr(
            proyecto,
            campo,
            valor,
        )

    try:
        db.commit()
        db.refresh(proyecto)

        return proyecto

    except Exception:
        db.rollback()
        raise


def eliminar_proyecto(
    db: Session,
    id_proyecto: int,
    usuario: Usuario,
) -> None:

    proyecto = obtener_proyecto(
        db=db,
        id_proyecto=id_proyecto,
    )

    # Solo el creador puede eliminarlo.
    if proyecto.creado_por != usuario.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este proyecto",
        )

    # Solo los borradores pueden eliminarse.
    if proyecto.estado != EstadoProyecto.BORRADOR:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Solo se pueden eliminar proyectos en estado BORRADOR",
        )

    try:
        db.delete(proyecto)
        db.commit()

    except Exception:
        db.rollback()
        raise

def listar_mis_proyectos(
    db: Session,
    usuario: Usuario,
    skip: int = 0,
    limit: int = 20,
) -> list[Proyecto]:

    consulta = (
        select(Proyecto)
        .join(
            ProyectoAutor,
            ProyectoAutor.id_proyecto
            == Proyecto.id_proyecto,
        )
        .where(
            ProyectoAutor.id_usuario
            == usuario.id_usuario
        )
        .order_by(
            Proyecto.fecha_creacion.desc()
        )
        .offset(skip)
        .limit(limit)
    )

    return list(
        db.scalars(consulta).all()
    )