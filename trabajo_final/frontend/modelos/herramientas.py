""" Módulo de Herramientas - - - 
Registro, edición, consulta y eliminación de herramientas. 
Campos mínimos: código, nombre, categoría, ubicación, estado, created_at, updated_at. 
Borrado físico (eliminación permanente)."""

from .api_cliente import APIClient


class HerramientaModel:

    def __init__(self):
        self.api = APIClient()

    def listar(self):
        return self.api.get("herramientas/")

    def crear(self, data):
        return self.api.post("herramientas/", data)

    def actualizar(self, codigo, data):
        return self.api.put(f"herramientas/{codigo}/", data)

    def eliminar(self, codigo):
        return self.api.delete(f"herramientas/{codigo}/")

