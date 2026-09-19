from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.departamento import Departamento
from app.models.enums import EstadoProyecto, TipoParticipacion
from app.models.proyecto import Proyecto
from app.models.proyecto_autor import ProyectoAutor
from app.models.usuario import Usuario
from app.models.archivo import Archivo
from app.models.area_tematica import AreaTematica
from app.models.palabra_clave import PalabraClave
from app.models.proyecto_area import ProyectoArea
from app.models.proyecto_palabra_clave import ProyectoPalabraClave

from app.schemas.proyecto import (
    AutorProyectoResponse,
    ProyectoCreate,
    ProyectoDetalleResponse,
    ProyectoUpdate,
)
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
            Proyecto.estado == EstadoProyecto.PUBLICADO
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
            Proyecto.estado == EstadoProyecto.PUBLICADO,
        )
    )

    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado",
        )

    return proyecto

def verificar_proyecto_editable(
    db: Session,
    id_proyecto: int,
    usuario: Usuario,
) -> Proyecto:

    proyecto = obtener_proyecto(
        db=db,
        id_proyecto=id_proyecto,
    )

    if proyecto.creado_por != usuario.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar este proyecto",
        )

    if proyecto.estado != EstadoProyecto.BORRADOR:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Solo se pueden modificar proyectos en estado BORRADOR",
        )

    return proyecto

def actualizar_proyecto(
    db: Session,
    id_proyecto: int,
    datos: ProyectoUpdate,
    usuario: Usuario,
) -> Proyecto:

    proyecto = verificar_proyecto_editable(
    db=db,
    id_proyecto=id_proyecto,
    usuario=usuario,
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

    proyecto = verificar_proyecto_editable(
    db=db,
    id_proyecto=id_proyecto,
    usuario=usuario,
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


def construir_detalle_proyecto(
    db: Session,
    proyecto: Proyecto,
) -> ProyectoDetalleResponse:

    # AREAS TEMATICAS

    areas = list(
        db.scalars(
            select(AreaTematica)
            .join(
                ProyectoArea,
                ProyectoArea.id_area == AreaTematica.id_area,
            )
            .where(
                ProyectoArea.id_proyecto == proyecto.id_proyecto
            )
            .order_by(AreaTematica.nombre)
        ).all()
    )

    # PALABRAS CLAVE

    palabras = list(
        db.scalars(
            select(PalabraClave)
            .join(
                ProyectoPalabraClave,
                ProyectoPalabraClave.id_palabra_clave
                == PalabraClave.id_palabra_clave,
            )
            .where(
                ProyectoPalabraClave.id_proyecto
                == proyecto.id_proyecto
            )
            .order_by(PalabraClave.nombre)
        ).all()
    )

    # AUTORES

    filas_autores = db.execute(
        select(
            Usuario,
            ProyectoAutor.tipo_participacion,
            ProyectoAutor.orden_autoria,
        )
        .join(
            ProyectoAutor,
            ProyectoAutor.id_usuario == Usuario.id_usuario,
        )
        .where(
            ProyectoAutor.id_proyecto == proyecto.id_proyecto
        )
        .order_by(
            ProyectoAutor.orden_autoria.asc().nulls_last()
        )
    ).all()

    autores = [
        AutorProyectoResponse(
            id_usuario=autor.id_usuario,
            nombre=autor.nombre,
            apellido_paterno=autor.apellido_paterno,
            apellido_materno=autor.apellido_materno,
            tipo_participacion=tipo_participacion.value,
            orden_autoria=orden_autoria,
        )
        for autor, tipo_participacion, orden_autoria
        in filas_autores
    ]
    archivos = list(
    db.scalars(
        select(Archivo)
        .where(
            Archivo.id_proyecto
            == proyecto.id_proyecto
        )
        .order_by(
            Archivo.fecha_subida.asc()
        )
    ).all()
)

    # RESPUESTA

    return ProyectoDetalleResponse(
        id_proyecto=proyecto.id_proyecto,
        titulo=proyecto.titulo,
        resumen=proyecto.resumen,
        fecha_creacion=proyecto.fecha_creacion,
        fecha_publicacion=proyecto.fecha_publicacion,
        estado=proyecto.estado,
        id_departamento=proyecto.id_departamento,
        creado_por=proyecto.creado_por,
        areas_tematicas=areas,
        palabras_clave=palabras,
        autores=autores,
        archivos=archivos,
    )

def obtener_detalle_publico(
    db: Session,
    id_proyecto: int,
) -> ProyectoDetalleResponse:

    proyecto = obtener_proyecto_publico(
        db=db,
        id_proyecto=id_proyecto,
    )

    return construir_detalle_proyecto(
        db=db,
        proyecto=proyecto,
    )


def obtener_mi_proyecto_detalle(
    db: Session,
    id_proyecto: int,
    usuario: Usuario,
) -> ProyectoDetalleResponse:

    proyecto = obtener_proyecto(
        db=db,
        id_proyecto=id_proyecto,
    )

    participacion = db.scalar(
        select(ProyectoAutor).where(
            ProyectoAutor.id_proyecto == id_proyecto,
            ProyectoAutor.id_usuario == usuario.id_usuario,
        )
    )

    if participacion is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este proyecto",
        )

    return construir_detalle_proyecto(
        db=db,
        proyecto=proyecto,
    )