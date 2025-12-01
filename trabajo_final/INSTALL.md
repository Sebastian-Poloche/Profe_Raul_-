# Guía de Instalación y Configuración - IHEP

## Prerrequisitos

Asegúrate de contar con lo siguiente antes de comenzar:

1. Python 3.12.3 o superior instalado
2. Acceso a línea de comandos (Terminal/PowerShell)
3. Conexión a internet (para descargar dependencias)
4. Aproximadamente 200 MB de espacio en disco disponible

### Verificar Instalación de Python

```bash
python --version
# o
python3 --version
```

Debe mostrar Python 3.12.3 o superior.

## Pasos de Instalación

### Paso 1: Descargar el Proyecto

Descarga o clona el proyecto en tu máquina local:

```bash
cd ruta/deseada
# O si usas git:
git clone https://github.com/usuario/IHEP.git
cd IHEP
```

### Paso 2: Crear Entorno Virtual

El entorno virtual aísla las dependencias del proyecto de la instalación global de Python.

**En Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**En Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**En Windows (Command Prompt):**

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

Después de ejecutar, deberías ver `(.venv)` al inicio de tu línea de comandos.

### Paso 3: Actualizar pip

Asegúrate de tener la última versión de pip:

```bash
pip install --upgrade pip
```

### Paso 4: Instalar Dependencias

Instala todas las dependencias listadas en requirements.txt:

```bash
pip install -r requirements.txt
```

Este proceso descargará e instalará:
- Django 5.2.8
- Django REST Framework 3.16.1
- django-cors-headers 4.9.0
- requests 2.32.5

El proceso tardará algunos minutos dependiendo de tu conexión.

### Paso 5: Configurar Base de Datos

Navega al directorio backend y crea las tablas en la base de datos:

```bash
cd backend
python manage.py migrate
```

Deberías ver mensajes indicando que las migraciones fueron aplicadas exitosamente.

**Salida esperada:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, api
Running migrations:
  Applying admin.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Paso 6 (Opcional): Crear Superusuario para Django Admin

Si deseas acceder a la interfaz administrativa de Django:

```bash
python manage.py createsuperuser
```

Se te pedirá:
- Nombre de usuario
- Email
- Contraseña

Este paso es opcional y solo necesario si deseas administrar datos directamente en Django Admin.

## Ejecución del Sistema

### Opción A: Ejecución Automática (Recomendada)

Desde el directorio raíz del proyecto (no dentro de backend):

```bash
# Primero, asegúrate de estar en el directorio correcto
cd /ruta/al/proyecto

# Activa el entorno virtual si no está activado
source .venv/bin/activate  # Linux/macOS
# o
.venv\Scripts\activate     # Windows

# Ejecuta el script de inicio
python iniciar_ihep.py
```

Este script iniciará automáticamente:
1. El servidor Django backend en http://127.0.0.1:8000
2. La interfaz gráfica Tkinter en una ventana separada
3. El sistema de respaldos automáticos en segundo plano

### Opción B: Ejecución Manual (Para Desarrollo)

**Terminal 1 - Iniciar Backend:**

```bash
cd backend
python manage.py runserver 127.0.0.1:8000
```

**Salida esperada:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
November 30, 2025 - 10:00:00
Django version 5.2.8, using settings 'ch_sp.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

**Terminal 2 - Iniciar Frontend:**

En una nueva ventana de terminal:

```bash
# Vuelve al directorio raíz
cd ..

# Activa el entorno virtual si no está activado
source .venv/bin/activate  # Linux/macOS
# o
.venv\Scripts\activate     # Windows

# Inicia la interfaz gráfica
python main.py
```

Debería aparecer la ventana de la aplicación IHEP.

## Verificación de Instalación

### Verificar Backend

Abre tu navegador y visita:

```
http://127.0.0.1:8000/api/herramientas/
```

Deberías ver una respuesta JSON con una lista vacía o con datos existentes:

