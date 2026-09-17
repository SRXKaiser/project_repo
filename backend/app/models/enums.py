from enum import Enum


class TipoUsuario(str, Enum):
    ESTUDIANTE = "ESTUDIANTE"
    DOCENTE = "DOCENTE"
    EGRESADO = "EGRESADO"


class EstadoCuenta(str, Enum):
    ACTIVA = "ACTIVA"
    INACTIVA = "INACTIVA"
    BLOQUEADA = "BLOQUEADA"

class EstadoProyecto(str, Enum):
    BORRADOR = "BORRADOR"
    EN_REVISION = "EN_REVISION"
    REQUIERE_CAMBIOS = "REQUIERE_CAMBIOS"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"
    PUBLICADO = "PUBLICADO"


class TipoParticipacion(str, Enum):
    AUTOR = "AUTOR"
    ASESOR = "ASESOR"
    COLABORADOR = "COLABORADOR"