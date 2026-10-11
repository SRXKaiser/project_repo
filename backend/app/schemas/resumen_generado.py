
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


EstadoEnvioResumen = Literal[
    "PENDIENTE",
    "ENVIADO",
    "FALLIDO",
]


class ResumenGeneradoCreate(BaseModel):
    id_proyecto: int = Field(gt=0)
    id_version: int | None = Field(default=None, gt=0)
    contenido: str = Field(min_length=1)
    correo_destino: EmailStr | None = None


class ResumenGeneradoUpdate(BaseModel):
    estado_envio: EstadoEnvioResumen


class ResumenGeneradoResponse(BaseModel):
    id_resumen: int
    id_proyecto: int
    id_version: int | None
    contenido: str
    correo_destino: str | None
    fecha_generacion: datetime
    estado_envio: str

    model_config = ConfigDict(from_attributes=True)
