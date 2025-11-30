import threading
import time
import os
from datetime import datetime
import json


def ejecutar_backup():
    """Ejecutar backup de los datos"""
    try:
        carpeta = os.path.join(os.path.dirname(__file__), "..", "backups")
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        
        nombre = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        ruta = os.path.join(carpeta, nombre)
        
        # Intentar obtener datos de la API
        try:
            from . import api_cliente
            client = api_cliente.APIClient()
            
            herramientas, _ = client.get("herramientas/")
            prestamos, _ = client.get("prestamos/")
            
            backup_data = {
                "timestamp": datetime.now().isoformat(),
                "herramientas": herramientas or [],
                "prestamos": prestamos or []
            }
        except:
            backup_data = {
                "timestamp": datetime.now().isoformat(),
                "herramientas": [],
                "prestamos": [],
                "error": "No se pudo conectar a la API"
            }
        
        # Guardar backup
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        # Limpiar backups antiguos (mantener últimos 10)
        try:
            backups = sorted([f for f in os.listdir(carpeta) if f.startswith("backup_")],
                           reverse=True)
            for backup_antiguo in backups[10:]:
                os.remove(os.path.join(carpeta, backup_antiguo))
        except:
            pass
            
    except Exception as e:
        print(f"Error en backup: {e}")


def iniciar_hilo_backup():
    """Iniciar hilo de backup automático"""
    intervalo = int(os.getenv("INTERVALO_BACKUP_SEG", "300"))  # 5 minutos por defecto
    
    def backup_loop():
        while True:
            try:
                ejecutar_backup()
                time.sleep(intervalo)
            except Exception as e:
                print(f"Error en loop de backup: {e}")
                time.sleep(10)  # Reintentar en 10 segundos
    
    hilo = threading.Thread(target=backup_loop, daemon=True, name="BackupThread")
    hilo.start()

