"""
Configuración centralizada del sistema IHEP.

Módulo que centraliza todas las variables de configuración del sistema IHEP,
permitiendo su modificación sin alterar el código fuente. Utiliza variables
de entorno como valores de fallback a configuraciones por defecto, proporcionando
flexibilidad para diferentes entornos (desarrollo, producción, pruebas).

Variables de entorno soportadas:
    - BACKEND_URL: URL de la API del backend (default: http://127.0.0.1:8000/api)
    - BACKEND_PORT: Puerto del servidor Django (default: 8000)
    - BACKEND_HOST: Host del servidor (default: 127.0.0.1)
    - INTERVALO_BACKUP_SEG: Intervalo de respaldo en segundos (default: 300)
"""

import os
from pathlib import Path

# Raíz del proyecto (directorio donde reside este archivo)
PROJECT_ROOT = Path(__file__).parent

# Directorio del backend Django
BACKEND_DIR = PROJECT_ROOT / "backend"

# Directorio del frontend con interfaz gráfica
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# Directorio donde se almacenan respaldos automáticos
BACKUP_DIR = FRONTEND_DIR / "backups"

# Ruta de la base de datos SQLite
DB_PATH = BACKEND_DIR / "db.sqlite3"


# URL base de la API RESTful que utiliza el frontend para comunicarse
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/api")

# Puerto en el que escucha el servidor Django
BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))

# Host/dirección IP donde se ejecuta el servidor
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")

# Garantizar que la URL siempre termina con barra diagonal para consistencia
if not BACKEND_URL.endswith("/"):
    BACKEND_URL += "/"


# Ancho inicial de la ventana principal en píxeles
FRONTEND_WINDOW_WIDTH = 1200

# Alto inicial de la ventana principal en píxeles
FRONTEND_WINDOW_HEIGHT = 720

# Timeout para peticiones HTTP hacia la API en segundos
HTTP_TIMEOUT = 5



# Intervalo entre respaldos automáticos en segundos
# Por defecto: 300 segundos (5 minutos)
# Puede modificarse mediante variable de entorno INTERVALO_BACKUP_SEG
BACKUP_INTERVAL_SECONDS = int(os.getenv("INTERVALO_BACKUP_SEG", 300))

# Número máximo de archivos de respaldo a mantener
# Los respaldos más antiguos se eliminan automáticamente
BACKUP_MAX_FILES = 10

# Formato de timestamp para nombres de archivos de respaldo
# Ejemplo: backup_20251130_143500.json (formato YYYYMMDDhhmmss)
BACKUP_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# Formato de los archivos de respaldo (actualmente JSON)
BACKUP_FORMAT = "json"

# Codificación de caracteres para archivos de respaldo
BACKUP_ENCODING = "utf-8"


# ============================================================================
# FUNCIONES GETTER (Accessores para configuración)
# ============================================================================

def get_backend_url():
    """
    Obtener la URL completa del servidor backend.

    Retorna la URL configurada para acceder a la API RESTful del backend.
    Garantiza que termina con barra diagonal.

    Returns:
        str: URL completa del API RESTful del backend
    """
    return BACKEND_URL


def get_backup_interval():
    """
    Obtener el intervalo de respaldo en segundos.

    Retorna el tiempo que debe esperar entre ejecuciones de respaldo automático.

    Returns:
        int: Intervalo en segundos entre respaldos automáticos
    """
    return BACKUP_INTERVAL_SECONDS


def get_backup_directory():
    """
    Obtener la ruta del directorio de respaldos.

    Retorna el Path del directorio donde se almacenan los archivos de respaldo
    automático de herramientas y préstamos.

    Returns:
        Path: Objeto Path del directorio de respaldos
    """
    return BACKUP_DIR

