
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RecuperacionAccesoSolicitud(BaseModel):
    correo: EmailStr


class RecuperacionAccesoConfirmacion(BaseModel):
    token: str = Field(min_length=16)
    nueva_password: str = Field(
        min_length=8,
        max_length=128,
    )


class RecuperacionAccesoResponse(BaseModel):
    id_recuperacion: int
    id_usuario: int
    fecha_expiracion: datetime
    usado: bool

    model_config = ConfigDict(from_attributes=True)


class RecuperacionAccesoMensaje(BaseModel):
    mensaje: str
