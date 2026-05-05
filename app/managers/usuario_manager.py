"""
managers/usuario_manager.py
────────────────────────────
Responsabilidad única: persistencia de usuarios en JSON.
No contiene lógica de negocio ni validaciones.
"""

import json
import os
from datetime import datetime
from flask import current_app


class UsuarioManager:

    def _ruta(self) -> str:
        """Obtiene la ruta del archivo de usuarios desde la config."""
        return current_app.config["USUARIOS_FILE"]

    # ── Lectura / Escritura ────────────────────────────────────────────────────

    def _leer(self) -> dict:
        ruta = self._ruta()
        if not os.path.exists(ruta):
            return {"usuarios": []}
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    def _guardar(self, data: dict) -> None:
        with open(self._ruta(), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # ── Operaciones públicas ───────────────────────────────────────────────────

    def existe(self, cedula: str) -> bool:
        """Verifica si una cédula ya está registrada."""
        data = self._leer()
        return any(u["cedula"] == cedula for u in data["usuarios"])

    def guardar(self, datos: dict) -> tuple[bool, str]:
        """
        Guarda un nuevo usuario.
        Retorna (True, "") o (False, "motivo") si ya existe.
        """
        data = self._leer()

        if any(u["cedula"] == datos["cedula"] for u in data["usuarios"]):
            return False, "Ya existe un registro con esta cédula"

        datos["placa"]           = datos.get("placa", "").upper()
        datos["fecha_registro"]  = str(datetime.now())

        data["usuarios"].append(datos)
        self._guardar(data)

        return True, ""

    def obtener_todos(self) -> list[dict]:
        """Retorna la lista completa de usuarios registrados."""
        return self._leer().get("usuarios", [])
