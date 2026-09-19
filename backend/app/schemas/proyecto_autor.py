from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import TipoParticipacion


class ProyectoAutorCreate(BaseModel):
    id_usuario: int

    tipo_participacion: TipoParticipacion = (
        TipoParticipacion.AUTOR
    )

    orden_autoria: int | None = Field(
        default=None,
        ge=1,
    )


class ProyectoAutorResponse(BaseModel):
    id_proyecto: int
    id_usuario: int
    tipo_participacion: TipoParticipacion
    orden_autoria: int | None

    model_config = ConfigDict(
        from_attributes=True
    )