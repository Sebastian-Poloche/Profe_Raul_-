"""
Módulo de gestión de respaldos automáticos.

Proporciona funcionalidad para ejecutar respaldos automáticos de herramientas y
préstamos en intervalos regulares mediante un thread daemon, evitando que bloquee
la interfaz gráfica de usuario.
"""

import json
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

# Agregar la raíz del proyecto al path para importar configuración
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import (
    BACKUP_ENCODING,
    BACKUP_MAX_FILES,
    BACKUP_TIMESTAMP_FORMAT,
    get_backup_directory,
    get_backup_interval,
)


def ejecutar_backup():
    """
    Ejecutar respaldo de datos de herramientas y préstamos.

    Obtiene datos de la API RESTful y los guarda en archivos JSON con
    timestamp. Limpia automáticamente respaldos antiguos manteniendo solo
    los últimos N archivos configurados en BACKUP_MAX_FILES.

    Returns:
        bool: True si el respaldo fue exitoso, False en caso contrario.
    """
    try:
        carpeta = get_backup_directory()
        if not carpeta.exists():
            carpeta.mkdir(parents=True, exist_ok=True)

        nombre = f"backup_{datetime.now().strftime(BACKUP_TIMESTAMP_FORMAT)}.json"
        ruta = carpeta / nombre

        # Intentar obtener datos de la API
        try:
            from . import api_cliente
            cliente = api_cliente.APIClient()

            herramientas, _ = cliente.get("herramientas/")
            prestamos, _ = cliente.get("prestamos/")

            datos_backup = {
                "timestamp": datetime.now().isoformat(),
                "herramientas": herramientas or [],
                "prestamos": prestamos or []
            }
        except Exception as error_api:
            # Si falla conexión a API, guardar respaldo con error registrado
            datos_backup = {
                "timestamp": datetime.now().isoformat(),
                "herramientas": [],
                "prestamos": [],
                "error": f"No se pudo conectar a la API: {str(error_api)}"
            }

        # Guardar respaldo en disco
        with open(ruta, "w", encoding=BACKUP_ENCODING) as archivo:
            json.dump(datos_backup, archivo, indent=2, ensure_ascii=False)

        # Limpiar respaldos antiguos (mantener últimos N archivos)
        try:
            respaldos = sorted(
                [f for f in carpeta.iterdir() if f.name.startswith("backup_")],
                reverse=True
            )
            # Eliminar respaldos que excedan el límite configurado
            for respaldo_antiguo in respaldos[BACKUP_MAX_FILES:]:
                respaldo_antiguo.unlink()
        except Exception as error_limpieza:
            print(f"Advertencia: Error limpiando respaldos antiguos: {error_limpieza}")

        return True

    except Exception as error:
        print(f"Error en respaldo: {error}")
        return False



def iniciar_hilo_backup():
    """
    Iniciar thread daemon de respaldo automático.

    Ejecuta el respaldo de datos a intervalos regulares configurables sin
    bloquear la interfaz gráfica de usuario. El thread se ejecuta como daemon
    permitiendo que la aplicación se cierre normalmente sin esperar a su
    terminación.
    """
    intervalo = get_backup_interval()

    def loop_backup():
        """
        Loop principal del thread de respaldo.

        Ejecuta respaldos indefinidamente a intervalos especificados.
        En caso de error, reininta después de 10 segundos.
        """
        while True:
            try:
                ejecutar_backup()
                time.sleep(intervalo)
            except Exception as error:
                print(f"Error en loop de respaldo: {error}")
                # Esperar 10 segundos antes de reintentar
                time.sleep(10)

    hilo = threading.Thread(target=loop_backup, daemon=True, name="BackupThread")
    hilo.start()


