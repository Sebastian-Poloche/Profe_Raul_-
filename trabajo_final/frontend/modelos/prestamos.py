from .api_cliente import APICliente


class PrestamoModel:

    def __init__(self):
        self.api = APICliente()

    def listar(self):
        return self.api.get("prestamos/")

    def crear(self, data):
        return self.api.post("prestamos/", data)

    def actualizar(self, numero, data):
        return self.api.put(f"prestamos/{numero}/", data)

    def eliminar(self, numero):
        return self.api.delete(f"prestamos/{numero}/")
