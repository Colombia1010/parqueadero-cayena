import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()


class Config:
    """
    Configuración base del proyecto.
    Todas las variables sensibles se leen desde .env
    """

    # ── Seguridad ──────────────────────────────────────────
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_key_insegura_cambiar")

    # ── Credenciales admin ─────────────────────────────────
    ADMIN_USER     = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

    # ── Archivos subidos ───────────────────────────────────
    UPLOAD_FOLDER      = os.path.join(os.getcwd(), "uploads")
    ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB máximo por archivo

    # ── Datos JSON ─────────────────────────────────────────
    DATA_FOLDER              = os.path.join(os.getcwd(), "data")
    USUARIOS_FILE            = os.path.join(DATA_FOLDER, "usuarios.json")
    VEHICULOS_FILE           = os.path.join(DATA_FOLDER, "vehiculos_autorizados.json")

    # ── Logs ───────────────────────────────────────────────
    LOGS_FOLDER = os.path.join(os.getcwd(), "app", "logs")


class DevelopmentConfig(Config):
    """Configuración para desarrollo local"""
    DEBUG = True
    FLASK_ENV = "development"


class ProductionConfig(Config):
    """Configuración para producción (Render, hosting)"""
    DEBUG = False
    FLASK_ENV = "production"


# Mapa para seleccionar config según variable de entorno
config_map = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
}

def get_config():
    entorno = os.getenv("FLASK_ENV", "production")
    return config_map.get(entorno, ProductionConfig)
