import os
from usuarios import UsuarioManager
from datetime import datetime

class UsuarioServicio:

    def __init__(self):
        self.usuario_manager = UsuarioManager()

    def obtener_usuarios_con_estado(self):

        usuarios = self.usuario_manager.obtener_usuarios()
        lista = []

        for u in usuarios:

            cedula = u["cedula"]

            ruta = os.path.join("uploads", cedula)

            archivos = []
            if os.path.exists(ruta):
                archivos = os.listdir(ruta)

            lista.append({
                "cedula": cedula,
                "nombre": u.get("nombre"),
                "torre": u.get("torre"),
                "apto": u.get("apto"),
                "nombre_propiedad": u.get("nombre_propiedad"),
                "celular": u.get("celular"),
                "correo": u.get("correo"),
                "nombre_propietario": u.get("nombre_propietario"),
                "mail_propietario": u.get("mail_propietario"),
                "celular1": u.get("celular1"),
                "nombre_arrendatario": u.get("nombre_arrendatario"),
                "vehiculo": u.get("vehiculo"),
                "placa": u.get("placa"),
                "marca": u.get("marca"),
                "modelo": u.get("modelo"),
                "color": u.get("color"),
                "archivos": archivos
            })

        return lista