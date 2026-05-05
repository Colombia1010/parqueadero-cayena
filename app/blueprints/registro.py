"""
blueprints/registro.py
───────────────────────
Rutas públicas: formulario de registro e inscripción al sorteo.
"""

from flask import (
    Blueprint, request, render_template,
    jsonify, current_app
)

from app.managers.usuario_manager  import UsuarioManager
from app.managers.vehiculo_manager import VehiculoManager
from app.utils.validaciones        import validar_registro
from app.utils.archivos            import guardar_documentos

registro_bp = Blueprint("registro", __name__)


@registro_bp.route("/")
def inicio():
    return render_template("formulario.html")


@registro_bp.route("/validar_placa", methods=["POST"])
def validar_placa():
    """
    Endpoint AJAX que verifica si una placa está autorizada.
    Permite feedback en tiempo real en el formulario.
    """
    data  = request.get_json(silent=True) or {}
    placa = data.get("placa", "").strip().upper()

    if not placa:
        return jsonify({"autorizada": False, "mensaje": "Placa vacía"})

    manager = VehiculoManager()

    if manager.esta_autorizada(placa):
        return jsonify({"autorizada": True, "mensaje": "✅ Vehículo autorizado"})

    current_app.logger.info("🔍 Placa no autorizada consultada: %s", placa)
    return jsonify({
        "autorizada": False,
        "mensaje": "❌ Esta placa no está registrada. Acércate a administración para autorizar tu vehículo."
    })


@registro_bp.route("/registro", methods=["POST"])
def registro():
    """
    Procesa el formulario de inscripción.
    Orden: validaciones → placa autorizada → duplicado → archivos → guardar.
    """
    try:
        form = request.form

        # 1️⃣ Validar campos del formulario
        valido, mensaje = validar_registro(form)
        if not valido:
            return mensaje, 400

        placa = form.get("placa", "").strip().upper()

        # 2️⃣ Validar placa autorizada (segunda capa, además del JS)
        vehiculo_manager = VehiculoManager()
        if not vehiculo_manager.esta_autorizada(placa):
            current_app.logger.warning(
                "🚫 Intento de registro con placa no autorizada: %s", placa
            )
            return (
                "🚫 Tu vehículo no está registrado. "
                "Acércate a administración del conjunto Cayena para autorizar tu placa.",
                403
            )

        cedula = form.get("cedula", "").strip()

        # 3️⃣ Verificar duplicado de cédula
        usuario_manager = UsuarioManager()
        if usuario_manager.existe(cedula):
            return "⚠️ Ya tienes un registro activo con esta cédula.", 409

        # 4️⃣ Guardar documentos
        ok, msg = guardar_documentos(request.files, cedula)
        if not ok:
            return f"❌ {msg}", 400

        # 5️⃣ Guardar usuario
        datos = {
            "cedula":            cedula,
            "nombre":            form.get("nombre", "").strip(),
            "torre":             form.get("torre", "").strip(),
            "apto":              form.get("apto", "").strip(),
            "nombre_propiedad":  form.get("nombre_propiedad", "").strip(),
            "celular":           form.get("celular", "").strip(),
            "correo":            form.get("correo", "").strip(),
            "nombre_propietario": form.get("nombre_propietario", "").strip(),
            "mail_propietario":  form.get("mail_propietario", "").strip(),
            "celular1":          form.get("celular1", "").strip(),
            "nombre_arrendatario": form.get("nombre_arrendatario", "").strip(),
            "vehiculo":          form.get("vehiculo", "").strip(),
            "placa":             placa,
            "marca":             form.get("marca", "").strip(),
            "modelo":            form.get("modelo", "").strip(),
            "color":             form.get("color", "").strip(),
        }

        ok, msg = usuario_manager.guardar(datos)
        if not ok:
            return f"⚠️ {msg}", 409

        current_app.logger.info(
            "✅ Nuevo registro exitoso — cédula: %s | placa: %s | apto: %s-%s",
            cedula, placa, form.get("torre"), form.get("apto")
        )
        return "✅ Registro exitoso. ¡Quedas inscrito al sorteo de parqueadero!", 200

    except Exception as e:
        current_app.logger.error("❌ Error inesperado en /registro: %s", str(e), exc_info=True)
        return "❌ Error interno del servidor. Intenta de nuevo.", 500