```json
{
  "results": [
    {
      "id": 1,
      "codigo": "HER0001",
      "nombre": "Martillo",
      "categoria": "Enviar",
      "estado": "Disponible",
      ...
    }
  ],
  "count": 1
}
```

### Verificar Interfaz Gráfica

La ventana de la aplicación debe estar abierta, mostrando:
- Dos pestañas: "Herramientas" y "Préstamos"
- Tablas vacías (si es la primera ejecución)
- Botones de operaciones (Crear, Editar, Eliminar)

## Configuración Post-Instalación

### 1. Modificar Configuración Base

Edita `config.py` para cambiar parámetros como:
- URL del backend
- Puerto del servidor
- Intervalo de respaldos

### 2. Variables de Entorno (Opcional)

Crea un archivo `.env` en el directorio raíz:

```bash
BACKEND_URL=http://127.0.0.1:8000/api
BACKEND_PORT=8000
BACKEND_HOST=127.0.0.1
INTERVALO_BACKUP_SEG=300
```

El sistema leerá automáticamente estas variables si existen.

### 3. Modificar Configuración de Django

Edita `backend/ch_sp/settings.py` para:
- Cambiar SECRET_KEY (importante para producción)
- Modificar ALLOWED_HOSTS
- Configurar bases de datos adicionales

## Solución de Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'django'"

**Causa:** Las dependencias no están instaladas o el entorno virtual no está activado.

**Solución:**
```bash
# Asegúrate de estar en el entorno virtual
source .venv/bin/activate  # Linux/macOS
# o
.venv\Scripts\activate     # Windows

# Reinstala las dependencias
pip install -r requirements.txt
```

### Error: "Port 8000 is already in use"

**Causa:** Otro proceso está usando el puerto 8000.

**Solución en Linux/macOS:**
```bash
# Identifica qué proceso usa el puerto
lsof -i :8000

# Termina el proceso (si es necesario)
kill -9 <PID>

# O usa otro puerto
python manage.py runserver 127.0.0.1:8001
```

**Solución en Windows:**
```powershell
# Identifica qué proceso usa el puerto
netstat -ano | findstr :8000

# Termina el proceso
taskkill /PID <PID> /F

# O usa otro puerto
python manage.py runserver 127.0.0.1:8001
```

### Error: "No such table: api_herramientas"

**Causa:** Las migraciones no han sido aplicadas.

**Solución:**
```bash
cd backend
python manage.py migrate
```

### La interfaz gráfica no se conecta al backend

**Causa:** El backend no está ejecutándose o la configuración está incorrecta.

**Solución:**
1. Verifica que el backend está corriendo en Terminal 1
2. Comprueba que la URL en `config.py` es correcta
3. Abre en el navegador: http://127.0.0.1:8000/api/herramientas/

Si la URL funciona en el navegador pero no en la aplicación, reinicia la aplicación.

### ImportError durante la ejecución

**Causa:** El módulo de Python especificado no existe en el proyecto.

**Solución:**
```bash
# Reinstala todas las dependencias
pip install --force-reinstall -r requirements.txt
```

## Desinstalación

Para desinstalar completamente el proyecto:

```bash
# Desactiva el entorno virtual
deactivate

# Elimina el directorio del proyecto
rm -rf /ruta/al/proyecto  # Linux/macOS
# o
rmdir /S /path/to/project  # Windows

# Si deseas limpiar paquetes pip (opcional)
pip freeze | xargs pip uninstall -y
```

## Próximos Pasos

Una vez instalado exitosamente:

1. Lee el README.md principal para entender la arquitectura
2. Explora la interfaz gráfica para familiarizarte con las funcionalidades
3. Consulta la sección de desarrollo si deseas realizar cambios

## Soporte Técnico

Si encuentras problemas no cubiertos en esta guía:

1. Verifica los requisitos técnicos
2. Revisa los logs de error en la consola
3. Asegúrate de que Python y todas las dependencias están correctamente instaladas
4. Contacta al equipo de desarrollo

---

Guía de Instalación - Versión 1.0
Última Actualización: 30 de Noviembre de 2025
