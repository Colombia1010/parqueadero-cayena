import os
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
from app.config import get_config


def create_app():
    """
    Factory function — crea y configura la aplicación Flask.
    Usar factory pattern permite instanciar la app con distintas
    configuraciones (desarrollo, producción, tests).
    """

    app = Flask(
        __name__,
        template_folder=os.path.join(os.getcwd(), "templates"),
        static_folder=os.path.join(os.getcwd(), "static"),
    )

    # ── Cargar configuración ───────────────────────────────
    config = get_config()
    app.config.from_object(config)

    # ── Crear carpetas necesarias ──────────────────────────
    _crear_carpetas(app)

    # ── Configurar logging ─────────────────────────────────
    _configurar_logs(app)

    # ── Registrar Blueprints ───────────────────────────────
    _registrar_blueprints(app)

    return app


def _crear_carpetas(app: Flask):
    """Crea las carpetas del sistema si no existen."""
    carpetas = [
        app.config["UPLOAD_FOLDER"],
        app.config["DATA_FOLDER"],
        app.config["LOGS_FOLDER"],
    ]
    for carpeta in carpetas:
        os.makedirs(carpeta, exist_ok=True)


def _configurar_logs(app: Flask):
    """
    Configura logging con rotación diaria.
    - Nivel INFO en producción, DEBUG en desarrollo.
    - Archivo rotativo: un log por día, guarda 30 días.
    - También muestra logs en consola.
    """
    nivel = logging.DEBUG if app.config.get("DEBUG") else logging.INFO

    # Formato de cada línea de log
    formato = logging.Formatter(
        "[%(asctime)s] %(levelname)s — %(name)s — %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler de archivo con rotación diaria
    ruta_log = os.path.join(app.config["LOGS_FOLDER"], "cayena.log")
    file_handler = TimedRotatingFileHandler(
        ruta_log,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )
    file_handler.setFormatter(formato)
    file_handler.setLevel(nivel)

    # Handler de consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formato)
    console_handler.setLevel(nivel)

    # Aplicar handlers a la app
    app.logger.setLevel(nivel)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)

    app.logger.info("🚀 Aplicación iniciada en modo %s", app.config.get("FLASK_ENV", "production"))


def _registrar_blueprints(app: Flask):
    """Registra todos los blueprints de la aplicación."""
    from app.blueprints.auth    import auth_bp
    from app.blueprints.registro import registro_bp
    from app.blueprints.admin   import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(registro_bp)
    app.register_blueprint(admin_bp)
