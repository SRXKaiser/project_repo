from pydantic import BaseModel, ConfigDict


class AreaTematicaResponse(BaseModel):
    id_area: int
    nombre: str
    descripcion: str | None

    model_config = ConfigDict(
        from_attributes=True
    )