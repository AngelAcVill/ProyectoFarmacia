"""
Datos de prueba para los 3 nodos: empleados, roles, credenciales,
clientes e inventarios. Se puede ejecutar varias veces sin duplicar.
"""

from werkzeug.security import generate_password_hash
from db import Nodo

PASSWORD_PRUEBA = "Yza2026!"  # misma contraseña de prueba para todos

# (usuario, nombre, correo, puesto, rol)
USUARIOS = {
    "Norte": [
        (
            "gerente_norte",
            "Laura Méndez",
            "gerente.norte@yza.com",
            "Gerente",
            "Gerente",
        ),
        (
            "operador_norte",
            "Carlos Pérez",
            "operador.norte@yza.com",
            "Cajero",
            "Operador",
        ),
    ],
    "Centro": [
        ("admin_yza", "Administrador Yza", "admin@yza.com", "Gerente", "Administrador"),
        (
            "gerente_centro",
            "Marta Ruiz",
            "gerente.centro@yza.com",
            "Gerente",
            "Gerente",
        ),
        (
            "operador_centro",
            "Luis Hernández",
            "operador.centro@yza.com",
            "Cajero",
            "Operador",
        ),
        ("auditor_yza", "Ana Torres", "auditor@yza.com", "Almacenista", "Auditor"),
        ("consulta_yza", "Pedro Gómez", "consulta@yza.com", "Farmaceutico", "Consulta"),
    ],
    "Sur": [
        ("gerente_sur", "Rosa Díaz", "gerente.sur@yza.com", "Gerente", "Gerente"),
        ("operador_sur", "Jorge Salazar", "operador.sur@yza.com", "Cajero", "Operador"),
    ],
}

# (nombre, correo, telefono)
CLIENTES = {
    "Norte": [
        ("María López", "maria.lopez@correo.com", "993-410-0001"),
        ("Juan Castillo", "juan.castillo@correo.com", "993-410-0002"),
    ],
    "Centro": [
        ("Elena Vargas", "elena.vargas@correo.com", "993-420-0001"),
        ("Raúl Morales", "raul.morales@correo.com", "993-420-0002"),
    ],
    "Sur": [
        ("Sofía Ramos", "sofia.ramos@correo.com", "993-430-0001"),
        ("Diego Cruz", "diego.cruz@correo.com", "993-430-0002"),
    ],
}

# Existencias de los 10 medicamentos (algunas bajo el mínimo, para probar alertas)
EXISTENCIAS = [50, 8, 40, 5, 30, 12, 25, 6, 18, 45]
DESPLAZAMIENTO = {"Norte": 0, "Centro": 3, "Sur": 6}


def sembrar(nombre):
    nodo = Nodo(nombre)
    conn = nodo.conectar()
    try:
        with conn.cursor() as cur:
            # Empleados + rol + credenciales
            for usuario, nom, correo, puesto, rol in USUARIOS[nombre]:
                cur.execute("SELECT 1 FROM credenciales WHERE usuario = %s", (usuario,))
                if cur.fetchone():
                    continue
                cur.execute(
                    "INSERT INTO empleados (nombre, correo, puesto) "
                    "VALUES (%s, %s, %s) RETURNING id_empleado",
                    (nom, correo, puesto),
                )
                id_emp = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO rol (id_empleado, nombre_rol) VALUES (%s, %s)",
                    (id_emp, rol),
                )
                cur.execute(
                    "INSERT INTO credenciales (id_empleado, usuario, contrasena_hash) "
                    "VALUES (%s, %s, %s)",
                    (id_emp, usuario, generate_password_hash(PASSWORD_PRUEBA)),
                )

            # Clientes
            for nom, correo, tel in CLIENTES[nombre]:
                cur.execute(
                    "INSERT INTO clientes (nombre, correo, telefono) VALUES (%s, %s, %s) "
                    "ON CONFLICT (correo) DO NOTHING",
                    (nom, correo, tel),
                )

            # Inventario (medicamentos 1..10)
            d = DESPLAZAMIENTO[nombre]
            for i in range(10):
                existencia = EXISTENCIAS[(i + d) % 10]
                cur.execute(
                    "INSERT INTO inventarios (id_medicamento, existencia, stock_minimo) "
                    "SELECT id_medicamento, %s, stock_minimo FROM medicamentos "
                    "WHERE id_medicamento = %s "
                    "ON CONFLICT (id_sucursal, id_medicamento) DO NOTHING",
                    (existencia, i + 1),
                )
        conn.commit()
        print(f"Nodo {nombre}: datos de prueba listos")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    for n in USUARIOS:
        sembrar(n)
    print("\nUsuarios de prueba (contraseña para todos:", PASSWORD_PRUEBA + ")")
    for n, lista in USUARIOS.items():
        for u, _, _, _, rol in lista:
            print(f"  {u:<16} {rol:<14} sucursal {n}")
