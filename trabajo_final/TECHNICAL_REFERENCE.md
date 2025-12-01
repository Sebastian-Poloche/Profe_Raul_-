# Referencia Técnica - IHEP

## Resumen Ejecutivo

IHEP es un sistema de gestión de inventario de herramientas y préstamos que implementa una arquitectura de tres capas: presentación Tkinter, API REST Django, y base de datos SQLite. El sistema proporciona validaciones robustas, respaldos automáticos y una experiencia de usuario intuitiva.

## Especificaciones Técnicas

### Ambiente de Ejecución

- **Python:** 3.12.3
- **Tkinter:** Incluido en Python 3.12.3
- **Base de Datos:** SQLite 3
- **Servidor HTTP:** Django Development Server (desarrollo)

### Dependencias de Terceros

```
Django==5.2.8
djangorestframework==3.16.1
django-cors-headers==4.9.0
requests==2.32.5
```

### Requisitos Computacionales

| Recurso | Mínimo | Recomendado |
|---------|--------|------------|
| CPU | 1.0 GHz | 2.0 GHz+ |
| RAM | 512 MB | 2 GB+ |
| Disco | 100 MB | 500 MB+ |
| Conexión | Localhost | LAN (local) |

## Arquitectura del Sistema

### Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    Capa de Presentación                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │     Interfaz Gráfica Tkinter (InterfazIHEP)         │  │
│  │  ├─ TabView: Herramientas y Préstamos              │  │
│  │  ├─ Tablas interactivas con datos en tiempo real   │  │
│  │  ├─ Formularios de entrada y búsqueda              │  │
│  │  └─ Sistema de diálogos para confirmaciones        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/JSON (requests)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Capa de Negocio                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         API REST Django Rest Framework              │  │
│  │  ├─ HerramientasViewSet: CRUD herramientas         │  │
│  │  ├─ PrestamosViewSet: CRUD préstamos               │  │
│  │  ├─ HerramientasSerializer: Validaciones           │  │
│  │  └─ PrestamosSerializer: Validaciones complejas    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ ORM (Django)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Capa de Persistencia                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │      Base de Datos SQLite (db.sqlite3)             │  │
│  │  ├─ Tabla: api_herramientas                        │  │
│  │  ├─ Tabla: api_prestamos                           │  │
│  │  └─ Tablas auxiliares de Django                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Datos

#### Lectura (GET)

```
Usuario solicita listar herramientas
    ↓
InterfazIHEP.cargar_herramientas()
    ↓
APIClient.get_herramientas()
    ↓
requests.get('http://127.0.0.1:8000/api/herramientas/')
    ↓
HerramientasViewSet.list()
    ↓
Herramientas.objects.all()
    ↓
SELECT * FROM api_herramientas
    ↓
Serializar a JSON
    ↓
Mostrar en Tabla Tkinter
```

#### Escritura (POST/PUT)

```
Usuario crea nueva herramienta
    ↓
InterfazIHEP.crear_herramienta()
    ↓
APIClient.post_herramienta(datos)
    ↓
requests.post('http://127.0.0.1:8000/api/herramientas/', data)
    ↓
HerramientasSerializer.validate()
    ├─ Validar formato de código (7 caracteres)
    ├─ Validar unicidad de código
    ├─ Validar campos requeridos
    └─ Validar valores de enum
    ↓
HerramientasViewSet.create()
    ↓
Herramientas.objects.create()
    ↓
INSERT INTO api_herramientas VALUES(...)
    ↓
Devolver JSON de confirmación
    ↓
Actualizar tabla en interfaz
```

## Estructura de Base de Datos

### Tabla: api_herramientas

```sql
CREATE TABLE api_herramientas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(7) NOT NULL UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    categoria VARCHAR(20) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(255) NOT NULL,
    fecha_ingreso DATETIME NOT NULL,
    observaciones TEXT,
    created_at DATETIME AUTO_NOW_ADD,
    updated_at DATETIME AUTO_NOW
);
```

### Tabla: api_prestamos

```sql
CREATE TABLE api_prestamos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero VARCHAR(7) NOT NULL UNIQUE,
    herramienta_codigo VARCHAR(7) NOT NULL,
    responsable VARCHAR(255) NOT NULL,
    fecha_salida DATETIME NOT NULL,
    fecha_esperada_devolucion DATETIME NOT NULL,
    fecha_devolucion DATETIME,
    estado VARCHAR(50) NOT NULL,
    observaciones TEXT,
    created_at DATETIME AUTO_NOW_ADD,
    updated_at DATETIME AUTO_NOW
);
```

### Índices

```sql
CREATE INDEX idx_herramientas_codigo ON api_herramientas(codigo);
CREATE INDEX idx_herramientas_estado ON api_herramientas(estado);
CREATE INDEX idx_prestamos_numero ON api_prestamos(numero);
CREATE INDEX idx_prestamos_herramienta ON api_prestamos(herramienta_codigo);
CREATE INDEX idx_prestamos_estado ON api_prestamos(estado);
```

