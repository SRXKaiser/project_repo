from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.usuario import Usuario
from app.schemas.archivo import ArchivoResponse
from app.services.archivo_service import (
    eliminar_archivo,
    listar_archivos_proyecto,
    obtener_archivo,
    obtener_archivo_publico,
    obtener_ruta_segura,
    subir_archivo,
)


router = APIRouter(
    prefix="/proyectos",
    tags=["Archivos de proyectos"],
)


@router.get(
    "/{id_proyecto}/archivos",
    response_model=list[ArchivoResponse],
)
def listar(
    id_proyecto: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return listar_archivos_proyecto(
        db=db,
        id_proyecto=id_proyecto,
        usuario=usuario,
    )


@router.post(
    "/{id_proyecto}/archivos",
    response_model=ArchivoResponse,
    status_code=status.HTTP_201_CREATED,
)
def subir(
    id_proyecto: int,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return subir_archivo(
        db=db,
        id_proyecto=id_proyecto,
        archivo=archivo,
        usuario=usuario,
    )


@router.get(
    "/{id_proyecto}/archivos/{id_archivo}/descargar",
)
def descargar(
    id_proyecto: int,
    id_archivo: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    registro = obtener_archivo(
        db=db,
        id_archivo=id_archivo,
        usuario=usuario,
    )

    if registro.id_proyecto != id_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archivo no encontrado",
        )

    ruta = obtener_ruta_segura(
        registro.ruta_archivo
    )

    if not ruta.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El archivo físico no está disponible",
        )

    return FileResponse(
        path=ruta,
        media_type=registro.tipo_mime,
        filename=registro.nombre_original,
    )


@router.delete(
    "/{id_proyecto}/archivos/{id_archivo}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar(
    id_proyecto: int,
    id_archivo: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    eliminar_archivo(
        db=db,
        id_proyecto=id_proyecto,
        id_archivo=id_archivo,
        usuario=usuario,
    )


@router.get(
    "/{id_proyecto}/archivos/{id_archivo}/publico",
)
def descargar_publico(
    id_proyecto: int,
    id_archivo: int,
    db: Session = Depends(get_db),
):
    registro = obtener_archivo_publico(
        db=db,
        id_proyecto=id_proyecto,
        id_archivo=id_archivo,
    )

    ruta = obtener_ruta_segura(
        registro.ruta_archivo
    )

    if not ruta.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El archivo físico no está disponible",
        )

    return FileResponse(
        path=ruta,
        media_type=registro.tipo_mime,
        filename=registro.nombre_original,
    )