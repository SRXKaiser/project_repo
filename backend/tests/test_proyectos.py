def test_crear_proyecto_requiere_jwt(
    client,
    catalogos,
):
    response = client.post(
        "/proyectos",
        json={
            "titulo": "Proyecto sin autenticación",
            "resumen": (
                "Este proyecto intenta crearse "
                "sin autenticación válida."
            ),
            "id_departamento": (
                catalogos[
                    "departamento"
                ].id_departamento
            ),
        },
    )

    assert response.status_code in (
        401,
        403,
    )


def test_crear_proyecto(
    client,
    auth_headers,
    catalogos,
):
    response = client.post(
        "/proyectos",
        headers=auth_headers,
        json={
            "titulo": "Sistema de investigación",
            "resumen": (
                "Proyecto utilizado para validar "
                "la creación mediante la API."
            ),
            "id_departamento": (
                catalogos[
                    "departamento"
                ].id_departamento
            ),
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert (
        data["titulo"]
        == "Sistema de investigación"
    )

    assert data["estado"] == "BORRADOR"


def test_borrador_no_aparece_publicamente(
    client,
    proyecto_creado,
):
    response = client.get("/proyectos")

    assert response.status_code == 200
    assert response.json() == []


def test_creador_puede_ver_mis_proyectos(
    client,
    auth_headers,
    proyecto_creado,
):
    response = client.get(
        "/proyectos/mis-proyectos",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert (
        data[0]["id_proyecto"]
        == proyecto_creado["id_proyecto"]
    )


def test_creador_puede_ver_detalle_privado(
    client,
    auth_headers,
    proyecto_creado,
):
    id_proyecto = (
        proyecto_creado["id_proyecto"]
    )

    response = client.get(
        (
            "/proyectos/"
            f"mis-proyectos/{id_proyecto}"
        ),
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["id_proyecto"]
        == id_proyecto
    )


def test_borrador_no_tiene_detalle_publico(
    client,
    proyecto_creado,
):
    id_proyecto = (
        proyecto_creado["id_proyecto"]
    )

    response = client.get(
        f"/proyectos/{id_proyecto}/detalle"
    )

    assert response.status_code == 404


def test_actualizar_proyecto(
    client,
    auth_headers,
    proyecto_creado,
):
    id_proyecto = (
        proyecto_creado["id_proyecto"]
    )

    response = client.put(
        f"/proyectos/{id_proyecto}",
        headers=auth_headers,
        json={
            "titulo": (
                "Proyecto actualizado"
            ),
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["titulo"]
        == "Proyecto actualizado"
    )