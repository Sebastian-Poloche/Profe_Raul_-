#!/usr/bin/env python
"""
Script de prueba para verificar la conexión entre frontend y backend
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_herramientas():
    try:
        print("=" * 60)
        print("PRUEBA DE HERRAMIENTAS")
        print("=" * 60)
        
        
        print(" GET /herramientas/")
        response = requests.get(f"{BASE_URL}/herramientas/", timeout=5)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Respuesta: {json.dumps(data, indent=2)}")
        
    except Exception as e:
        print(f" Error: {str(e)}")

def test_prestamos():
    try:
        print("\n" + "=" * 60)
        print("PRUEBA DE PRÉSTAMOS")
        print("=" * 60)
        
        # GET
        print("GET /prestamos/")
        response = requests.get(f"{BASE_URL}/prestamos/", timeout=5)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Respuesta: {json.dumps(data, indent=2)}")
        
    except Exception as e:
        print(f" Error: {str(e)}")

def test_create_herramienta():
    """Probar crear herramienta"""
    try:
        print("\n" + "=" * 60)
        print("PRUEBA DE CREAR HERRAMIENTA")
        print("=" * 60)
        
        data = {
            "codigo": "H001",
            "nombre": "Taladro",
            "categoria": "Enviar",
            "ubicacion": "Almacén A",
            "estado": "Disponible"
        }
        
        print(f"\n POST /herramientas/")
        print(f"Datos: {json.dumps(data, indent=2)}")
        
        response = requests.post(f"{BASE_URL}/herramientas/", json=data, timeout=5)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Respuesta: {json.dumps(result, indent=2)}")
        
    except Exception as e:
        print(f" Error: {str(e)}")

if __name__ == "__main__":
    print("\n INICIANDO PRUEBAS DE API\n")
    
    try:
        response = requests.get(f"{BASE_URL}/herramientas/", timeout=2)
        print(f"✓ Conexión exitosa: {BASE_URL}")
    except requests.exceptions.ConnectionError:
        print(f" No se puede conectar a {BASE_URL}")
        print("Asegúrate de que Django esté corriendo con: python manage.py runserver")
        exit(1)
    except Exception as e:
        print(f" Error de conexión: {e}")
        exit(1)
    
    test_herramientas()
    test_prestamos()
    test_create_herramienta()
    
    print("\n" + "=" * 60)
    print(" PRUEBAS COMPLETADAS")
    print("=" * 60)
