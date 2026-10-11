from app.models.departamento import Departamento
from app.models.carrera import Carrera
from app.models.usuario import Usuario
from app.models.estudiante import Estudiante
from app.models.docente import Docente
from app.models.egresado import Egresado
from app.models.rol import Rol
from app.models.usuario_rol import UsuarioRol
from app.models.responsable_departamento import ResponsableDepartamento
from app.models.proyecto import Proyecto
from app.models.proyecto_autor import ProyectoAutor
from app.models.area_tematica import AreaTematica
from app.models.proyecto_area import ProyectoArea
from app.models.palabra_clave import PalabraClave
from app.models.proyecto_palabra_clave import ProyectoPalabraClave
from app.models.archivo import Archivo
from app.models.historial_estado import HistorialEstado
from app.models.recuperacion_acceso import RecuperacionAcceso
from app.models.notificacion import Notificacion
from app.models.estudiante_perfil import EstudiantePerfil
from app.models.version_proyecto import VersionProyecto
from app.models.resumen_generado import ResumenGenerado


__all__ = [
    "Departamento",
    "Carrera",
    "Usuario",
    "Estudiante",
    "Docente",
    "Egresado",
    "Rol",
    "UsuarioRol",
    "ResponsableDepartamento",
    "Proyecto",
    "ProyectoAutor",
    "AreaTematica",
    "ProyectoArea",
    "PalabraClave",
    "ProyectoPalabraClave",
    "Archivo",
    "HistorialEstado",
    "RecuperacionAcceso",
    "Notificacion",
    "EstudiantePerfil",
    "VersionProyecto",
    "ResumenGenerado"
]