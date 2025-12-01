"""
Cliente HTTP para comunicación con la API REST del backend.

Proporciona métodos para realizar operaciones CRUD contra la API Django,
con manejo robusto de errores y excepciones de red.
"""

import requests
import json
import sys
from pathlib import Path

# Agregar raíz del proyecto al path para importar config
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import get_backend_url, HTTP_TIMEOUT


class APIClient:
    """
    Cliente HTTP para comunicarse con la API REST del backend IHEP.
    
    Proporciona métodos para realizar peticiones GET, POST, PUT y DELETE,
    con manejo centralizado de errores y timeouts configurables.
    """

    def __init__(self):
        """
        Inicializa el cliente con la configuración centralizada.
        
        Obtiene la URL base del backend y el timeout desde config.py,
        permitiendo que estos valores sean configurables globalmente.
        """
        self.base_url = get_backend_url()
        self.timeout = HTTP_TIMEOUT

    def get(self, endpoint: str):
        """
        Realiza una petición GET a la API.
        
        Args:
            endpoint (str): Ruta relativa del endpoint (ej: "herramientas/")
            
        Returns:
            tuple: (datos, error) donde datos es el JSON de respuesta
                   o None si hay error, y error es el mensaje de error o None
        """
        try:
            url = self.base_url + endpoint
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json(), None

        except requests.exceptions.Timeout:
            return None, "Tiempo de conexión agotado"
        except requests.exceptions.ConnectionError:
            return None, "No se puede conectar al servidor"
        except requests.exceptions.HTTPError as e:
            return None, f"Error HTTP {response.status_code}: {response.text}"
        except requests.exceptions.RequestException as e:
            return None, str(e)
        except json.JSONDecodeError:
            return None, "Error al decodificar respuesta JSON"
        except Exception as e:
            return None, str(e)

    def post(self, endpoint: str, data: dict):
        """
        Realiza una petición POST a la API para crear recursos.
        
        Args:
            endpoint (str): Ruta relativa del endpoint
            data (dict): Datos a enviar en formato JSON
            
        Returns:
            tuple: (datos, error) donde datos es el JSON de respuesta
                   o None si hay error, y error es el mensaje de error o None
        """
        try:
            url = self.base_url + endpoint
            response = requests.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json(), None

        except requests.exceptions.Timeout:
            return None, "Tiempo de conexión agotado"
        except requests.exceptions.ConnectionError:
            return None, "No se puede conectar al servidor"
        except requests.exceptions.HTTPError as e:
            return None, f"Error HTTP {response.status_code}: {response.text}"
        except requests.exceptions.RequestException as e:
            return None, str(e)
        except json.JSONDecodeError:
            return None, "Error al decodificar respuesta JSON"
        except Exception as e:
            return None, str(e)

    def put(self, endpoint: str, data: dict):
        """
        Realiza una petición PUT a la API para actualizar recursos.
        
        Args:
            endpoint (str): Ruta relativa del endpoint
            data (dict): Datos actualizados en formato JSON
            
        Returns:
            tuple: (datos, error) donde datos es el JSON de respuesta
                   o None si hay error, y error es el mensaje de error o None
        """
        try:
            url = self.base_url + endpoint
            response = requests.put(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json(), None

        except requests.exceptions.Timeout:
            return None, "Tiempo de conexión agotado"
        except requests.exceptions.ConnectionError:
            return None, "No se puede conectar al servidor"
        except requests.exceptions.HTTPError as e:
            return None, f"Error HTTP {response.status_code}: {response.text}"
        except requests.exceptions.RequestException as e:
            return None, str(e)
        except json.JSONDecodeError:
            return None, "Error al decodificar respuesta JSON"
        except Exception as e:
            return None, str(e)

    def delete(self, endpoint: str):
        """
        Realiza una petición DELETE a la API para eliminar recursos.
        
        Args:
            endpoint (str): Ruta relativa del endpoint
            
        Returns:
            tuple: (éxito, error) donde éxito es True si se eliminó correctamente,
                   o None si hay error, y error es el mensaje de error o None
        """
        try:
            url = self.base_url + endpoint
            response = requests.delete(url, timeout=self.timeout)
            response.raise_for_status()
            return True, None

        except requests.exceptions.Timeout:
            return None, "Tiempo de conexión agotado"
        except requests.exceptions.ConnectionError:
            return None, "No se puede conectar al servidor"
        except requests.exceptions.HTTPError as e:
            return None, f"Error HTTP {response.status_code}: {response.text}"
        except requests.exceptions.RequestException as e:
            return None, str(e)
        except Exception as e:
            return None, str(e)


# Instancia global del cliente para uso en funciones auxiliares
_client = APIClient()


# ===== Funciones auxiliares de compatibilidad =====
# Estas funciones permiten usar el cliente de forma más simple en otros módulos

def obtener_herramientas():
    """Obtiene la lista de todas las herramientas del sistema."""
    data, error = _client.get("herramientas/")
    if error:
        raise Exception(error)
    return data


def crear_herramienta(data):
    """Crea una nueva herramienta en el sistema."""
    result, error = _client.post("herramientas/", data)
    if error:
        raise Exception(error)
    return result


def actualizar_herramienta(id_herramienta, data):
    """Actualiza una herramienta existente."""
    result, error = _client.put(f"herramientas/{id_herramienta}/", data)
    if error:
        raise Exception(error)
    return result


def eliminar_herramienta(id_herramienta):
    """Elimina una herramienta del sistema."""
    result, error = _client.delete(f"herramientas/{id_herramienta}/")
    if error:
        raise Exception(error)
    return result


def obtener_prestamos():
    """Obtiene la lista de todos los préstamos del sistema."""
    data, error = _client.get("prestamos/")
    if error:
        raise Exception(error)
    return data


def crear_prestamo(data):
    """Crea un nuevo préstamo en el sistema."""
    result, error = _client.post("prestamos/", data)
    if error:
        raise Exception(error)
    return result


def actualizar_prestamo(id_prestamo, data):
    """Actualiza un préstamo existente."""
    result, error = _client.put(f"prestamos/{id_prestamo}/", data)
    if error:
        raise Exception(error)
    return result


def eliminar_prestamo(id_prestamo):
    """Elimina un préstamo del sistema."""
    result, error = _client.delete(f"prestamos/{id_prestamo}/")
    if error:
        raise Exception(error)
    return result