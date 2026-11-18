from datetime import datetime

from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from db import todos_los_nodos
from datos_dashboard import obtener_datos
from perfiles import obtener_seccion, perfil_de

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-secreta"  # cámbiala por una cadena larga y propia
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax")
app.jinja_env.filters["money"] = lambda v: "${:,.2f}".format(float(v or 0))

SUCURSALES = {1: "Norte", 2: "Centro", 3: "Sur"}

SQL_USUARIO = """
    SELECT c.id_empleado, c.usuario, c.contrasena_hash, c.activo,
           e.nombre, e.puesto, e.id_sucursal, r.nombre_rol
    FROM credenciales c
    JOIN empleados e ON e.id_empleado = c.id_empleado
    LEFT JOIN rol r  ON r.id_empleado = c.id_empleado AND r.activo
    WHERE c.usuario = %s
    LIMIT 1
"""


def buscar_usuario(usuario):
    """Busca el usuario en los tres nodos.
    Devuelve (fila_o_None, hubo_error_de_conexion)."""
    hubo_error = False
    for nodo in todos_los_nodos():
        try:
            filas = nodo.consultar(SQL_USUARIO, (usuario,))
        except Exception:
            hubo_error = True
            continue
        if filas:
            return filas[0], hubo_error
    return None, hubo_error


def registrar_acceso(u):
    """Guarda la fecha del último acceso en el nodo de la sucursal del usuario."""
    try:
        nodo = next(
            n for n in todos_los_nodos() if n.nombre == SUCURSALES[u["id_sucursal"]]
        )
        nodo.ejecutar(
            "UPDATE credenciales SET ultimo_acceso = now() WHERE id_empleado = %s",
            (u["id_empleado"],),
        )
    except Exception:
        pass  # no impedir el acceso si esto falla


def login_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return wrapper


@app.route("/")
def index():
    return redirect(url_for("dashboard" if "usuario" in session else "login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        clave = request.form.get("clave", "")

        u, hubo_error = buscar_usuario(usuario)

        if u and u["activo"] and check_password_hash(u["contrasena_hash"], clave):
            session.clear()
            session["usuario"] = {
                "id_empleado": u["id_empleado"],
                "usuario": u["usuario"],
                "nombre": u["nombre"],
                "puesto": u["puesto"],
                "rol": u["nombre_rol"],
                "sucursal": SUCURSALES[u["id_sucursal"]],
            }
            registrar_acceso(u)
            return redirect(url_for("dashboard"))

        if not u and hubo_error:
            flash(
                "No se pudo conectar con la base de datos. Intenta de nuevo.", "error"
            )
        else:
            flash("Usuario o contraseña incorrectos.", "error")

    return render_template("login.html")


@app.route("/dashboard")
@app.route("/dashboard/<slug>")
@login_requerido
def dashboard(slug="resumen"):
    u = session["usuario"]
    perfil = perfil_de(u.get("rol"))
    seccion = obtener_seccion(perfil, slug)
    datos = obtener_datos(u.get("rol"), u.get("sucursal"))
    return render_template(
        "dashboard.html",
        u=u,
        perfil=perfil,
        seccion=seccion,
        datos=datos,
        hoy=datetime.now().strftime("%d/%m/%Y"),
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
