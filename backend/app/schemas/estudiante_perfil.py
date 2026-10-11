
from pydantic import BaseModel, ConfigDict, Field


class EstudiantePerfilCreate(BaseModel):
    generacion: str | None = Field(
        default=None,
        max_length=30,
    )
    habilidad: str | None = None
    intereses: str | None = None
    imagen_perfil: str | None = None


class EstudiantePerfilUpdate(BaseModel):
    generacion: str | None = Field(
        default=None,
        max_length=30,
    )
    habilidad: str | None = None
    intereses: str | None = None
    imagen_perfil: str | None = None


class EstudiantePerfilResponse(BaseModel):
    id_usuario: int
    generacion: str | None
    habilidad: str | None
    intereses: str | None
    imagen_perfil: str | None

    model_config = ConfigDict(from_attributes=True)
