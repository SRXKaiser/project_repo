
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


EstadoEnvio = Literal[
    "PENDIENTE",
    "ENVIADO",
    "FALLIDO",
]


class NotificacionCreate(BaseModel):
    id_usuario: int = Field(gt=0)
    id_proyecto: int | None = Field(default=None, gt=0)
    tipo: str = Field(min_length=1, max_length=60)
    mensaje: str = Field(min_length=1)


class NotificacionUpdate(BaseModel):
    estado_envio: EstadoEnvio


class NotificacionResponse(BaseModel):
    id_notificacion: int
    id_usuario: int
    id_proyecto: int | None
    tipo: str
    mensaje: str
    fecha_envio: datetime
    estado_envio: str

    model_config = ConfigDict(from_attributes=True)
