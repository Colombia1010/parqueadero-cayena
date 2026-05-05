"""
blueprints/auth.py
───────────────────
Maneja autenticación: login y logout del administrador.
"""

from flask import (
    Blueprint, request, render_template,
    redirect, session, current_app
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario  = request.form.get("usuario", "").strip()
        password = request.form.get("password", "").strip()

        admin_user = current_app.config["ADMIN_USER"]
        admin_pass = current_app.config["ADMIN_PASSWORD"]

        if usuario == admin_user and password == admin_pass:
            session["admin"] = True
            current_app.logger.info("✅ Login exitoso para usuario: %s", usuario)
            return redirect("/admin")

        current_app.logger.warning("⚠️ Intento de login fallido para usuario: %s", usuario)
        return render_template("login.html", error="❌ Credenciales incorrectas")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    current_app.logger.info("🔒 Sesión cerrada")
    return redirect("/login")
