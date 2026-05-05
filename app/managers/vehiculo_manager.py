"""
managers/vehiculo_manager.py
─────────────────────────────
Responsabilidad única: persistencia de vehículos autorizados en JSON.
"""

import json
import os
from datetime import datetime
from flask import current_app


class VehiculoManager:

    def _ruta(self) -> str:
        return current_app.config["VEHICULOS_FILE"]

    # ── Lectura / Escritura ────────────────────────────────────────────────────

    def _leer(self) -> dict:
        ruta = self._ruta()
        if not os.path.exists(ruta):
            return {"vehiculos": []}
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    def _guardar(self, data: dict) -> None:
        with open(self._ruta(), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # ── Operaciones públicas ───────────────────────────────────────────────────

    def esta_autorizada(self, placa: str) -> bool:
        """Verifica si una placa está en la lista de autorizados."""
        data  = self._leer()
        placa = placa.strip().upper()
        return any(v["placa"].upper() == placa for v in data["vehiculos"])

    def agregar(self, datos: dict) -> tuple[bool, str]:
        """
        Agrega un vehículo a la lista de autorizados.
        Retorna (True, "") o (False, "motivo") si ya existe.
        """
        data  = self._leer()
        placa = datos.get("placa", "").strip().upper()

        if any(v["placa"].upper() == placa for v in data["vehiculos"]):
            return False, f"La placa {placa} ya está autorizada"

        datos["placa"]           = placa
        datos["fecha_registro"]  = str(datetime.now())

        data["vehiculos"].append(datos)
        self._guardar(data)

        return True, ""

    def eliminar(self, placa: str) -> tuple[bool, str]:
        """Elimina un vehículo autorizado por placa."""
        data  = self._leer()
        placa = placa.strip().upper()

        originales = len(data["vehiculos"])
        data["vehiculos"] = [
            v for v in data["vehiculos"]
            if v["placa"].upper() != placa
        ]

        if len(data["vehiculos"]) == originales:
            return False, f"No se encontró la placa {placa}"

        self._guardar(data)
        return True, ""

    def obtener_todos(self) -> list[dict]:
        """Retorna todos los vehículos autorizados."""
        return self._leer().get("vehiculos", [])
