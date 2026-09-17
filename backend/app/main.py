from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine

from app.api.routes.auth import router as auth_router
from app.api.routes.usuarios import router as usuarios_router
app = FastAPI(
    title="Project Repository API",
    description="API para el repositorio de proyectos de investigación del ITCJ",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(usuarios_router)

@app.get("/")
def root():
    return {
        "message": "Project Repository API",
        "status": "ok"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/health/database")
def database_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "database": "connected"
    }