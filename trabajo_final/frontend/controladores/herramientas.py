"""
Controlador de operaciones sobre herramientas.

Proporciona una interfaz para gestionar el ciclo de vida de herramientas
(crear, leer, actualizar, eliminar) mediante la API RESTful del backend.
"""

from .api_cliente import APIClient


class HerramientaModel:
    """
    Controlador para operaciones CRUD de herramientas.

    Encapsula la comunicación con la API para operaciones sobre el inventario
    de herramientas, proporcionando métodos simples para acceder a la
    funcionalidad del backend.
    """

    def __init__(self):
        """Inicializar controlador de herramientas con cliente API."""
        self.api = APIClient()

    def listar(self):
        """
        Obtener lista de todas las herramientas.

        Returns:
            tuple: (datos, error) donde datos es lista de herramientas
                   o None si hay error, y error es mensaje de error o None.
        """
        return self.api.get("herramientas/")

    def crear(self, data):
        """
        Crear una nueva herramienta.

        Args:
            data (dict): Diccionario con los datos de la herramienta
                        (código, nombre, categoría, ubicación, estado).

        Returns:
            tuple: (respuesta, error) donde respuesta contiene los datos
                   creados o None si hay error.
        """
        return self.api.post("herramientas/", data)

    def actualizar(self, codigo, data):
        """
        Actualizar una herramienta existente.

        Args:
            codigo (str): Código único de la herramienta a actualizar.
            data (dict): Diccionario con los datos a actualizar.

        Returns:
            tuple: (respuesta, error) con los datos actualizados o error.
        """
        return self.api.put(f"herramientas/{codigo}/", data)

    def eliminar(self, codigo):
        """
        Eliminar una herramienta.

        Args:
            codigo (str): Código único de la herramienta a eliminar.

        Returns:
            tuple: (respuesta, error) donde respuesta es True si se eliminó,
                   o error si falló la operación.
        """
        return self.api.delete(f"herramientas/{codigo}/")


