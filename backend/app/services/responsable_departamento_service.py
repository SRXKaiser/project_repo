from datetime import date

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.departamento import Departamento
from app.models.docente import Docente
from app.models.enums import EstadoCuenta, TipoUsuario
from app.models.responsable_departamento import ResponsableDepartamento
from app.models.usuario import Usuario
from app.schemas.responsable_departamento import (
    ResponsableDetalleResponse,
)


def verificar_departamento(
    db: Session,
    id_departamento: int,
) -> Departamento:

    departamento = db.get(
        Departamento,
        id_departamento,
    )

    if departamento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Departamento no encontrado",
        )

    return departamento


def verificar_docente_departamento(
    db: Session,
    id_usuario_docente: int,
    id_departamento: int,
) -> tuple[Usuario, Docente]:

    usuario = db.get(
        Usuario,
        id_usuario_docente,
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    if usuario.tipo_usuario != TipoUsuario.DOCENTE:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "El responsable del departamento "
                "debe ser un docente"
            ),
        )

    if usuario.estado_cuenta != EstadoCuenta.ACTIVA:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "El docente debe tener una "
                "cuenta activa"
            ),
        )

    docente = db.get(
        Docente,
        id_usuario_docente,
    )

    if docente is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "El usuario no tiene un perfil "
                "de docente válido"
            ),
        )

    if docente.id_departamento != id_departamento:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "El docente no pertenece "
                "al departamento indicado"
            ),
        )

    return usuario, docente


def obtener_responsable_activo(
    db: Session,
    id_departamento: int,
) -> ResponsableDepartamento | None:

    return db.scalar(
        select(ResponsableDepartamento).where(
            ResponsableDepartamento.id_departamento
            == id_departamento,
            ResponsableDepartamento.activo.is_(True),
        )
    )


def asignar_responsable(
    db: Session,
    id_departamento: int,
    id_usuario_docente: int,
) -> ResponsableDepartamento:

    verificar_departamento(
        db=db,
        id_departamento=id_departamento,
    )

    verificar_docente_departamento(
        db=db,
        id_usuario_docente=id_usuario_docente,
        id_departamento=id_departamento,
    )

    responsable_actual = obtener_responsable_activo(
        db=db,
        id_departamento=id_departamento,
    )

    if (
        responsable_actual is not None
        and responsable_actual.id_usuario_docente
        == id_usuario_docente
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "El docente ya es el responsable "
                "activo de este departamento"
            ),
        )

    hoy = date.today()

    try:
        # Cerramos el nombramiento anterior,
        # pero NO lo eliminamos.
        if responsable_actual is not None:
            responsable_actual.activo = False
            responsable_actual.fecha_fin = hoy

        nuevo_responsable = ResponsableDepartamento(
            id_departamento=id_departamento,
            id_usuario_docente=id_usuario_docente,
            fecha_inicio=hoy,
            fecha_fin=None,
            activo=True,
        )

        db.add(nuevo_responsable)

        db.commit()
        db.refresh(nuevo_responsable)

        return nuevo_responsable

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "No se pudo asignar el responsable porque "
                "el departamento ya tiene un responsable activo"
            ),
        )

    except Exception:
        db.rollback()
        raise


def retirar_responsable(
    db: Session,
    id_departamento: int,
) -> ResponsableDepartamento:

    verificar_departamento(
        db=db,
        id_departamento=id_departamento,
    )

    responsable = obtener_responsable_activo(
        db=db,
        id_departamento=id_departamento,
    )

    if responsable is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "El departamento no tiene "
                "un responsable activo"
            ),
        )

    try:
        responsable.activo = False
        responsable.fecha_fin = date.today()

        db.commit()
        db.refresh(responsable)

        return responsable

    except Exception:
        db.rollback()
        raise


def construir_detalle(
    db: Session,
    responsable: ResponsableDepartamento,
) -> ResponsableDetalleResponse:

    departamento = db.get(
        Departamento,
        responsable.id_departamento,
    )

    usuario = db.get(
        Usuario,
        responsable.id_usuario_docente,
    )

    return ResponsableDetalleResponse(
        id_responsable=responsable.id_responsable,
        id_departamento=responsable.id_departamento,
        departamento=departamento.nombre,
        id_usuario_docente=responsable.id_usuario_docente,
        nombre=usuario.nombre,
        apellido_paterno=usuario.apellido_paterno,
        apellido_materno=usuario.apellido_materno,
        correo=usuario.correo,
        fecha_inicio=responsable.fecha_inicio,
        fecha_fin=responsable.fecha_fin,
        activo=responsable.activo,
    )


def listar_responsables_activos(
    db: Session,
) -> list[ResponsableDetalleResponse]:

    responsables = list(
        db.scalars(
            select(ResponsableDepartamento)
            .where(
                ResponsableDepartamento.activo.is_(True)
            )
            .order_by(
                ResponsableDepartamento.id_departamento
            )
        ).all()
    )

    return [
        construir_detalle(
            db=db,
            responsable=responsable,
        )
        for responsable in responsables
    ]


def obtener_responsable_departamento(
    db: Session,
    id_departamento: int,
) -> ResponsableDetalleResponse:

    verificar_departamento(
        db=db,
        id_departamento=id_departamento,
    )

    responsable = obtener_responsable_activo(
        db=db,
        id_departamento=id_departamento,
    )

    if responsable is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "El departamento no tiene "
                "un responsable activo"
            ),
        )

    return construir_detalle(
        db=db,
        responsable=responsable,
    )