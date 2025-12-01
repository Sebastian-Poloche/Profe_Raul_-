# Guía de Desarrollo - IHEP

## Introducción para Desarrolladores

Esta guía está dirigida a desarrolladores que deseen modificar, extender o mantener el código de IHEP. Cubre convenciones de código, patrones de diseño utilizados, y procedimientos estándar de desarrollo.

## Convenciones de Código

### Estilo Python (PEP 8)

El proyecto sigue las convenciones estándar de Python (PEP 8):

- **Nombres de variables**: snake_case
- **Nombres de clases**: PascalCase
- **Nombres de constantes**: UPPER_SNAKE_CASE
- **Longitud de línea**: Máximo 80-100 caracteres
- **Indentación**: 4 espacios

### Ejemplo de Código Bien Formateado

```python
"""
Módulo que proporciona utilidades para validación de datos.
"""

# Constante global
TIMEOUT_SEGUNDOS = 30

class ValidadorDatos:
    """
    Clase responsable de validar datos de entrada.
    
    Implementa validaciones comunes como longitud, formato
    y consistencia de datos.
    """
    
    def __init__(self, modo_estricto=False):
        """
        Inicializar el validador.
        
        Args:
            modo_estricto (bool): Si True, aplica validaciones adicionales
        """
        self.modo_estricto = modo_estricto
    
    def validar_codigo(self, codigo):
        """
        Validar formato de código.
        
        Args:
            codigo (str): Código a validar
            
        Returns:
            bool: True si el código es válido
            
        Raises:
            ValueError: Si el código no cumple el formato requerido
        """
        if not codigo or len(codigo) != 7:
            raise ValueError("Código debe tener exactamente 7 caracteres")
        
        if not codigo.isalnum():
            raise ValueError("Código solo debe contener caracteres alfanuméricos")
        
        return True
```

## Estructura de Directorios

### Backend

```
backend/
├── api/
│   ├── __init__.py              # Inicializador del app Django
│   ├── admin.py                 # Configuración de Django Admin
│   ├── apps.py                  # Configuración del app
│   ├── tests.py                 # Pruebas unitarias
│   ├── models/
│   │   ├── __init__.py
│   │   ├── herramientas.py      # Modelo Herramientas
│   │   └── prestamos.py         # Modelo Préstamos
│   ├── views/
│   │   ├── __init__.py
│   │   ├── herramientas_views.py # ViewSet de Herramientas
│   │   ├── prestamos_views.py    # ViewSet de Préstamos
│   │   └── views.py              # Vistas comunes
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── herramientas_serializer.py # Serializer de Herramientas
│   │   └── prestamos_serializer.py    # Serializer de Préstamos
│   └── migrations/
│       ├── __init__.py
│       ├── 0001_initial.py      # Primera migración
│       └── ...
├── ch_sp/
│   ├── __init__.py
│   ├── settings.py              # Configuración de Django
│   ├── urls.py                  # URLs principales
│   ├── wsgi.py                  # WSGI para producción
│   ├── asgi.py                  # ASGI para WebSocket
│   └── __pycache__/
├── manage.py                    # Utilidad de administración
└── db.sqlite3                   # Base de datos
```

### Frontend

```
frontend/
├── __init__.py
├── vista/
│   ├── __init__.py
│   └── interfaz_grafica.py      # Interfaz principal Tkinter
├── controladores/
│   ├── __init__.py
│   ├── api_cliente.py           # Cliente HTTP para API
│   ├── app_controller.py        # Controlador principal
│   ├── backup_thread.py         # Sistema de respaldos
│   ├── herramientas.py          # Lógica de herramientas
│   ├── prestamos.py             # Lógica de préstamos
│   └── busqueda.py              # Funcionalidad de búsqueda
├── modelos/
│   ├── __init__.py
│   ├── herramienta_model.py     # Modelo de dominio
│   └── prestamo_model.py        # Modelo de dominio
└── backups/                     # Directorio de respaldos
    └── backup_*.json
```

## Patrones de Diseño Utilizados

### Patrón MVC (Model-View-Controller)

El backend utiliza MVC a través de Django:

- **Model**: Definido en `api/models/`
- **View**: ViewSets en `api/views/`
- **Controller**: Serializers en `api/serializers/`

### Patrón Repository

El cliente API actúa como repository:

```python
class APIClient:
    """Repository pattern para acceso a datos remotos"""
    
    def obtener_herramientas(self):
        """Simula acceso a repositorio remoto"""
        return self._get("/herramientas/")
```

### Patrón Observer

El sistema de actualizaciones automáticas implementa observer:

```python
class InterfazIHEP:
    """Observer pattern para actualización de datos"""
    
    def _iniciar_actualizaciones_automaticas(self):
        """Inicia observer para cambios en datos"""
        thread = threading.Thread(target=self._actualizar_periodicamente)
        thread.daemon = True
        thread.start()
```

