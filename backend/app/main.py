from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.routes.admin_catalogos import (
    router as admin_catalogos_router,
)
from app.api.routes.admin_responsables import (
    router as admin_responsables_router,
)
from app.api.routes.admin_usuarios import (
    router as admin_usuarios_router,
)
from app.api.routes.archivos import router as archivos_router
from app.api.routes.areas_tematicas import (
    router as areas_tematicas_router,
)
from app.api.routes.auth import router as auth_router
from app.api.routes.carreras import router as carreras_router
from app.api.routes.departamentos import (
    router as departamentos_router,
)
from app.api.routes.palabras_clave import (
    router as palabras_clave_router,
)
from app.api.routes.proyecto_autores import (
    router as proyecto_autores_router,
)
from app.api.routes.proyectos import router as proyectos_router
from app.api.routes.usuarios import router as usuarios_router
from app.api.routes.workflow import router as workflow_router
from app.core.config import settings
from app.db.database import engine


app = FastAPI(
    title="Project Repository API",
    description=(
        "API para el repositorio de proyectos "
        "de investigación del ITCJ"
    ),
    version="0.1.0",
)


origins = [
    origin.strip()
    for origin in settings.cors_origins.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rutas públicas y autenticación
app.include_router(auth_router)
app.include_router(carreras_router)
app.include_router(departamentos_router)
app.include_router(areas_tematicas_router)
app.include_router(palabras_clave_router)

# Usuarios y proyectos
app.include_router(usuarios_router)
app.include_router(proyectos_router)
app.include_router(proyecto_autores_router)
app.include_router(archivos_router)
app.include_router(workflow_router)

# Administración
app.include_router(admin_usuarios_router)
app.include_router(admin_responsables_router)
app.include_router(admin_catalogos_router)


@app.get("/")
def root():
    return {
        "message": "Project Repository API",
        "status": "ok",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.get("/health/database")
def database_health():
    with engine.connect() as connection:
        connection.execute(
            text("SELECT 1")
        )

    return {
        "database": "connected",
    }