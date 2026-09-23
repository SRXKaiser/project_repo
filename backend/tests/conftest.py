import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)

import app.models  # noqa: F401
from app.db.base import Base
from app.db.database import get_db
from app.main import app
from app.models.area_tematica import AreaTematica
from app.models.carrera import Carrera
from app.models.departamento import Departamento


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL"
)


if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL no está definida. "
        "Configura una base PostgreSQL exclusiva "
        "para pruebas antes de ejecutar pytest."
    )


database_name = (
    TEST_DATABASE_URL
    .split("/")[-1]
    .split("?")[0]
    .lower()
)

if "test" not in database_name:
    raise RuntimeError(
        "TEST_DATABASE_URL debe apuntar a una "
        "base de datos cuyo nombre contenga 'test'. "
        "Esto evita borrar accidentalmente la "
        "base de desarrollo."
    )


test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(
        bind=test_engine
    )

    Base.metadata.create_all(
        bind=test_engine
    )

    yield


@pytest.fixture
def db() -> Session:
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def catalogos(db: Session):
    departamento = Departamento(
        nombre="Sistemas y Computación",
        descripcion=(
            "Departamento para pruebas automatizadas"
        ),
    )

    db.add(departamento)
    db.flush()

    carrera = Carrera(
        nombre=(
            "Ingeniería en Sistemas Computacionales"
        ),
        siglas="ISC",
        activa=True,
        id_departamento=(
            departamento.id_departamento
        ),
    )

    area = AreaTematica(
        nombre="Desarrollo de Software",
        descripcion=(
            "Área temática para pruebas"
        ),
    )

    db.add_all([
        carrera,
        area,
    ])

    db.commit()

    db.refresh(departamento)
    db.refresh(carrera)
    db.refresh(area)

    return {
        "departamento": departamento,
        "carrera": carrera,
        "area": area,
    }


@pytest.fixture
def estudiante_payload(catalogos):
    return {
        "nombre": "Usuario",
        "apellido_paterno": "Prueba",
        "apellido_materno": "Automatica",
        "correo": "estudiante@example.com",
        "password": "Password123!",
        "tipo_usuario": "ESTUDIANTE",
        "num_control": "TEST000001",
        "id_carrera": (
            catalogos["carrera"].id_carrera
        ),
        "semestre": 8,
    }


@pytest.fixture
def usuario_registrado(
    client,
    estudiante_payload,
):
    response = client.post(
        "/auth/register",
        json=estudiante_payload,
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def auth_headers(
    client,
    estudiante_payload,
    usuario_registrado,
):
    response = client.post(
        "/auth/login",
        json={
            "correo": (
                estudiante_payload["correo"]
            ),
            "password": (
                estudiante_payload["password"]
            ),
        },
    )

    assert response.status_code == 200

    token = response.json()[
        "access_token"
    ]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def proyecto_creado(
    client,
    auth_headers,
    catalogos,
):
    response = client.post(
        "/proyectos",
        headers=auth_headers,
        json={
            "titulo": (
                "Proyecto automatizado de prueba"
            ),
            "resumen": (
                "Este es un resumen suficientemente "
                "largo para el proyecto de prueba."
            ),
            "id_departamento": (
                catalogos[
                    "departamento"
                ].id_departamento
            ),
        },
    )

    assert response.status_code == 201

    return response.json()