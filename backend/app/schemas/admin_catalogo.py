from pydantic import BaseModel, ConfigDict, Field


# Departamentos

class DepartamentoCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    descripcion: str | None = Field(
        default=None,
        max_length=500,
    )


class DepartamentoUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )
    descripcion: str | None = Field(
        default=None,
        max_length=500,
    )


class DepartamentoResponse(BaseModel):
    id_departamento: int
    nombre: str
    descripcion: str | None

    model_config = ConfigDict(from_attributes=True)


# Carreras

class CarreraCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    siglas: str = Field(min_length=1, max_length=20)
    id_departamento: int


class CarreraUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )
    siglas: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )
    id_departamento: int | None = None


class CarreraEstadoRequest(BaseModel):
    activa: bool


class CarreraResponse(BaseModel):
    id_carrera: int
    nombre: str
    siglas: str
    activa: bool
    id_departamento: int

    model_config = ConfigDict(from_attributes=True)


# Areas tematicas


class AreaTematicaCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    descripcion: str | None = Field(
        default=None,
        max_length=500,
    )


class AreaTematicaUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )
    descripcion: str | None = Field(
        default=None,
        max_length=500,
    )