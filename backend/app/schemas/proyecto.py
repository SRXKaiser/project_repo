from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import EstadoProyecto
from app.schemas.archivo import ArchivoResponse
from app.schemas.area_tematica import AreaTematicaResponse
from app.schemas.palabra_clave import PalabraClaveResponse



class ProyectoCreate(BaseModel):
    titulo: str = Field(
        min_length=3,
        max_length=300
    )

    resumen: str = Field(
        min_length=10
    )

    id_departamento: int

class ProyectoUpdate(BaseModel):
    titulo: str | None = Field(
        default=None,
        min_length=3,
        max_length=300,
    )

    resumen: str | None = Field(
        default=None,
        min_length=10,
    )

    id_departamento: int | None = None

class ProyectoResponse(BaseModel):
    id_proyecto: int
    titulo: str
    resumen: str

    fecha_creacion: datetime
    fecha_publicacion: datetime | None

    estado: EstadoProyecto

    id_departamento: int
    creado_por: int

    model_config = ConfigDict(
        from_attributes=True
    )

class AutorProyectoResponse(BaseModel):
    id_usuario: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None
    tipo_participacion: str
    orden_autoria: int | None


class ProyectoDetalleResponse(ProyectoResponse):
    areas_tematicas: list[AreaTematicaResponse]
    palabras_clave: list[PalabraClaveResponse]
    autores: list[AutorProyectoResponse]
    archivos: list[ArchivoResponse]