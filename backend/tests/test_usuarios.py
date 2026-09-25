from datetime import date

from app.models.docente import Docente
from app.models.responsable_departamento import ResponsableDepartamento
from app.models.rol import Rol
from app.models.usuario_rol import UsuarioRol
from app.models.enums import EstadoCuenta, TipoUsuario
from app.models.usuario import Usuario
from app.core.security import hash_password


def test_buscar_usuario_autenticado(
    client,
    db,
    auth_headers,
):
    usuario = Usuario(
        nombre="Laura",
        apellido_paterno="Ramirez",
        apellido_materno="Lopez",
        correo="laura@example.com",
        password_hash=hash_password(
            "Password123!"
        ),
        tipo_usuario=TipoUsuario.DOCENTE,
        estado_cuenta=EstadoCuenta.ACTIVA,
    )

    db.add(usuario)
    db.commit()

    response = client.get(
        "/usuarios/buscar",
        params={"q": "Laura"},
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["nombre"] == "Laura"
    assert data[0]["apellido_paterno"] == "Ramirez"
    assert data[0]["tipo_usuario"] == "DOCENTE"

    # El endpoint no debe exponer información
    # innecesaria para seleccionar participantes.
    assert "correo" not in data[0]
    assert "password_hash" not in data[0]
    assert "estado_cuenta" not in data[0]
    assert "ultimo_acceso" not in data[0]


def test_buscar_usuario_por_apellido(
    client,
    db,
    auth_headers,
):
    usuario = Usuario(
        nombre="Carlos",
        apellido_paterno="Mendoza",
        apellido_materno=None,
        correo="carlos@example.com",
        password_hash=hash_password(
            "Password123!"
        ),
        tipo_usuario=TipoUsuario.DOCENTE,
        estado_cuenta=EstadoCuenta.ACTIVA,
    )

    db.add(usuario)
    db.commit()

    response = client.get(
        "/usuarios/buscar",
        params={"q": "mendoza"},
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["nombre"] == "Carlos"


def test_busqueda_no_devuelve_usuario_inactivo(
    client,
    db,
    auth_headers,
):
    usuario = Usuario(
        nombre="Usuario",
        apellido_paterno="Inactivo",
        apellido_materno=None,
        correo="inactivo@example.com",
        password_hash=hash_password(
            "Password123!"
        ),
        tipo_usuario=TipoUsuario.DOCENTE,
        estado_cuenta=EstadoCuenta.INACTIVA,
    )

    db.add(usuario)
    db.commit()

    response = client.get(
        "/usuarios/buscar",
        params={"q": "Inactivo"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json() == []


def test_buscar_usuario_requiere_autenticacion(
    client,
):
    response = client.get(
        "/usuarios/buscar",
        params={"q": "Laura"},
    )

    assert response.status_code == 401


def test_buscar_usuario_requiere_dos_caracteres(
    client,
    auth_headers,
):
    response = client.get(
        "/usuarios/buscar",
        params={"q": "L"},
        headers=auth_headers,
    )

    assert response.status_code == 422

def test_me_usuario_normal_sin_permisos_especiales(
    client,
    auth_headers,
):
    response = client.get(
        "/usuarios/me",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["tipo_usuario"] == "ESTUDIANTE"
    assert data["es_administrador"] is False
    assert data["departamentos_responsable"] == []


def test_me_detecta_administrador(
    client,
    db,
    auth_headers,
    usuario_registrado,
):
    rol = Rol(
        nombre="ADMINISTRADOR",
        descripcion="Administrador de prueba",
    )

    db.add(rol)
    db.flush()

    usuario_rol = UsuarioRol(
        id_usuario=usuario_registrado["id_usuario"],
        id_rol=rol.id_rol,
    )

    db.add(usuario_rol)
    db.commit()

    response = client.get(
        "/usuarios/me",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["es_administrador"] is True
    assert data["departamentos_responsable"] == []


def test_me_detecta_responsable_departamento(
    client,
    db,
    catalogos,
):
    docente = Usuario(
        nombre="Laura",
        apellido_paterno="Ramirez",
        apellido_materno="Lopez",
        correo="responsable@example.com",
        password_hash=hash_password(
            "Password123!"
        ),
        tipo_usuario=TipoUsuario.DOCENTE,
        estado_cuenta=EstadoCuenta.ACTIVA,
    )

    db.add(docente)
    db.flush()

    perfil_docente = Docente(
        id_usuario=docente.id_usuario,
        num_empleado="DOC-TEST-001",
        id_departamento=(
            catalogos["departamento"].id_departamento
        ),
    )

    responsable = ResponsableDepartamento(
        id_departamento=(
            catalogos["departamento"].id_departamento
        ),
        id_usuario_docente=docente.id_usuario,
        fecha_inicio=date.today(),
        fecha_fin=None,
        activo=True,
    )

    db.add_all([
        perfil_docente,
        responsable,
    ])
    db.commit()

    login = client.post(
        "/auth/login",
        json={
            "correo": "responsable@example.com",
            "password": "Password123!",
        },
    )

    assert login.status_code == 200

    headers = {
        "Authorization": (
            f"Bearer {login.json()['access_token']}"
        )
    }

    response = client.get(
        "/usuarios/me",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["tipo_usuario"] == "DOCENTE"
    assert data["es_administrador"] is False
    assert data["departamentos_responsable"] == [
        catalogos["departamento"].id_departamento
    ]