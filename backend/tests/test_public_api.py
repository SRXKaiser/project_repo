def test_root(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_listar_carreras_publicas(
    client,
    catalogos,
):
    response = client.get("/carreras")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["siglas"] == "ISC"
    assert (
        data[0]["id_departamento"]
        == catalogos[
            "departamento"
        ].id_departamento
    )


def test_listar_departamentos_publicos(
    client,
    catalogos,
):
    response = client.get(
        "/departamentos"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert (
        data[0]["nombre"]
        == "Sistemas y Computación"
    )


def test_listar_areas_publicas(
    client,
    catalogos,
):
    response = client.get(
        "/areas-tematicas"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert (
        data[0]["nombre"]
        == "Desarrollo de Software"
    )


def test_proyectos_publicos_inicialmente_vacios(
    client,
):
    response = client.get("/proyectos")

    assert response.status_code == 200
    assert response.json() == []


def test_busqueda_publica_inicialmente_vacia(
    client,
):
    response = client.get(
        "/proyectos/buscar"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["resultados"] == []
    assert data["total"] == 0