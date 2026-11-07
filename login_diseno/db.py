import psycopg2
import psycopg2.extras
from config import NODOS


class Nodo:
    """Conexión a un nodo (sucursal) de la cadena Yza."""

    def __init__(self, nombre):
        self.nombre = nombre
        self.cfg = NODOS[nombre]

    def conectar(self):
        return psycopg2.connect(
            host=self.cfg["host"],
            port=self.cfg["port"],
            dbname=self.cfg["dbname"],
            user=self.cfg["user"],
            password=self.cfg["password"],
            connect_timeout=5,
        )

    def consultar(self, sql, params=None):
        conn = self.conectar()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql, params)
                return cur.fetchall()
        finally:
            conn.close()

    def ejecutar(self, sql, params=None):
        """Una sentencia en transacción: COMMIT si sale bien, ROLLBACK si falla."""
        conn = self.conectar()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, params)
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def todos_los_nodos():
    return [Nodo(n) for n in NODOS]