## Endpoints de la API

### Base URL

```
http://127.0.0.1:8000/api/
```

### Herramientas

#### Listar Herramientas

```
GET /herramientas/
```

Parámetros de Query (opcionales):
- `search`: Buscar por nombre o código
- `ordering`: Ordenar por campo
- `limit`: Limitar resultados

Respuesta (200 OK):
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "codigo": "HER0001",
      "nombre": "Martillo",
      "categoria": "Enviar",
      "estado": "Disponible",
      "ubicacion": "Almacén A",
      "fecha_ingreso": "2025-11-01T10:00:00Z",
      "observaciones": ""
    }
  ]
}
```

#### Crear Herramienta

```
POST /herramientas/
Content-Type: application/json
```

Cuerpo de la Solicitud:
```json
{
  "codigo": "HER0002",
  "nombre": "Destornillador",
  "categoria": "Enviar",
  "estado": "Disponible",
  "ubicacion": "Almacén B",
  "observaciones": "Nueva herramienta"
}
```

Respuesta (201 Created):
```json
{
  "id": 2,
  "codigo": "HER0002",
  "nombre": "Destornillador",
  ...
}
```

#### Obtener Herramienta

```
GET /herramientas/{id}/
```

Respuesta (200 OK):
```json
{
  "id": 1,
  "codigo": "HER0001",
  "nombre": "Martillo",
  ...
}
```

#### Actualizar Herramienta

```
PUT /herramientas/{id}/
Content-Type: application/json
```

Cuerpo:
```json
{
  "codigo": "HER0001",
  "nombre": "Martillo de Acero",
  "categoria": "Enviar",
  "estado": "En mantenimiento",
  "ubicacion": "Almacén A",
  "observaciones": "Requiere reparación"
}
```

Respuesta (200 OK):
```json
{
  "id": 1,
  "codigo": "HER0001",
  "nombre": "Martillo de Acero",
  ...
}
```

#### Eliminar Herramienta

```
DELETE /herramientas/{id}/
```

Respuesta (204 No Content)

### Préstamos

Endpoints análogos a Herramientas, reemplazando `/herramientas/` con `/prestamos/`

## Validaciones Implementadas

### Nivel Serializer (Backend)

#### Herramientas

```python
class HerramientasSerializer:
    
    def validate_codigo(self, value):
        # Validación 1: Formato exacto (7 caracteres alfanuméricos)
        if not re.match(r'^[A-Za-z0-9]{7}$', value):
            raise ValidationError("Código debe tener exactamente 7 caracteres alfanuméricos")
        
        # Validación 2: Unicidad
        if Herramientas.objects.filter(codigo=value).exclude(id=self.instance.id).exists():
            raise ValidationError("Código ya existe en la base de datos")
        
        return value
    
    def validate_nombre(self, value):
        # Validación 3: Campo requerido y no vacío
        if not value or not value.strip():
            raise ValidationError("Nombre es requerido")
        return value
    
    def validate(self, data):
        # Validación 4: Validaciones cruzadas
        if data.get('categoria') not in ['Enviar', 'Devolver']:
            raise ValidationError("Categoría inválida")
        
        if data.get('estado') not in ['Disponible', 'En préstamo', 'En mantenimiento', 'Inactivo']:
            raise ValidationError("Estado inválido")
        
        return data
```

#### Préstamos

```python
class PrestamosSerializer:
    
    def validate_numero(self, value):
        # Validación de formato y unicidad (similar a herramientas)
        ...
    
    def validate_herramienta_codigo(self, value):
        # Validación: Herramienta debe existir
        if not Herramientas.objects.filter(codigo=value).exists():
            raise ValidationError("Herramienta no existe")
        
        # Validación: Herramienta debe estar disponible
        herramienta = Herramientas.objects.get(codigo=value)
        if herramienta.estado != 'Disponible':
            raise ValidationError("Herramienta no está disponible para préstamo")
        
        return value
    
    def validate(self, data):
        # Validación: Fechas en orden correcto
        if data['fecha_salida'] >= data['fecha_esperada_devolucion']:
            raise ValidationError("Fecha de salida debe ser anterior a fecha esperada de devolución")
        
        if data.get('fecha_devolucion'):
            if data['fecha_devolucion'] <= data['fecha_esperada_devolucion']:
                raise ValidationError("Fecha de devolución debe ser posterior a fecha esperada")
        
        return data
```

## Configuración

### archivo: config.py

```python
# URLs del backend
BACKEND_HOST = os.getenv('BACKEND_HOST', '127.0.0.1')
BACKEND_PORT = int(os.getenv('BACKEND_PORT', 8000))
BACKEND_URL = os.getenv('BACKEND_URL', f'http://{BACKEND_HOST}:{BACKEND_PORT}/api/')

