from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)


@router.get(
    "/me",
    response_model=UsuarioResponse,
)
def obtener_mi_usuario(
    usuario: Usuario = Depends(get_current_user),
):
    return usuario