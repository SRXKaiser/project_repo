from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.usuario_rol import UsuarioRol


def assign_admin(correo: str):
    db = SessionLocal()

    try:
        correo = correo.lower().strip()

        usuario = db.scalar(
            select(Usuario).where(
                Usuario.correo == correo
            )
        )

        if usuario is None:
            print("No existe un usuario con ese correo.")
            return

        rol_admin = db.scalar(
            select(Rol).where(
                Rol.nombre == "ADMINISTRADOR"
            )
        )

        if rol_admin is None:
            print(
                "No existe el rol ADMINISTRADOR. "
                "Ejecuta primero initial_data."
            )
            return

        asignacion = db.scalar(
            select(UsuarioRol).where(
                UsuarioRol.id_usuario == usuario.id_usuario,
                UsuarioRol.id_rol == rol_admin.id_rol,
            )
        )

        if asignacion is not None:
            print(
                f"{usuario.correo} ya es administrador."
            )
            return

        asignacion = UsuarioRol(
            id_usuario=usuario.id_usuario,
            id_rol=rol_admin.id_rol,
        )

        db.add(asignacion)
        db.commit()

        print(
            f"Rol ADMINISTRADOR asignado a "
            f"{usuario.correo}."
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    correo = input(
        "Correo del usuario que será administrador: "
    )

    assign_admin(correo)