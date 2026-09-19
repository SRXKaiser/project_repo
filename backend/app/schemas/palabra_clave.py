from pydantic import BaseModel, ConfigDict, Field


class PalabraClaveCreate(BaseModel):
    nombre: str = Field(
        min_length=2,
        max_length=100,
    )


class PalabraClaveResponse(BaseModel):
    id_palabra_clave: int
    nombre: str

    model_config = ConfigDict(
        from_attributes=True
    )