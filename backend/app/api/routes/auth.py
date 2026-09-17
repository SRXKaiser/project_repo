from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.auth import (
    LoginRequest,
    RegistroUsuario,
    TokenResponse,
)
from app.schemas.usuario import UsuarioResponse
from app.services.auth_service import (
    autenticar_usuario,
    registrar_usuario,
)


router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
)


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    datos: RegistroUsuario,
    db: Session = Depends(get_db),
):
    return registrar_usuario(db, datos)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    datos: LoginRequest,
    db: Session = Depends(get_db),
):
    _, token = autenticar_usuario(db, datos)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )