
from datetime import datetime, timedelta, timezone
import hashlib
import secrets

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.recuperacion_acceso import RecuperacionAcceso
from app.models.usuario import Usuario


DURACION_TOKEN_MINUTOS = 30


def _hash_token(token: str) -> str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def generar_token_recuperacion(
    db: Session,
    correo: str,
) -> str | None:
    """
    Genera un token temporal de recuperacion.

    El token original debe entregarse exclusivamente
    mediante un canal privadol.

    Esta función NO envia correos.
    """
    correo_normalizado = correo.strip().lower()

    usuario = db.scalar(
        select(Usuario).where(
            Usuario.correo == correo_normalizado
        )
    )

    if usuario is None:
        return None

    ahora = datetime.now(timezone.utc)

    # Invalidar solicitudes anteriores.
    db.execute(
        update(RecuperacionAcceso)
        .where(
            RecuperacionAcceso.id_usuario
            == usuario.id_usuario,
            RecuperacionAcceso.usado.is_(False),
        )
        .values(usado=True)
    )

    token = secrets.token_urlsafe(32)

    recuperacion = RecuperacionAcceso(
        id_usuario=usuario.id_usuario,
        token_hash=_hash_token(token),
        fecha_expiracion=ahora + timedelta(
            minutes=DURACION_TOKEN_MINUTOS
        ),
        usado=False,
    )

    db.add(recuperacion)
    db.commit()

    return token


def restablecer_password(
    db: Session,
    token: str,
    nueva_password: str,
) -> None:
    """
    Valida y consume un token de un solo uso.

    La actualización de la contraseña y el consumo
    del token se realizan en una misma transacción.
    """
    ahora = datetime.now(timezone.utc)

    token_hash = _hash_token(token)

    recuperacion = db.scalar(
        select(RecuperacionAcceso)
        .where(
            RecuperacionAcceso.token_hash == token_hash
        )
        .with_for_update()
    )

    if recuperacion is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado",
        )

    expiracion = recuperacion.fecha_expiracion

    # Compatibilidad defensiva con fechas naive.
    if expiracion.tzinfo is None:
        expiracion = expiracion.replace(
            tzinfo=timezone.utc
        )

    if recuperacion.usado or expiracion <= ahora:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado",
        )

    usuario = db.get(
        Usuario,
        recuperacion.id_usuario,
        with_for_update=True,
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado",
        )

    usuario.password_hash = hash_password(
        nueva_password
    )

    recuperacion.usado = True

    # Invalidar otros tokens del mismo usuario.
    db.execute(
        update(RecuperacionAcceso)
        .where(
            RecuperacionAcceso.id_usuario
            == usuario.id_usuario,
            RecuperacionAcceso.id_recuperacion
            != recuperacion.id_recuperacion,
            RecuperacionAcceso.usado.is_(False),
        )
        .values(usado=True)
    )

    db.commit()
