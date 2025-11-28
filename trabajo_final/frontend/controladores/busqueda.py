from .api_cliente import APIClient


class BusquedaModel:

    def __init__(self):
        self.api = APIClient()

    def buscar(self, tipo, termino):
        endpoint = f"buscar/?tipo={tipo}&q={termino}"
        return self.api.get(endpoint)
