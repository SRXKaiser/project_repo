from pydantic import BaseModel

from app.schemas.proyecto import ProyectoResponse


class BusquedaProyectosResponse(BaseModel):
    resultados: list[ProyectoResponse]

    total: int
    pagina: int
    por_pagina: int
    total_paginas: int