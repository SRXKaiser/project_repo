from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.carrera import Carrera
from app.models.departamento import Departamento
from app.models.docente import Docente
from app.models.egresado import Egresado
from app.models.enums import EstadoCuenta, TipoUsuario
from app.models.estudiante import Estudiante
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, RegistroUsuario


def registrar_usuario(
    db: Session,
    datos: RegistroUsuario,
) -> Usuario:

    # Normalizamos el correo para evitar cosas como:
    # Usuario@correo.com y usuario@correo.com
    correo = datos.correo.lower().strip()

    usuario_existente = db.scalar(
        select(Usuario).where(Usuario.correo == correo)
    )

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese correo",
        )

    # Validaciones según tipo de usuario
    if datos.tipo_usuario == TipoUsuario.ESTUDIANTE:

        if not datos.num_control or datos.id_carrera is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El estudiante requiere num_control e id_carrera",
            )

        carrera = db.get(Carrera, datos.id_carrera)

        if carrera is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La carrera especificada no existe",
            )

        num_control_existente = db.scalar(
            select(Estudiante).where(
                Estudiante.num_control == datos.num_control
            )
        )

        if num_control_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un estudiante con ese número de control",
            )

    elif datos.tipo_usuario == TipoUsuario.DOCENTE:

        if not datos.num_empleado or datos.id_departamento is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El docente requiere num_empleado e id_departamento",
            )

        departamento = db.get(
            Departamento,
            datos.id_departamento,
        )

        if departamento is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El departamento especificado no existe",
            )

        empleado_existente = db.scalar(
            select(Docente).where(
                Docente.num_empleado == datos.num_empleado
            )
        )

        if empleado_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un docente con ese número de empleado",
            )

    elif datos.tipo_usuario == TipoUsuario.EGRESADO:

        if (
            not datos.num_control
            or datos.id_carrera is None
            or datos.anio_egreso is None
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "El egresado requiere num_control, "
                    "id_carrera y anio_egreso"
                ),
            )

        carrera = db.get(Carrera, datos.id_carrera)

        if carrera is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La carrera especificada no existe",
            )

        egresado_existente = db.scalar(
            select(Egresado).where(
                Egresado.num_control == datos.num_control
            )
        )

        if egresado_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un egresado con ese número de control",
            )

    # Crear usuario base
    usuario = Usuario(
        nombre=datos.nombre.strip(),
        apellido_paterno=datos.apellido_paterno.strip(),
        apellido_materno=(
            datos.apellido_materno.strip()
            if datos.apellido_materno
            else None
        ),
        correo=correo,
        password_hash=hash_password(datos.password),
        tipo_usuario=datos.tipo_usuario,
        estado_cuenta=EstadoCuenta.ACTIVA,
    )

    try:
        db.add(usuario)

        # Necesitamos el ID antes de crear el perfil.
        db.flush()

        if datos.tipo_usuario == TipoUsuario.ESTUDIANTE:

            perfil = Estudiante(
                id_usuario=usuario.id_usuario,
                num_control=datos.num_control,
                id_carrera=datos.id_carrera,
                semestre=datos.semestre,
            )

        elif datos.tipo_usuario == TipoUsuario.DOCENTE:

            perfil = Docente(
                id_usuario=usuario.id_usuario,
                num_empleado=datos.num_empleado,
                id_departamento=datos.id_departamento,
            )

        else:

            perfil = Egresado(
                id_usuario=usuario.id_usuario,
                num_control=datos.num_control,
                id_carrera=datos.id_carrera,
                anio_egreso=datos.anio_egreso,
            )

        db.add(perfil)

        db.commit()
        db.refresh(usuario)

        return usuario

    except Exception:
        db.rollback()
        raise


def autenticar_usuario(
    db: Session,
    datos: LoginRequest,
) -> tuple[Usuario, str]:

    correo = datos.correo.lower().strip()

    usuario = db.scalar(
        select(Usuario).where(Usuario.correo == correo)
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
        )

    if not verify_password(
        datos.password,
        usuario.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
        )

    if usuario.estado_cuenta != EstadoCuenta.ACTIVA:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta no está activa",
        )

    usuario.ultimo_acceso = datetime.now(timezone.utc)

    token = create_access_token(usuario.id_usuario)

    db.commit()

    return usuario, token