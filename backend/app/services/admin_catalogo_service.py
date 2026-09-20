from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.area_tematica import AreaTematica
from app.models.carrera import Carrera
from app.models.departamento import Departamento
from app.schemas.admin_catalogo import (
    AreaTematicaCreate,
    AreaTematicaUpdate,
    CarreraCreate,
    CarreraUpdate,
    DepartamentoCreate,
    DepartamentoUpdate,
)


def limpiar_texto(valor: str) -> str:
    return valor.strip()


def limpiar_texto_opcional(
    valor: str | None,
) -> str | None:
    if valor is None:
        return None

    valor = valor.strip()

    return valor or None


# Departamentos

def listar_departamentos(
    db: Session,
) -> list[Departamento]:
    return list(
        db.scalars(
            select(Departamento)
            .order_by(Departamento.nombre)
        ).all()
    )


def crear_departamento(
    db: Session,
    datos: DepartamentoCreate,
) -> Departamento:

    nombre = limpiar_texto(datos.nombre)

    existente = db.scalar(
        select(Departamento).where(
            func.lower(Departamento.nombre)
            == nombre.lower()
        )
    )

    if existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un departamento con ese nombre",
        )

    departamento = Departamento(
        nombre=nombre,
        descripcion=limpiar_texto_opcional(
            datos.descripcion
        ),
    )

    try:
        db.add(departamento)
        db.commit()
        db.refresh(departamento)
        return departamento

    except Exception:
        db.rollback()
        raise


def actualizar_departamento(
    db: Session,
    id_departamento: int,
    datos: DepartamentoUpdate,
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

    cambios = datos.model_dump(exclude_unset=True)

    if "nombre" in cambios:
        nombre = limpiar_texto(cambios["nombre"])

        existente = db.scalar(
            select(Departamento).where(
                func.lower(Departamento.nombre)
                == nombre.lower(),
                Departamento.id_departamento
                != id_departamento,
            )
        )

        if existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un departamento con ese nombre",
            )

        departamento.nombre = nombre

    if "descripcion" in cambios:
        departamento.descripcion = (
            limpiar_texto_opcional(
                cambios["descripcion"]
            )
        )

    try:
        db.commit()
        db.refresh(departamento)
        return departamento

    except Exception:
        db.rollback()
        raise


# Carreras

def listar_carreras(
    db: Session,
) -> list[Carrera]:
    return list(
        db.scalars(
            select(Carrera)
            .order_by(Carrera.nombre)
        ).all()
    )


def verificar_departamento(
    db: Session,
    id_departamento: int,
) -> None:

    if db.get(Departamento, id_departamento) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Departamento no encontrado",
        )


def verificar_carrera_duplicada(
    db: Session,
    nombre: str,
    siglas: str,
    excluir_id: int | None = None,
) -> None:

    condiciones_nombre = [
        func.lower(Carrera.nombre) == nombre.lower()
    ]

    condiciones_siglas = [
        func.lower(Carrera.siglas) == siglas.lower()
    ]

    if excluir_id is not None:
        condiciones_nombre.append(
            Carrera.id_carrera != excluir_id
        )
        condiciones_siglas.append(
            Carrera.id_carrera != excluir_id
        )

    if db.scalar(
        select(Carrera).where(*condiciones_nombre)
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una carrera con ese nombre",
        )

    if db.scalar(
        select(Carrera).where(*condiciones_siglas)
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una carrera con esas siglas",
        )


def crear_carrera(
    db: Session,
    datos: CarreraCreate,
) -> Carrera:

    verificar_departamento(
        db,
        datos.id_departamento,
    )

    nombre = limpiar_texto(datos.nombre)
    siglas = limpiar_texto(datos.siglas).upper()

    verificar_carrera_duplicada(
        db,
        nombre,
        siglas,
    )

    carrera = Carrera(
        nombre=nombre,
        siglas=siglas,
        activa=True,
        id_departamento=datos.id_departamento,
    )

    try:
        db.add(carrera)
        db.commit()
        db.refresh(carrera)
        return carrera

    except Exception:
        db.rollback()
        raise


def actualizar_carrera(
    db: Session,
    id_carrera: int,
    datos: CarreraUpdate,
) -> Carrera:

    carrera = db.get(Carrera, id_carrera)

    if carrera is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrera no encontrada",
        )

    cambios = datos.model_dump(exclude_unset=True)

    nombre = (
        limpiar_texto(cambios["nombre"])
        if "nombre" in cambios
        else carrera.nombre
    )

    siglas = (
        limpiar_texto(cambios["siglas"]).upper()
        if "siglas" in cambios
        else carrera.siglas
    )

    id_departamento = cambios.get(
        "id_departamento",
        carrera.id_departamento,
    )

    verificar_departamento(
        db,
        id_departamento,
    )

    verificar_carrera_duplicada(
        db,
        nombre,
        siglas,
        excluir_id=id_carrera,
    )

    carrera.nombre = nombre
    carrera.siglas = siglas
    carrera.id_departamento = id_departamento

    try:
        db.commit()
        db.refresh(carrera)
        return carrera

    except Exception:
        db.rollback()
        raise


def cambiar_estado_carrera(
    db: Session,
    id_carrera: int,
    activa: bool,
) -> Carrera:

    carrera = db.get(Carrera, id_carrera)

    if carrera is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrera no encontrada",
        )

    carrera.activa = activa

    try:
        db.commit()
        db.refresh(carrera)
        return carrera

    except Exception:
        db.rollback()
        raise


# Areas tematicas

def crear_area(
    db: Session,
    datos: AreaTematicaCreate,
) -> AreaTematica:

    nombre = limpiar_texto(datos.nombre)

    existente = db.scalar(
        select(AreaTematica).where(
            func.lower(AreaTematica.nombre)
            == nombre.lower()
        )
    )

    if existente is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un área temática con ese nombre",
        )

    area = AreaTematica(
        nombre=nombre,
        descripcion=limpiar_texto_opcional(
            datos.descripcion
        ),
    )

    try:
        db.add(area)
        db.commit()
        db.refresh(area)
        return area

    except Exception:
        db.rollback()
        raise


def actualizar_area(
    db: Session,
    id_area: int,
    datos: AreaTematicaUpdate,
) -> AreaTematica:

    area = db.get(AreaTematica, id_area)

    if area is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Área temática no encontrada",
        )

    cambios = datos.model_dump(exclude_unset=True)

    if "nombre" in cambios:
        nombre = limpiar_texto(cambios["nombre"])

        existente = db.scalar(
            select(AreaTematica).where(
                func.lower(AreaTematica.nombre)
                == nombre.lower(),
                AreaTematica.id_area != id_area,
            )
        )

        if existente is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un área temática con ese nombre",
            )

        area.nombre = nombre

    if "descripcion" in cambios:
        area.descripcion = limpiar_texto_opcional(
            cambios["descripcion"]
        )

    try:
        db.commit()
        db.refresh(area)
        return area

    except Exception:
        db.rollback()
        raise