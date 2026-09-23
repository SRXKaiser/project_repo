from datetime import date

from app.core.security import hash_password
from app.models.docente import Docente
from app.models.enums import (
    EstadoCuenta,
    TipoUsuario,
)
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.usuario_rol import UsuarioRol


def crear_usuario_docente(
    db,
    catalogos,
):
    usuario = Usuario(
        nombre="Docente",
        apellido_paterno="Responsable",
        apellido_materno="Prueba",
        correo="docente@example.com",
        password_hash=hash_password(
            "PasswordDocente123!"
        ),
        tipo_usuario=TipoUsuario.DOCENTE,
        estado_cuenta=EstadoCuenta.ACTIVA,
    )

    db.add(usuario)
    db.flush()

    docente = Docente(
        id_usuario=usuario.id_usuario,
        num_empleado="DOC-TEST-001",
        id_departamento=(
            catalogos[
                "departamento"
            ].id_departamento
        ),
    )

    db.add(docente)
    db.commit()
    db.refresh(usuario)

    return usuario


def crear_administrador(
    db,
):
    usuario = Usuario(
        nombre="Administrador",
        apellido_paterno="Sistema",
        apellido_materno="Prueba",
        correo="admin@example.com",
        password_hash=hash_password(
            "PasswordAdmin123!"
        ),
        tipo_usuario=TipoUsuario.DOCENTE,
        estado_cuenta=EstadoCuenta.ACTIVA,
    )

    db.add(usuario)
    db.flush()

    rol = Rol(
        nombre="ADMINISTRADOR",
    )

    db.add(rol)
    db.flush()

    usuario_rol = UsuarioRol(
        id_usuario=usuario.id_usuario,
        id_rol=rol.id_rol,
    )

    db.add(usuario_rol)
    db.commit()
    db.refresh(usuario)

    return usuario


def login(
    client,
    correo,
    password,
):
    response = client.post(
        "/auth/login",
        json={
            "correo": correo,
            "password": password,
        },
    )

    assert response.status_code == 200

    return {
        "Authorization": (
            "Bearer "
            + response.json()["access_token"]
        )
    }


