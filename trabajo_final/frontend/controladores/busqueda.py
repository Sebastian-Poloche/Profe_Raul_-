"""Controlador de búsqueda para el frontend IHEP.

Proporciona funcionalidad de búsqueda de herramientas y préstamos.
"""

from .api_cliente import APIClient


class BusquedaModel:
    """
    Modelo que gestiona las búsquedas en la aplicación.
    
    Encapsula la lógica para realizar búsquedas de herramientas
    y préstamos a través de la API del backend.
    """

    def __init__(self):
        """
        Inicializa el modelo de búsqueda.
        
        Crea una instancia del cliente API para comunicarse con el backend.
        """
        self.api = APIClient()

    def buscar(self, tipo, termino):
        """
        Realiza una búsqueda según el tipo y término proporcionados.
        
        Args:
            tipo (str): Tipo de búsqueda ('herramientas' o 'prestamos')
            termino (str): Término o palabra clave a buscar
            
        Returns:
            tuple: (resultados, error) donde resultados es la lista de elementos
                   encontrados o None si hay error
        """
        endpoint = f"buscar/?tipo={tipo}&q={termino}"
        return self.api.get(endpoint)
