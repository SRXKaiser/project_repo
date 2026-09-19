from datetime import date

from pydantic import BaseModel, ConfigDict


class AsignarResponsableRequest(BaseModel):
    id_usuario_docente: int


class ResponsableDepartamentoResponse(BaseModel):
    id_responsable: int
    id_departamento: int
    id_usuario_docente: int
    fecha_inicio: date
    fecha_fin: date | None
    activo: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class ResponsableDetalleResponse(BaseModel):
    id_responsable: int
    id_departamento: int
    departamento: str

    id_usuario_docente: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None
    correo: str

    fecha_inicio: date
    fecha_fin: date | None
    activo: bool