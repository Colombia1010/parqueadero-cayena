"""
services/usuario_servicio.py
─────────────────────────────
Capa de servicio: combina managers y utilidades para
entregar datos listos para los templates (lógica de negocio).
"""

from app.managers.usuario_manager  import UsuarioManager
from app.utils.archivos            import listar_documentos


class UsuarioServicio:

    def __init__(self):
        self.manager = UsuarioManager()

    def obtener_usuarios_con_estado(self) -> list[dict]:
        """
        Retorna todos los usuarios enriquecidos con:
        - lista de documentos subidos
        - estado: 'Completo' o 'Sin documentos'
        """
        usuarios = self.manager.obtener_todos()

        for usuario in usuarios:
            cedula            = usuario.get("cedula", "")
            archivos          = listar_documentos(cedula)
            usuario["archivos"] = archivos
            usuario["estado"]   = "Completo" if archivos else "Sin documentos"

        return usuarios
