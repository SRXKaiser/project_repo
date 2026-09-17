from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import EstadoCuenta, TipoUsuario


class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None
    correo: EmailStr
    tipo_usuario: TipoUsuario
    estado_cuenta: EstadoCuenta
    fecha_registro: datetime
    ultimo_acceso: datetime | None

    model_config = ConfigDict(from_attributes=True)