## Flujo de Desarrollo

### 1. Crear una Rama de Feature

```bash
git checkout -b feature/nombre-descriptivo
```

Ejemplos:
- `feature/agregar-validacion-emails`
- `feature/mejorar-busqueda`
- `fix/corregir-bug-respaldos`

### 2. Realizar Cambios

Editar archivos según sea necesario, mantiendo las convenciones.

### 3. Escribir Pruebas

```python
# backend/api/tests.py

from django.test import TestCase
from api.models import Herramientas

class HerramientasTestCase(TestCase):
    
    def setUp(self):
        """Configurar datos de prueba"""
        self.herramienta = Herramientas.objects.create(
            codigo="HER0001",
            nombre="Martillo",
            categoria="Enviar",
            estado="Disponible",
            ubicacion="Almacén A"
        )
    
    def test_crear_herramienta(self):
        """Verificar que se puede crear una herramienta"""
        self.assertEqual(self.herramienta.codigo, "HER0001")
    
    def test_validar_codigo_unico(self):
        """Verificar que el código debe ser único"""
        with self.assertRaises(IntegrityError):
            Herramientas.objects.create(
                codigo="HER0001",  # Código duplicado
                nombre="Destornillador",
                categoria="Enviar",
                estado="Disponible",
                ubicacion="Almacén B"
            )
```

### 4. Ejecutar Pruebas

```bash
cd backend
python manage.py test
```

### 5. Hacer Commit de Cambios

```bash
git add .
git commit -m "Descripción clara del cambio"
```

### 6. Hacer Push a Rama Remota

```bash
git push origin feature/nombre-descriptivo
```

### 7. Crear Pull Request

En la plataforma Git (GitHub, GitLab, etc.), crear PR con:
- Título descriptivo
- Descripción de cambios
- Enlace a issues relacionados
- Screenshots si es necesario

## Tareas Comunes de Desarrollo

### Agregar un Nuevo Campo a un Modelo

1. **Modificar el modelo**

```python
# backend/api/models/herramientas.py

class Herramientas(models.Model):
    # ... campos existentes ...
    peso_kg = models.FloatField(
        default=0.0,
        help_text="Peso de la herramienta en kilogramos"
    )
```

2. **Crear migración**

```bash
cd backend
python manage.py makemigrations api
```

3. **Aplicar migración**

```bash
python manage.py migrate
```

4. **Actualizar serializer**

```python
# backend/api/serializers/herramientas_serializer.py

class HerramientasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herramientas
        fields = [
            'id', 'codigo', 'nombre', 'categoria', 
            'estado', 'ubicacion', 'fecha_ingreso', 
            'observaciones', 'peso_kg'  # Nuevo campo
        ]
    
    def validate_peso_kg(self, value):
        if value < 0:
            raise serializers.ValidationError("Peso no puede ser negativo")
        return value
```

### Agregar una Nueva Validación

1. **Identificar dónde agregar la validación**

   - Validaciones simples de campo: Método `validate_<campo>()` en serializer
   - Validaciones cruzadas: Método `validate()` en serializer

2. **Implementar la validación**

```python
def validate_fecha_devolucion(self, value):
    """Validar que la fecha de devolución es coherente"""
    if value and value < datetime.now():
        raise serializers.ValidationError(
            "La fecha de devolución no puede ser en el pasado"
        )
    return value
```

3. **Probar la validación**

```python
def test_validar_fecha_devolucion(self):
    """Verificar validación de fecha de devolución"""
    with self.assertRaises(ValidationError):
        serializer = PrestamosSerializer(data={
            'numero': 'PRES001',
            'herramienta_codigo': 'HER0001',
            'responsable': 'Juan',
            'fecha_salida': datetime.now(),
            'fecha_esperada_devolucion': datetime.now() + timedelta(days=1),
            'fecha_devolucion': datetime.now() - timedelta(days=1),  # En el pasado
            'estado': 'Completado'
        })
        serializer.is_valid(raise_exception=True)
```

### Modificar la Interfaz Gráfica

1. **Identificar el componente en InterfazIHEP**

```python
def _crear_tab_herramientas(self):
    """Crear pestaña de herramientas"""
    # ... código existente ...
```

2. **Realizar cambios**

```python
def _crear_tab_herramientas(self):
    """Crear pestaña de herramientas"""
    self.frame_herramientas = ttk.Frame(self.notebook)
    
    # Agregar nuevo botón
    btn_nueva_funcionalidad = ttk.Button(
        self.frame_herramientas,
        text="Nueva Funcionalidad",
        command=self.nueva_funcionalidad
    )
    btn_nueva_funcionalidad.pack(pady=5)

def nueva_funcionalidad(self):
    """Implementar nueva funcionalidad"""
    messagebox.showinfo("Info", "Nueva funcionalidad ejecutada")
```

3. **Probar cambios**

