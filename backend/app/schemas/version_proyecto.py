
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VersionProyectoCreate(BaseModel):
    id_proyecto: int = Field(gt=0)
    numero_version: int = Field(gt=0)
    ruta_pdf: str = Field(min_length=1)
    tamano_bytes: int = Field(ge=0)


class VersionProyectoResponse(BaseModel):
    id_version: int
    id_proyecto: int
    numero_version: int
    ruta_pdf: str
    tamano_bytes: int
    fecha_subida: datetime

    model_config = ConfigDict(from_attributes=True)