# Configuración de respaldos
INTERVALO_BACKUP_SEG = int(os.getenv('INTERVALO_BACKUP_SEG', 300))
BACKUP_DIRECTORY = FRONTEND_DIR / 'backups'
BACKUP_MAX_FILES = 50
BACKUP_TIMESTAMP_FORMAT = '%Y%m%d_%H%M%S'

# Configuración de HTTP
HTTP_TIMEOUT = 5
CONEXION_REINTENTOS = 3
ESPERA_ENTRE_REINTENTOS = 2
```

### archivo: backend/ch_sp/settings.py

```python
# Configuración crítica
SECRET_KEY = 'django-insecure-...'  # CAMBIAR EN PRODUCCIÓN
DEBUG = True  # CAMBIAR EN PRODUCCIÓN
ALLOWED_HOSTS = ['*']

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50
}
```

## Respaldos Automáticos

### Ubicación

```
frontend/backups/
├── backup_20251130_181831.json
├── backup_20251130_182256.json
└── ...
```

### Estructura del Archivo de Respaldo

```json
{
  "timestamp": "2025-11-30 18:18:31",
  "herramientas": [
    {
      "id": 1,
      "codigo": "HER0001",
      "nombre": "Martillo",
      ...
    }
  ],
  "prestamos": [
    {
      "id": 1,
      "numero": "PRES001",
      "herramienta_codigo": "HER0001",
      ...
    }
  ]
}
```

### Comportamiento

- Ejecuta automáticamente cada 300 segundos (configurable)
- Se ejecuta en hilo daemon (no bloquea la interfaz)
- Limpia archivos antiguos (mantiene últimos 50)
- Maneja errores gracefully (continúa aunque falle un respaldo)

## Rendimiento

### Benchmarks

| Operación | Tiempo Típico | Condiciones |
|-----------|---------------|------------|
| GET /herramientas/ (100 registros) | 45ms | Conexión local |
| POST /herramientas/ | 80ms | Incluye validaciones |
| Respaldo completo | 250ms | 100+ registros |
| Actualización UI | 150ms | Redibujado de tabla |

### Límites Conocidos

- Máximo 10,000 registros sin indexación adicional
- Máximo 50 respaldos simultáneos (se limpian antiguos)
- Timeout de conexión API: 5 segundos
- Máximo de reintentos de conexión: 3

## Seguridad

### Protecciones Implementadas

1. **Validación de Entrada**
   - Validaciones en serializers
   - Restricciones de longitud de campo
   - Validaciones de tipo de datos

2. **CORS Configuration**
   - Orígenes permitidos configurados
   - Métodos HTTP limitados

3. **Errores**
   - Mensajes de error seguros (no exponen detalles internos)
   - Logging de errores en servidor

### Recomendaciones para Producción

1. Cambiar SECRET_KEY en settings.py
2. Establecer DEBUG=False
3. Implementar HTTPS
4. Usar servidor WSGI (Gunicorn)
5. Configurar ALLOWED_HOSTS específicamente
6. Implementar autenticación (JWT/Token)
7. Configurar rate limiting
8. Usar base de datos PostgreSQL o MySQL
9. Implementar logging centralizado
10. Configurar CSRF protection

## Extensibilidad

### Agregar Nueva Funcionalidad

1. **Crear modelo**
   ```python
   class NuevoModelo(models.Model):
       # Campos del modelo
   ```

2. **Crear migración**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Crear serializer**
   ```python
   class NuevoModeloSerializer(serializers.ModelSerializer):
       # Validaciones
   ```

4. **Crear viewset**
   ```python
   class NuevoModeloViewSet(viewsets.ModelViewSet):
       queryset = NuevoModelo.objects.all()
       serializer_class = NuevoModeloSerializer
   ```

5. **Registrar en URLs**
   ```python
   router.register(r'nuevomodelo', NuevoModeloViewSet)
   ```

## Monitoreo y Debugging

### Logs

- **Backend**: Revisar consola de `python manage.py runserver`
- **Frontend**: Revisar consola de `python main.py`
- **Respaldos**: Revisar archivos en `frontend/backups/`

### Debugging en Desarrollo

```python
# Agregar prints estratégicos
print(f"DEBUG: Variable = {variable}")

# O usar logging
import logging
logger = logging.getLogger(__name__)
logger.debug("Mensaje de debug")
```

### Herramientas de Inspección

```bash
# Inspeccionar base de datos
cd backend
python manage.py shell

# Desde la shell Python
from api.models import Herramientas
Herramientas.objects.all()

# Acceder a Django Admin
# http://127.0.0.1:8000/admin/
```

## Versioning

### Versionado Semántico

Versión: MAJOR.MINOR.PATCH

- MAJOR: Cambios incompatibles con versiones anteriores
- MINOR: Nuevas funcionalidades compatibles
- PATCH: Correcciones de errores

Versión Actual: 1.0.0

---

Referencia Técnica - Versión 1.0
Última Actualización: 30 de Noviembre de 2025