Ejecutar la aplicación y verificar que el cambio funciona correctamente.

## Debugging

### Debugger de Python

```python
# Agregar punto de quiebre
import pdb; pdb.set_trace()

# Comandos útiles en pdb
# n - siguiente línea
# s - entrar en función
# c - continuar ejecución
# p variable - imprimir variable
# l - listar código
# b - establecer breakpoint
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Mensaje de debug")
logger.info("Información")
logger.warning("Advertencia")
logger.error("Error")
logger.critical("Error crítico")
```

### Inspeccionar Solicitudes HTTP

```python
# En APIClient, agregar logging

import requests
requests.packages.urllib3.disable_warnings()
logger = logging.getLogger('requests')
logger.setLevel(logging.DEBUG)
```

## Optimización

### Optimizaciones de Base de Datos

```python
# Usar select_related para Foreign Keys
herramientas = Herramientas.objects.select_related('categoria')

# Usar prefetch_related para Many-to-Many
prestamos = Prestamos.objects.prefetch_related('herramientas')

# Agregar índices
class Herramientas(models.Model):
    codigo = models.CharField(
        max_length=7,
        db_index=True  # Agregar índice
    )
```

### Optimizaciones de API

```python
# Paginación
class CustomPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

# Caché
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutos
def mi_vista(request):
    pass
```

## Documentación de Código

### Docstrings

Utilizar formato Google o NumPy:

```python
def crear_respaldo(ruta_salida, nombre_archivo):
    """
    Crear un archivo de respaldo de los datos.
    
    Genera un archivo JSON con datos de herramientas y préstamos,
    lo serializa y lo guarda en la ruta especificada.
    
    Args:
        ruta_salida (Path): Ruta del directorio de salida
        nombre_archivo (str): Nombre del archivo (sin extensión)
    
    Returns:
        bool: True si el respaldo fue exitoso, False en caso contrario
    
    Raises:
        IOError: Si no se puede escribir en la ruta especificada
        Exception: Si hay error durante la serialización de datos
    
    Example:
        >>> crear_respaldo(Path('/backups'), 'backup')
        True
    """
    pass
```

### Comentarios en Línea

```python
# Usar comentarios para explicar el "por qué", no el "qué"

# Bien
datos_ordenados = sorted(datos, key=lambda x: x['fecha'])  # Necesario para generar reportes

# Mal
lista = sorted(lista, key=lambda x: x['fecha'])  # Ordenar por fecha
```

## Control de Versiones

### Mensajes de Commit

```
<tipo>(<alcance>): <descripción>

<cuerpo>

<pie>
```

Tipos válidos: feat, fix, docs, style, refactor, test, chore

Ejemplos:

```
feat(herramientas): agregar validación de peso

Agregar validación de peso en el serializer de herramientas.
El peso debe ser un número positivo.

Closes #123
```

```
fix(api): corregir error en búsqueda de herramientas

Se corrigió el filtro de búsqueda que no funcionaba con caracteres especiales.

Fixes #456
```

## Testing

### Estructura de Pruebas

```
backend/
├── api/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_serializers.py
│   │   ├── test_views.py
│   │   └── test_integration.py
│   └── ...
```

### Ejecutar Pruebas Específicas

```bash
# Todas las pruebas
python manage.py test

# Pruebas de una app
python manage.py test api

# Pruebas de una clase
python manage.py test api.tests.HerramientasTestCase

# Pruebas de un método
python manage.py test api.tests.HerramientasTestCase.test_crear_herramienta

# Con cobertura
pip install coverage
coverage run --source='api' manage.py test
coverage report
```

## Deployment

### Preparar para Producción

1. **Cambiar configuración**

```python
# settings.py
DEBUG = False
SECRET_KEY = 'nueva-clave-secreta-segura'
ALLOWED_HOSTS = ['dominio.com', 'www.dominio.com']
```

2. **Recolectar archivos estáticos**

```bash
python manage.py collectstatic
```

3. **Ejecutar verificaciones de seguridad**

```bash
python manage.py check --deploy
```

### Usar Gunicorn

```bash
# Instalar
pip install gunicorn

# Ejecutar
gunicorn ch_sp.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## Herramientas Recomendadas

### IDE / Editor

- PyCharm Professional
- Visual Studio Code con extensión Python
- Sublime Text 3

### Linters y Formateadores

```bash
# Instalar
pip install black flake8 pylint

# Usar
black archivo.py
flake8 archivo.py
pylint archivo.py
```

### Git Hooks

```bash
# Pre-commit hook para ejecutar linter
#!/bin/bash
black . && flake8 .
```

## Recursos Adicionales

- Documentación Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- PEP 8: https://www.python.org/dev/peps/pep-0008/
- Git: https://git-scm.com/doc

---

Guía de Desarrollo - Versión 1.0
Última Actualización: 30 de Noviembre de 2025
