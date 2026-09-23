def crear_segundo_usuario(
    client,
    catalogos,
):
    payload = {
        "nombre": "Segundo",
        "apellido_paterno": "Usuario",
        "apellido_materno": "Prueba",
        "correo": "segundo@example.com",
        "password": "Password456!",
        "tipo_usuario": "ESTUDIANTE",
        "num_control": "TEST000002",
        "id_carrera": (
            catalogos["carrera"].id_carrera
        ),
        "semestre": 7,
    }

    register = client.post(
        "/auth/register",
        json=payload,
    )

    assert register.status_code == 201

    login = client.post(
        "/auth/login",
        json={
            "correo": payload["correo"],
            "password": payload["password"],
        },
    )

    assert login.status_code == 200

    return {
        "Authorization": (
            "Bearer "
            + login.json()["access_token"]
        )
    }


def test_otro_usuario_no_puede_modificar(
    client,
    catalogos,
    proyecto_creado,
):
    headers = crear_segundo_usuario(
        client,
        catalogos,
    )

    id_proyecto = (
        proyecto_creado["id_proyecto"]
    )

    response = client.put(
        f"/proyectos/{id_proyecto}",
        headers=headers,
        json={
            "titulo": (
                "Intento de modificación ajena"
            ),
        },
    )

    assert response.status_code == 403


def test_otro_usuario_no_puede_ver_detalle_privado(
    client,
    catalogos,
    proyecto_creado,
):
    headers = crear_segundo_usuario(
        client,
        catalogos,
    )

    id_proyecto = (
        proyecto_creado["id_proyecto"]
    )

    response = client.get(
        (
            "/proyectos/"
            f"mis-proyectos/{id_proyecto}"
        ),
        headers=headers,
    )

    assert response.status_code == 403


def test_participantes_requieren_autenticacion(
    client,
    proyecto_creado,
):
    id_proyecto = (
        proyecto_creado["id_proyecto"]
    )

    response = client.get(
        (
            f"/proyectos/{id_proyecto}"
            "/participantes"
        )
    )

    assert response.status_code in (
        401,
        403,
    )


def test_otro_usuario_no_puede_ver_archivos(
    client,
    catalogos,
    proyecto_creado,
):
    headers = crear_segundo_usuario(
        client,
        catalogos,
    )

    id_proyecto = (
        proyecto_creado["id_proyecto"]
    )

    response = client.get(
        (
            f"/proyectos/{id_proyecto}"
            "/archivos"
        ),
        headers=headers,
    )

    assert response.status_code == 403