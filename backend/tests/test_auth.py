def test_registrar_estudiante(
    client,
    estudiante_payload,
):
    response = client.post(
        "/auth/register",
        json=estudiante_payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert (
        data["correo"]
        == estudiante_payload["correo"]
    )

    assert (
        data["tipo_usuario"]
        == "ESTUDIANTE"
    )

    assert "password" not in data
    assert "password_hash" not in data


def test_correo_duplicado_retorna_409(
    client,
    estudiante_payload,
):
    first = client.post(
        "/auth/register",
        json=estudiante_payload,
    )

    assert first.status_code == 201

    second = client.post(
        "/auth/register",
        json=estudiante_payload,
    )

    assert second.status_code == 409


def test_login_correcto(
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

    data = response.json()

    assert data["token_type"] == "bearer"
    assert isinstance(
        data["access_token"],
        str,
    )
    assert data["access_token"]


def test_login_password_incorrecto(
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
            "password": "PasswordIncorrecto123!",
        },
    )

    assert response.status_code == 401


def test_password_demasiado_corto(
    client,
    estudiante_payload,
):
    payload = estudiante_payload.copy()

    payload["password"] = "123"

    response = client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 422


def test_estudiante_requiere_carrera(
    client,
    estudiante_payload,
):
    payload = estudiante_payload.copy()

    payload["id_carrera"] = None

    response = client.post(
        "/auth/register",
        json=payload,
    )

    assert response.status_code == 400

def test_registrar_estudiante(
    client,
    estudiante_payload,
):
    response = client.post(
        "/auth/register",
        json=estudiante_payload,
    )

    print("\nPAYLOAD:")
    print(estudiante_payload)

    print("\nRESPUESTA:")
    print(response.status_code)
    print(response.json())

    assert response.status_code == 201

    data = response.json()

    assert (
        data["correo"]
        == estudiante_payload["correo"]
    )

    assert (
        data["tipo_usuario"]
        == "ESTUDIANTE"
    )

    assert "password" not in data
    assert "password_hash" not in data