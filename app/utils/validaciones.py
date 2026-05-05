"""
utils/validaciones.py
─────────────────────
Centraliza todas las reglas de validación del sistema.
Retorna tuplas (es_valido: bool, mensaje: str) para un
manejo de errores consistente en toda la aplicación.
"""

import re


# ── Constantes de validación ───────────────────────────────────────────────────

LONGITUD_TORRE_MAX   = 2
LONGITUD_APTO_MAX    = 4
LONGITUD_CELULAR     = 10
LONGITUD_PLACA_MAX   = 6
LONGITUD_CEDULA_MAX  = 15


# ── Validadores individuales ───────────────────────────────────────────────────

def validar_torre(torre: str) -> tuple[bool, str]:
    torre = torre.strip()
    if not torre:
        return False, "La torre es obligatoria"
    if not torre.isdigit():
        return False, "La torre solo debe contener números"
    if len(torre) > LONGITUD_TORRE_MAX:
        return False, f"La torre no puede tener más de {LONGITUD_TORRE_MAX} dígitos"
    return True, ""


def validar_apto(apto: str) -> tuple[bool, str]:
    apto = apto.strip()
    if not apto:
        return False, "El apto es obligatorio"
    if not apto.isdigit():
        return False, "El apto solo debe contener números"
    if len(apto) > LONGITUD_APTO_MAX:
        return False, f"El apto no puede tener más de {LONGITUD_APTO_MAX} dígitos"
    return True, ""


def validar_celular(celular: str) -> tuple[bool, str]:
    celular = celular.strip()
    if not celular:
        return False, "El celular es obligatorio"
    if not celular.isdigit():
        return False, "El celular solo debe contener números"
    if len(celular) != LONGITUD_CELULAR:
        return False, f"El celular debe tener exactamente {LONGITUD_CELULAR} dígitos"
    return True, ""


def validar_placa(placa: str) -> tuple[bool, str]:
    placa = placa.strip().upper()
    if not placa:
        return False, "La placa es obligatoria"
    if len(placa) > LONGITUD_PLACA_MAX:
        return False, f"La placa no puede tener más de {LONGITUD_PLACA_MAX} caracteres"
    if not re.match(r'^[A-Z0-9]+$', placa):
        return False, "La placa solo puede contener letras y números"
    return True, ""


def validar_cedula(cedula: str) -> tuple[bool, str]:
    cedula = cedula.strip()
    if not cedula:
        return False, "La cédula es obligatoria"
    if len(cedula) > LONGITUD_CEDULA_MAX:
        return False, f"La cédula no puede tener más de {LONGITUD_CEDULA_MAX} caracteres"
    if not cedula.isdigit():
        return False, "La cédula solo debe contener números"
    return True, ""


def validar_email(email: str) -> tuple[bool, str]:
    email = email.strip()
    if not email:
        return False, "El correo es obligatorio"
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(patron, email):
        return False, f"El correo '{email}' no tiene un formato válido"
    return True, ""


# ── Validador completo del formulario de registro ──────────────────────────────

def validar_registro(form: dict) -> tuple[bool, str]:
    """
    Valida todos los campos del formulario de registro.
    Retorna (True, "") si todo está bien,
    o (False, "mensaje de error") al primer problema encontrado.
    """

    validaciones = [
        validar_cedula(form.get("cedula", "")),
        validar_torre(form.get("torre", "")),
        validar_apto(form.get("apto", "")),
        validar_celular(form.get("celular", "")),
        validar_email(form.get("correo", "")),
        validar_email(form.get("mail_propietario", "")),
        validar_placa(form.get("placa", "")),
    ]

    for es_valido, mensaje in validaciones:
        if not es_valido:
            return False, mensaje

    # Campos de texto obligatorios
    campos_requeridos = [
        ("nombre", "El nombre es obligatorio"),
        ("nombre_propiedad", "El nombre en tarjeta de propiedad es obligatorio"),
        ("nombre_propietario", "El nombre del propietario es obligatorio"),
        ("vehiculo", "El tipo de vehículo es obligatorio"),
        ("marca", "La marca es obligatoria"),
        ("modelo", "El modelo es obligatorio"),
        ("color", "El color es obligatorio"),
    ]

    for campo, mensaje in campos_requeridos:
        if not form.get(campo, "").strip():
            return False, mensaje

    return True, ""
