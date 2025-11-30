import os
import requests
import json


class APIClient:
    """Cliente para comunicarse con la API REST del backend"""
    
    def __init__(self):
        # Usar http://127.0.0.1:8000/api/ como URL base
        base_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/api")
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        self.timeout = 5

    def get(self, endpoint: str):
        """GET request"""
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
        """POST request"""
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
        """PUT request"""
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
        """DELETE request"""
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


# Funciones de compatibilidad (por si se usan directamente)
_client = APIClient()

def obtener_herramientas():
    data, error = _client.get("herramientas/")
    if error:
        raise Exception(error)
    return data

def crear_herramienta(data):
    result, error = _client.post("herramientas/", data)
    if error:
        raise Exception(error)
    return result

def actualizar_herramienta(id_herramienta, data):
    result, error = _client.put(f"herramientas/{id_herramienta}/", data)
    if error:
        raise Exception(error)
    return result

def eliminar_herramienta(id_herramienta):
    result, error = _client.delete(f"herramientas/{id_herramienta}/")
    if error:
        raise Exception(error)
    return result

def obtener_prestamos():
    data, error = _client.get("prestamos/")
    if error:
        raise Exception(error)
    return data

def crear_prestamo(data):
    result, error = _client.post("prestamos/", data)
    if error:
        raise Exception(error)
    return result

def actualizar_prestamo(id_prestamo, data):
    result, error = _client.put(f"prestamos/{id_prestamo}/", data)
    if error:
        raise Exception(error)
    return result

def eliminar_prestamo(id_prestamo):
    result, error = _client.delete(f"prestamos/{id_prestamo}/")
    if error:
        raise Exception(error)
    return result

