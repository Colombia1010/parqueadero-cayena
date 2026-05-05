"""
utils/archivos.py
─────────────────
Centraliza toda la lógica de manejo de archivos subidos:
validación de extensión, guardado y listado.
"""

import os
from werkzeug.utils import secure_filename
from flask import current_app


# Campos de documentos requeridos en el formulario
CAMPOS_DOCUMENTOS = ["cedula_doc", "soat", "tarjeta"]


def extension_permitida(nombre_archivo: str) -> bool:
    """Verifica que la extensión del archivo esté en la lista permitida."""
    extensiones = current_app.config.get("ALLOWED_EXTENSIONS", set())
    return (
        "." in nombre_archivo
        and nombre_archivo.rsplit(".", 1)[1].lower() in extensiones
    )


def guardar_documentos(archivos: dict, cedula: str) -> tuple[bool, str]:
    """
    Guarda los documentos del usuario en su carpeta personal.

    Args:
        archivos: dict de {campo: FileStorage} proveniente de request.files
        cedula:   cédula del usuario (usada como nombre de carpeta)

    Returns:
        (True, "") si todo salió bien
        (False, "mensaje de error") si hubo algún problema
    """
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    ruta_usuario  = os.path.join(upload_folder, cedula)
    os.makedirs(ruta_usuario, exist_ok=True)

    for campo in CAMPOS_DOCUMENTOS:
        archivo = archivos.get(campo)

        if not archivo or archivo.filename == "":
            return False, f"El documento '{campo}' es obligatorio"

        if not extension_permitida(archivo.filename):
            return False, f"El archivo '{campo}' tiene una extensión no permitida (usa PDF, JPG o PNG)"

        nombre_seguro = secure_filename(f"{campo}_{archivo.filename}")
        archivo.save(os.path.join(ruta_usuario, nombre_seguro))

    return True, ""


def listar_documentos(cedula: str) -> list[str]:
    """
    Lista los archivos guardados en la carpeta de un usuario.

    Returns:
        Lista de nombres de archivo, o lista vacía si no existe la carpeta.
    """
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    ruta = os.path.join(upload_folder, cedula)

    if not os.path.exists(ruta):
        return []

    return os.listdir(ruta)
