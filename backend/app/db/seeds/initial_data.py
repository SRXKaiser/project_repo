from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.carrera import Carrera
from app.models.departamento import Departamento
from app.models.rol import Rol

def seed_initial_data():
    db = SessionLocal()

    try:
        # =========================
        # DEPARTAMENTOS
        # =========================

        departamento = db.scalar(
            select(Departamento).where(
                Departamento.nombre == "Sistemas y Computación"
            )
        )

        if departamento is None:
            departamento = Departamento(
                nombre="Sistemas y Computación"
            )

            db.add(departamento)
            db.flush()

            print(
                f"Departamento creado: "
                f"{departamento.nombre} "
                f"(ID {departamento.id_departamento})"
            )
        else:
            print(
                f"Departamento ya existe: "
                f"{departamento.nombre} "
                f"(ID {departamento.id_departamento})"
            )

        # =========================
        # CARRERAS
        # =========================

        carrera = db.scalar(
            select(Carrera).where(
                Carrera.nombre
                == "Ingeniería en Sistemas Computacionales"
            )
        )

        if carrera is None:
            carrera = Carrera(
                nombre="Ingeniería en Sistemas Computacionales",
                siglas="ISC",
                activa=True,
                id_departamento=departamento.id_departamento,
            )

            db.add(carrera)
            db.flush()

            print(
                f"Carrera creada: "
                f"{carrera.nombre} "
                f"({carrera.siglas}) "
                f"(ID {carrera.id_carrera})"
            )
        else:
            print(
                f"Carrera ya existe: "
                f"{carrera.nombre} "
                f"({carrera.siglas}) "
                f"(ID {carrera.id_carrera})"
            )
            # =========================
            # ROLES
            # =========================

        rol_admin = db.scalar(
            select(Rol).where(
                Rol.nombre == "ADMINISTRADOR"
            )
        )

        if rol_admin is None:
            rol_admin = Rol(
                nombre="ADMINISTRADOR",
                descripcion="Administrador general del sistema",
            )

            db.add(rol_admin)
            db.flush()

            print(
                f"Rol creado: {rol_admin.nombre} "
                f"(ID {rol_admin.id_rol})"
            )
        else:
            print(
                f"Rol ya existe: {rol_admin.nombre} "
                f"(ID {rol_admin.id_rol})"
            )

        # =========================
        # CONFIRMAR TRANSACCIÓN
        # =========================

        db.commit()

        print()
        print("Seed completado correctamente.")

    except Exception as error:
        db.rollback()

        print()
        print("Error al ejecutar el seed.")
        print("Se revirtieron todos los cambios.")

        raise error

    finally:
        db.close()


if __name__ == "__main__":
    seed_initial_data()