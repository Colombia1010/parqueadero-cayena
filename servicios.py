import os
from usuarios import UsuarioManager

class UsuarioServicio:

    def __init__(self):
        self.usuario_manager = UsuarioManager()

    # ---------------------------
    # OBTENER USUARIOS CON ESTADO Y ARCHIVOS
    # ---------------------------
    def obtener_usuarios_con_estado(self):
        usuarios = self.usuario_manager.obtener_usuarios()

        for u in usuarios:
            cedula = u.get("cedula")

            ruta = os.path.join("uploads", cedula)

            if os.path.exists(ruta):
                archivos = os.listdir(ruta)
            else:
                archivos = []

            u["archivos"] = archivos
            u["estado"] = "Completo" if archivos else "Sin documentos"

        return usuarios