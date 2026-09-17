from pydantic import BaseModel, EmailStr, Field

from app.models.enums import TipoUsuario


class RegistroUsuario(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    apellido_paterno: str = Field(min_length=2, max_length=100)
    apellido_materno: str | None = Field(default=None, max_length=100)

    correo: EmailStr

    password: str = Field(min_length=8, max_length=128)

    tipo_usuario: TipoUsuario

    # Estudiante / egresado
    num_control: str | None = Field(default=None, max_length=20)
    id_carrera: int | None = None
    semestre: int | None = Field(default=None, ge=1)

    # Docente
    num_empleado: str | None = Field(default=None, max_length=30)
    id_departamento: int | None = None

    # Egresado
    anio_egreso: int | None = None


class LoginRequest(BaseModel):
    correo: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"