import json
from datetime import datetime


class UsuarioManager:

    def __init__(self, archivo='usuarios.json'):
        self.archivo = archivo

    # ---------------------------
    # Cargar datos
    # ---------------------------
    def cargar_datos(self):
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"usuarios": []}

    # ---------------------------
    # Guardar datos
    # ---------------------------
    def guardar_datos(self, data):
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    # ---------------------------
    # Guardar usuario COMPLETO
    # ---------------------------
    def guardar_usuario(self, cedula, nombre, torre, apto, nombre_propiedad,
                        celular, correo, nombre_propietario, mail_propietario,
                        celular1, nombre_arrendatario, vehiculo, placa,
                        marca, modelo, color):

        data = self.cargar_datos()

        # ⚠️ Validar si ya existe
        for u in data["usuarios"]:
            if u["cedula"] == cedula:
                return  # ya existe, no duplicar

        # ✅ Crear nuevo usuario
        nuevo_usuario = {
            "cedula": cedula,
            "nombre": nombre,
            "torre": torre,
            "apto": apto,
            "nombre_propiedad": nombre_propiedad,
            "celular": celular,
            "correo": correo,
            "nombre_propietario": nombre_propietario,
            "mail_propietario": mail_propietario,
            "celular1": celular1,
            "nombre_arrendatario": nombre_arrendatario,
            "vehiculo": vehiculo,
            "placa": placa,
            "marca": marca,
            "modelo": modelo,
            "color": color,
            "fecha_registro": str(datetime.now())
        }

        data["usuarios"].append(nuevo_usuario)

        self.guardar_datos(data)

    # ---------------------------
    # Obtener usuarios
    # ---------------------------
    def obtener_usuarios(self):
        data = self.cargar_datos()
        return data["usuarios"]

    # ---------------------------
    # Validar si existe
    # ---------------------------
    def usuario_existe(self, cedula):
        usuarios = self.obtener_usuarios()

        for u in usuarios:
            if u["cedula"] == cedula:
                return True

        return False