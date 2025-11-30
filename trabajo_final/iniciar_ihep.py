#!/usr/bin/env python
"""
Script para iniciar el sistema IHEP completo
Inicia Backend y Frontend en paralelo
"""
import subprocess
import time
import os
import signal
import sys
from pathlib import Path

def print_header(text):
    print(f"\n{'='*40}")
    print(f"  {text}")
    print(f"{'='*40}\n")

def main():
    print_header("IHEP - Sistema de Herramientas")
    

    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    backend_dir = project_root / "backend"
    
    if not venv_python.exists():
        print(" ERROR: No se encuentra el entorno virtual")
        sys.exit(1)
    
    print(" Entorno virtual encontrado")
    print(f" Directorio de trabajo: {project_root}")
    
    backend_process = None
    frontend_process = None
    
    try:
        print("\n[1/2] Iniciando Backend Django...")
        backend_cmd = [
            str(venv_python),
            "manage.py",
            "runserver",
            "127.0.0.1:8000"
        ]
        backend_process = subprocess.Popen(
            backend_cmd,
            cwd=str(backend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
        )
        print(" Backend iniciado (PID: {})".format(backend_process.pid))
        

        time.sleep(4)
        
        print("\n[2/2] Iniciando Frontend...")
        frontend_cmd = [
            str(venv_python),
            "main.py"
        ]
        frontend_process = subprocess.Popen(
            frontend_cmd,
            cwd=str(project_root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
        )
        print("Frontend iniciado (PID: {})".format(frontend_process.pid))
        
        print_header(" Sistema  iniciado correctamente")
        print("Backend: http://127.0.0.1:8000")
        print("API: http://127.0.0.1:8000/api/")
        print("\n Sistema en ejecución...")
        print("Presiona CTRL+C para detener\n")
        

        while True:
            time.sleep(1)
          
            if backend_process and backend_process.poll() is not None:
                print(" Backend se detuvo")
                break
            if frontend_process and frontend_process.poll() is not None:
                print(" Frontend cerrado por el usuario")
                break
    
    except KeyboardInterrupt:
        print(" Deteniendo sistema...")
    
    finally:
        if backend_process and backend_process.poll() is None:
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
            except:
                backend_process.kill()
        
        if frontend_process and frontend_process.poll() is None:
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=5)
            except:
                frontend_process.kill()
        
        print("✓ Sistema detenido\n")

if __name__ == "__main__":
    main()
