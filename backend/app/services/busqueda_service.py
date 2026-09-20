from math import ceil

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.area_tematica import AreaTematica
from app.models.enums import EstadoProyecto
from app.models.palabra_clave import PalabraClave
from app.models.proyecto import Proyecto
from app.models.proyecto_area import ProyectoArea
from app.models.proyecto_autor import ProyectoAutor
from app.models.proyecto_palabra_clave import ProyectoPalabraClave
from app.models.usuario import Usuario
from app.schemas.busqueda import BusquedaProyectosResponse


def buscar_proyectos_publicos(
    db: Session,
    q: str | None = None,
    autor: str | None = None,
    palabra_clave: str | None = None,
    id_area: int | None = None,
    id_departamento: int | None = None,
    pagina: int = 1,
    por_pagina: int = 20,
) -> BusquedaProyectosResponse:

    condiciones = [
        Proyecto.estado == EstadoProyecto.PUBLICADO
    ]

    # Texto libre

    if q and q.strip():
        texto = f"%{q.strip()}%"

        condiciones.append(
            or_(
                Proyecto.titulo.ilike(texto),
                Proyecto.resumen.ilike(texto),
            )
        )

    # Departamento

    if id_departamento is not None:
        condiciones.append(
            Proyecto.id_departamento == id_departamento
        )

    # Area tematica

    if id_area is not None:
        subconsulta_area = (
            select(ProyectoArea.id_proyecto)
            .where(
                ProyectoArea.id_area == id_area
            )
        )

        condiciones.append(
            Proyecto.id_proyecto.in_(subconsulta_area)
        )

    # Palabra clave

    if palabra_clave and palabra_clave.strip():
        texto_palabra = (
            f"%{palabra_clave.strip()}%"
        )

        subconsulta_palabra = (
            select(ProyectoPalabraClave.id_proyecto)
            .join(
                PalabraClave,
                PalabraClave.id_palabra_clave
                == ProyectoPalabraClave.id_palabra_clave,
            )
            .where(
                PalabraClave.nombre.ilike(
                    texto_palabra
                )
            )
        )

        condiciones.append(
            Proyecto.id_proyecto.in_(
                subconsulta_palabra
            )
        )

    # Autor / participante

    if autor and autor.strip():
        texto_autor = f"%{autor.strip()}%"

        subconsulta_autor = (
            select(ProyectoAutor.id_proyecto)
            .join(
                Usuario,
                Usuario.id_usuario
                == ProyectoAutor.id_usuario,
            )
            .where(
                or_(
                    Usuario.nombre.ilike(texto_autor),
                    Usuario.apellido_paterno.ilike(
                        texto_autor
                    ),
                    Usuario.apellido_materno.ilike(
                        texto_autor
                    ),
                )
            )
        )

        condiciones.append(
            Proyecto.id_proyecto.in_(
                subconsulta_autor
            )
        )

    # Total de resultados

    total = db.scalar(
        select(func.count(Proyecto.id_proyecto))
        .where(*condiciones)
    ) or 0

    total_paginas = (
        ceil(total / por_pagina)
        if total > 0
        else 0
    )

    offset = (pagina - 1) * por_pagina

    # Consulta paginada

    consulta = (
        select(Proyecto)
        .where(*condiciones)
        .order_by(
            Proyecto.fecha_publicacion.desc(),
            Proyecto.id_proyecto.desc(),
        )
        .offset(offset)
        .limit(por_pagina)
    )

    proyectos = list(
        db.scalars(consulta).all()
    )

    return BusquedaProyectosResponse(
        resultados=proyectos,
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        total_paginas=total_paginas,
    )