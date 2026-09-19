from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import EstadoProyecto


class CambioEstadoRequest(BaseModel):
    comentario: str | None = Field(
        default=None,
        max_length=2000,
    )


class HistorialEstadoResponse(BaseModel):
    id_historial: int
    id_proyecto: int
    estado_anterior: EstadoProyecto | None
    estado_nuevo: EstadoProyecto
    cambiado_por: int
    fecha_cambio: datetime
    comentario: str | None

    model_config = ConfigDict(
        from_attributes=True
    )