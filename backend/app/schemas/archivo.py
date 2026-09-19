from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ArchivoResponse(BaseModel):
    id_archivo: int
    id_proyecto: int
    nombre_original: str
    tipo_mime: str
    tamanio: int
    fecha_subida: datetime
    subido_por: int

    model_config = ConfigDict(
        from_attributes=True
    )