def test_workflow_completo_hasta_publicacion(
    client,
    db,
    catalogos,
    estudiante_payload,
):
    # -------------------------------------------------
    # 1. Registrar y autenticar al autor
    # -------------------------------------------------

    registro = client.post(
        "/auth/register",
        json=estudiante_payload,
    )

    assert registro.status_code == 201

    autor_headers = login(
        client,
        estudiante_payload["correo"],
        estudiante_payload["password"],
    )

    # -------------------------------------------------
    # 2. Crear proyecto
    # -------------------------------------------------

    proyecto_response = client.post(
        "/proyectos",
        headers=autor_headers,
        json={
            "titulo": (
                "Sistema integral de investigación"
            ),
            "resumen": (
                "Proyecto utilizado para comprobar "
                "el workflow integral del repositorio."
            ),
            "id_departamento": (
                catalogos[
                    "departamento"
                ].id_departamento
            ),
        },
    )

    assert proyecto_response.status_code == 201

    proyecto = proyecto_response.json()

    id_proyecto = proyecto["id_proyecto"]

    assert proyecto["estado"] == "BORRADOR"

    # -------------------------------------------------
    # 3. Asignar área temática
    # -------------------------------------------------

    area_response = client.post(
        (
            f"/proyectos/{id_proyecto}"
            f"/areas/"
            f"{catalogos['area'].id_area}"
        ),
        headers=autor_headers,
    )

    assert area_response.status_code == 201

    # -------------------------------------------------
    # 4. Agregar palabra clave
    # -------------------------------------------------

    keyword_response = client.post(
        (
            f"/proyectos/{id_proyecto}"
            "/palabras-clave"
        ),
        headers=autor_headers,
        json={
            "nombre": "Integración"
        },
    )

    assert keyword_response.status_code == 201

    # -------------------------------------------------
    # 5. Subir un PDF válido mínimo
    # -------------------------------------------------

    pdf_bytes = (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog >>\n"
        b"endobj\n"
        b"trailer\n"
        b"<<>>\n"
        b"%%EOF\n"
    )

    archivo_response = client.post(
        (
            f"/proyectos/{id_proyecto}"
            "/archivos"
        ),
        headers=autor_headers,
        files={
            "archivo": (
                "proyecto_integral.pdf",
                pdf_bytes,
                "application/pdf",
            )
        },
    )

    assert archivo_response.status_code == 201

    archivo = archivo_response.json()

    id_archivo = archivo["id_archivo"]

    # -------------------------------------------------
    # 6. Enviar proyecto a revisión
    # -------------------------------------------------

    revision_response = client.post(
        (
            f"/proyectos/{id_proyecto}"
            "/enviar-revision"
        ),
        headers=autor_headers,
        json={
            "comentario": (
                "Proyecto listo para revisión"
            )
        },
    )

    assert revision_response.status_code == 200

    assert (
        revision_response.json()["estado"]
        == "EN_REVISION"
    )

    # -------------------------------------------------
    # 7. Crear docente responsable
    # -------------------------------------------------

    docente = crear_usuario_docente(
        db,
        catalogos,
    )

    docente_headers = login(
        client,
        "docente@example.com",
        "PasswordDocente123!",
    )

    # Antes de asignarlo, no debe poder aprobar.
    sin_permiso = client.post(
        f"/proyectos/{id_proyecto}/aprobar",
        headers=docente_headers,
        json={
            "comentario": (
                "Intento sin ser responsable"
            )
        },
    )

    assert sin_permiso.status_code == 403

    # -------------------------------------------------
    # 8. Crear administrador
    # -------------------------------------------------

    crear_administrador(db)

    admin_headers = login(
        client,
        "admin@example.com",
        "PasswordAdmin123!",
    )

    # -------------------------------------------------
    # 9. Admin asigna responsable de departamento
    # -------------------------------------------------

    id_departamento = (
        catalogos[
            "departamento"
        ].id_departamento
    )

    responsable_response = client.put(
        (
            "/admin/departamentos/"
            f"{id_departamento}"
            "/responsable"
        ),
        headers=admin_headers,
        json={
            "id_usuario_docente": (
                docente.id_usuario
            )
        },
    )

    assert responsable_response.status_code == 200

    responsable = (
        responsable_response.json()
    )

    assert (
        responsable["id_usuario_docente"]
        == docente.id_usuario
    )

    assert responsable["activo"] is True

    # -------------------------------------------------
    # 10. Responsable ve el proyecto pendiente
    # -------------------------------------------------

    pendientes_response = client.get(
        "/proyectos/revision/pendientes",
        headers=docente_headers,
    )

    assert pendientes_response.status_code == 200

    pendientes = pendientes_response.json()

    assert any(
        item["id_proyecto"] == id_proyecto
        for item in pendientes
    )

    # -------------------------------------------------
    # 11. Responsable aprueba
    # -------------------------------------------------

    aprobar_response = client.post(
        f"/proyectos/{id_proyecto}/aprobar",
        headers=docente_headers,
        json={
            "comentario": (
                "Proyecto aprobado en prueba integral"
            )
        },
    )

    assert aprobar_response.status_code == 200

    assert (
        aprobar_response.json()["estado"]
        == "APROBADO"
    )

    # -------------------------------------------------
    # 12. Responsable publica
    # -------------------------------------------------

    publicar_response = client.post(
        f"/proyectos/{id_proyecto}/publicar",
        headers=docente_headers,
        json={
            "comentario": (
                "Proyecto publicado"
            )
        },
    )

    assert publicar_response.status_code == 200

    publicado = publicar_response.json()

    assert publicado["estado"] == "PUBLICADO"

    assert (
        publicado["fecha_publicacion"]
        is not None
    )

    # -------------------------------------------------
    # 13. Proyecto ahora es público
    # -------------------------------------------------

    publico_response = client.get(
        f"/proyectos/{id_proyecto}"
    )

    assert publico_response.status_code == 200

    assert (
        publico_response.json()["estado"]
        == "PUBLICADO"
    )

    # -------------------------------------------------
    # 14. Detalle público
    # -------------------------------------------------

    detalle_response = client.get(
        f"/proyectos/{id_proyecto}/detalle"
    )

    assert detalle_response.status_code == 200

    detalle = detalle_response.json()

    assert (
        detalle["id_proyecto"]
        == id_proyecto
    )

    # -------------------------------------------------
    # 15. Debe aparecer en listado público
    # -------------------------------------------------

    listado_response = client.get(
        "/proyectos"
    )

    assert listado_response.status_code == 200

    assert any(
        item["id_proyecto"] == id_proyecto
        for item in listado_response.json()
    )

    # -------------------------------------------------
    # 16. Debe aparecer en búsqueda pública
    # -------------------------------------------------

    busqueda_response = client.get(
        "/proyectos/buscar",
        params={
            "q": "Sistema integral"
        },
    )

    assert busqueda_response.status_code == 200

    busqueda = busqueda_response.json()

    assert busqueda["total"] >= 1

    assert any(
        item["id_proyecto"] == id_proyecto
        for item in busqueda["resultados"]
    )

    # -------------------------------------------------
    # 17. Descarga pública del PDF
    # -------------------------------------------------

    descarga_response = client.get(
        (
            f"/proyectos/{id_proyecto}"
            f"/archivos/{id_archivo}/publico"
        )
    )

    assert descarga_response.status_code == 200

    assert descarga_response.content.startswith(
        b"%PDF-"
    )

    # -------------------------------------------------
    # 18. Historial
    # -------------------------------------------------

    historial_response = client.get(
        (
            f"/proyectos/{id_proyecto}"
            "/historial"
        ),
        headers=autor_headers,
    )

    assert historial_response.status_code == 200

    historial = historial_response.json()

    estados = [
        registro["estado_nuevo"]
        for registro in historial
    ]

    assert "EN_REVISION" in estados
    assert "APROBADO" in estados
    assert "PUBLICADO" in estados