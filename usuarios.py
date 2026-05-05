import json
from datetime import datetime
import os

class UsuarioManager:

    def __init__(self, archivo='usuarios.json'):
        self.archivo = archivo

        # Crear archivo si no existe
        if not os.path.exists(self.archivo):
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump({"usuarios": []}, f)

    # ---------------------------
    # LEER DATOS
    # ---------------------------
    def leer_datos(self):
        with open(self.archivo, 'r', encoding='utf-8') as f:
            return json.load(f)

    # ---------------------------
    # GUARDAR DATOS
    # ---------------------------
    def guardar_datos(self, data):
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    # ---------------------------
    # VALIDAR SI EXISTE
    # ---------------------------
    def usuario_existe(self, cedula):
        data = self.leer_datos()
        for u in data["usuarios"]:
            if u["cedula"] == cedula:
                return True
        return False

    # ---------------------------
    # GUARDAR USUARIO (FORMATO CORRECTO)
    # ---------------------------
    def guardar_usuario(self, data_usuario):
        data = self.leer_datos()

        # Si ya existe → NO lo duplica
        for u in data["usuarios"]:
            if u["cedula"] == data_usuario["cedula"]:
                return False

        data_usuario["fecha_registro"] = str(datetime.now())

        data["usuarios"].append(data_usuario)
        self.guardar_datos(data)

        return True

    # ---------------------------
    # OBTENER USUARIOS (ESTA ERA LA QUE TE FALTABA)
    # ---------------------------
    def obtener_usuarios(self):
        data = self.leer_datos()
        return data.get("usuarios", [])