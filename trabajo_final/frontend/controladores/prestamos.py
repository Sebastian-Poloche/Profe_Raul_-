"""
Controlador de operaciones sobre préstamos.

Proporciona una interfaz para gestionar el ciclo de vida de préstamos
(crear, leer, actualizar, eliminar) mediante la API RESTful del backend.
"""

from .api_cliente import APIClient


class PrestamoModel:
    """
    Controlador para operaciones CRUD de préstamos.

    Encapsula la comunicación con la API para operaciones sobre el registro
    de préstamos de herramientas, proporcionando métodos simples para acceder
    a la funcionalidad del backend.
    """

    def __init__(self):
        """Inicializar controlador de préstamos con cliente API."""
        self.api = APIClient()

    def listar(self):
        """
        Obtener lista de todos los préstamos.

        Returns:
            tuple: (datos, error) donde datos es lista de préstamos
                   o None si hay error, y error es mensaje de error o None.
        """
        return self.api.get("prestamos/")

    def crear(self, data):
        """
        Crear un nuevo préstamo.

        Args:
            data (dict): Diccionario con los datos del préstamo (número,
                        código herramienta, responsable, fechas).

        Returns:
            tuple: (respuesta, error) donde respuesta contiene los datos
                   creados o None si hay error.
        """
        return self.api.post("prestamos/", data)

    def actualizar(self, numero, data):
        """
        Actualizar un préstamo existente.

        Args:
            numero (str): Número único del préstamo a actualizar.
            data (dict): Diccionario con los datos a actualizar.

        Returns:
            tuple: (respuesta, error) con los datos actualizados o error.
        """
        return self.api.put(f"prestamos/{numero}/", data)

    def eliminar(self, numero):
        """
        Eliminar un préstamo.

        Args:
            numero (str): Número único del préstamo a eliminar.

        Returns:
            tuple: (respuesta, error) donde respuesta es True si se eliminó,
                   o error si falló la operación.
        """
        return self.api.delete(f"prestamos/{numero}/")

