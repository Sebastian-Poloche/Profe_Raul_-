@echo off
REM 

echo.
echo 
echo IHEP - Sistema de Herramientas
echo 
echo.

REM 
if not exist ".venv" (
    echo ERROR: No se encuentra el entorno virtual
    echo Por favor ejecutar desde: c:\Users\chatarra\Documents\Profe_Raul_-\trabajo_final
    pause
    exit /b 1
)

REM 
echo  Iniciando Backend Django...
start "IHEP Backend" cmd /k ".venv\Scripts\python.exe backend\manage.py runserver 127.0.0.1:8000"

REM 
echo [hola] Esperando que el servidor inicie...
timeout /t 3 /nobreak

REM 
echo [2/2] Iniciando Frontend...
start "IHEP Frontend" cmd /k ".venv\Scripts\python.exe main.py"

echo.
echo 
echo Sistema IHEP iniciado correctamente
echo 
echo.
echo Backend: http://127.0.0.1:8000
echo.
pause
