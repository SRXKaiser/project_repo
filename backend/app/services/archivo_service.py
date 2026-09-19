from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import EstadoProyecto
from app.models.proyecto import Proyecto

from app.models.archivo import Archivo
from app.models.proyecto_autor import ProyectoAutor
from app.models.usuario import Usuario
from app.services.proyecto_service import (
    obtener_proyecto,
    verificar_proyecto_editable,
)


STORAGE_ROOT = Path("storage/proyectos")

TIPOS_PERMITIDOS = {
    "application/pdf": ".pdf",
}

TAMANIO_MAXIMO = 10 * 1024 * 1024  # 10 MB


def listar_archivos_proyecto(
    db: Session,
    id_proyecto: int,
    usuario: Usuario,
) -> list[Archivo]:

    obtener_proyecto(
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
            detail="No tienes acceso a los archivos de este proyecto",
        )

    consulta = (
        select(Archivo)
        .where(
            Archivo.id_proyecto == id_proyecto
        )
        .order_by(
            Archivo.fecha_subida.desc()
        )
    )

    return list(
        db.scalars(consulta).all()
    )


def subir_archivo(
    db: Session,
    id_proyecto: int,
    archivo: UploadFile,
    usuario: Usuario,
) -> Archivo:

    proyecto = verificar_proyecto_editable(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
    )

    if archivo.content_type not in TIPOS_PERMITIDOS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Solo se permiten archivos PDF",
        )

    contenido = archivo.file.read()

    if not contenido:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo está vacío",
        )

    if len(contenido) > TAMANIO_MAXIMO:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="El archivo supera el límite de 10 MB",
        )

    # Verificación básica de la firma PDF.
    if not contenido.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo no contiene un PDF válido",
        )

    extension = TIPOS_PERMITIDOS[archivo.content_type]

    nombre_almacenado = (
        f"{uuid4().hex}{extension}"
    )

    directorio_proyecto = (
        STORAGE_ROOT / str(proyecto.id_proyecto)
    )

    directorio_proyecto.mkdir(
        parents=True,
        exist_ok=True,
    )

    ruta = directorio_proyecto / nombre_almacenado

    try:
        ruta.write_bytes(contenido)

        registro = Archivo(
            id_proyecto=proyecto.id_proyecto,
            nombre_original=(
                archivo.filename or "documento.pdf"
            )[:255],
            nombre_almacenado=nombre_almacenado,
            tipo_mime=archivo.content_type,
            tamanio=len(contenido),
            ruta_archivo=str(ruta),
            subido_por=usuario.id_usuario,
        )

        db.add(registro)
        db.commit()
        db.refresh(registro)

        return registro

    except Exception:
        db.rollback()

        if ruta.exists():
            ruta.unlink()

        raise


def obtener_archivo(
    db: Session,
    id_archivo: int,
    usuario: Usuario,
) -> Archivo:

    registro = db.get(
        Archivo,
        id_archivo,
    )

    if registro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archivo no encontrado",
        )

    participacion = db.scalar(
        select(ProyectoAutor).where(
            ProyectoAutor.id_proyecto
            == registro.id_proyecto,

            ProyectoAutor.id_usuario
            == usuario.id_usuario,
        )
    )

    if participacion is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes acceso a este archivo",
        )

    return registro


def eliminar_archivo(
    db: Session,
    id_proyecto: int,
    id_archivo: int,
    usuario: Usuario,
) -> None:

    verificar_proyecto_editable(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
    )

    registro = db.get(
        Archivo,
        id_archivo,
    )

    if (
        registro is None
        or registro.id_proyecto != id_proyecto
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archivo no encontrado",
        )

    ruta = Path(registro.ruta_archivo)

    try:
        db.delete(registro)
        db.commit()

        if ruta.exists():
            ruta.unlink()

    except Exception:
        db.rollback()
        raise

def obtener_archivo_publico(
    db: Session,
    id_proyecto: int,
    id_archivo: int,
) -> Archivo:

    proyecto = db.get(
        Proyecto,
        id_proyecto,
    )

    if (
        proyecto is None
        or proyecto.estado != EstadoProyecto.PUBLICADO
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado",
        )

    registro = db.get(
        Archivo,
        id_archivo,
    )

    if (
        registro is None
        or registro.id_proyecto != id_proyecto
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archivo no encontrado",
        )

    return registro