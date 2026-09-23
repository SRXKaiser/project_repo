def test_no_puede_enviar_proyecto_incompleto(
    client,
    auth_headers,
    proyecto_creado,
):
    id_proyecto = (
        proyecto_creado["id_proyecto"]
    )

    response = client.post(
        (
            f"/proyectos/{id_proyecto}"
            "/enviar-revision"
        ),
        headers=auth_headers,
        json={
            "comentario": (
                "Intento de envío incompleto"
            )
        },
    )

    assert response.status_code == 409


def test_asignar_area_al_proyecto(
    client,
    auth_headers,
    proyecto_creado,
    catalogos,
):
    id_proyecto = (
        proyecto_creado["id_proyecto"]
    )

    id_area = (
        catalogos["area"].id_area
    )

    response = client.post(
        (
            f"/proyectos/{id_proyecto}"
            f"/areas/{id_area}"
        ),
        headers=auth_headers,
    )

    assert response.status_code == 201

    assert (
        response.json()["id_area"]
        == id_area
    )


def test_agregar_palabra_clave(
    client,
    auth_headers,
    proyecto_creado,
):
    id_proyecto = (
        proyecto_creado["id_proyecto"]
    )

    response = client.post(
        (
            f"/proyectos/{id_proyecto}"
            "/palabras-clave"
        ),
        headers=auth_headers,
        json={
            "nombre": "FastAPI"
        },
    )

    assert response.status_code == 201

    assert (
        response.json()["nombre"]
        == "FastAPI"
    )


def test_rechaza_archivo_que_no_es_pdf(
    client,
    auth_headers,
    proyecto_creado,
):
    id_proyecto = (
        proyecto_creado["id_proyecto"]
    )

    response = client.post(
        (
            f"/proyectos/{id_proyecto}"
            "/archivos"
        ),
        headers=auth_headers,
        files={
            "archivo": (
                "archivo.txt",
                b"Esto no es un PDF",
                "text/plain",
            )
        },
    )

    assert response.status_code == 415


def test_rechaza_pdf_con_contenido_invalido(
    client,
    auth_headers,
    proyecto_creado,
):
    id_proyecto = (
        proyecto_creado["id_proyecto"]
    )

    response = client.post(
        (
            f"/proyectos/{id_proyecto}"
            "/archivos"
        ),
        headers=auth_headers,
        files={
            "archivo": (
                "falso.pdf",
                b"Esto tampoco es un PDF",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400


def test_proyecto_sigue_borrador_si_faltan_requisitos(
    client,
    auth_headers,
    proyecto_creado,
    catalogos,
):
    id_proyecto = (
        proyecto_creado["id_proyecto"]
    )

    id_area = (
        catalogos["area"].id_area
    )

    area_response = client.post(
        (
            f"/proyectos/{id_proyecto}"
            f"/areas/{id_area}"
        ),
        headers=auth_headers,
    )

    assert area_response.status_code == 201

    keyword_response = client.post(
        (
            f"/proyectos/{id_proyecto}"
            "/palabras-clave"
        ),
        headers=auth_headers,
        json={
            "nombre": "PostgreSQL"
        },
    )

    assert keyword_response.status_code == 201

    response = client.post(
        (
            f"/proyectos/{id_proyecto}"
            "/enviar-revision"
        ),
        headers=auth_headers,
        json={
            "comentario": (
                "Todavía falta el documento"
            )
        },
    )

    assert response.status_code == 409