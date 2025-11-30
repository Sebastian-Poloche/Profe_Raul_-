# IHEP - Inventario de Herramientas y Préstamos

> Sistema de gestión de herramientas y préstamos desarrollado para **TecnoGestión S.A.S.** bajo la referencia **RFP-IHEP-2025**

## 📌 Descripción del Proyecto

**IHEP** es una aplicación de escritorio desarrollada en Python que automatiza la administración de herramientas y préstamos en TecnoGestión S.A.S. El sistema reemplaza los procesos manuales dispersos por una solución integrada que ofrece:

- ✅ Registro y control centralizado de herramientas
- ✅ Gestión completa de préstamos con trazabilidad
- ✅ Interface gráfica intuitiva con Tkinter
- ✅ API REST moderna con Django
- ✅ Respaldo automático de datos
- ✅ Búsqueda avanzada en tiempo real

---

## 🏗️ Arquitectura Técnica

### Stack Tecnológico

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| **Frontend** | Python + Tkinter | 3.14 |
| **Backend** | Django + DRF | 5.2.8 / 3.16.1 |
| **Base de datos** | SQLite | 3.x |
| **API** | REST HTTP/JSON | - |
| **Comunicación** | Requests | 2.32.5 |

### Arquitectura en Capas

```
┌─────────────────────────────────────┐
│      CAPA DE PRESENTACIÓN           │
│   (Tkinter GUI - InterfazIHEP)      │
├─────────────────────────────────────┤
│      CAPA DE LÓGICA DE NEGOCIO      │
│  (Controladores - API Client)       │
├─────────────────────────────────────┤
│      CAPA DE DATOS / API REST       │
│ (Django ViewSets - Serializers)     │
├─────────────────────────────────────┤
│      CAPA DE PERSISTENCIA           │
│  (SQLite - Modelos Django)          │
└─────────────────────────────────────┘
```

### Características Clave

#### 1. **Modelos de Datos (sin Llaves Foráneas)**

**Herramientas**
```python
- id: Integer (PK)
- codigo: CharField(7) - Código único
- nombre: CharField(20) - Nombre descriptivo
- categoria: Choice[Enviar|Devolver]
- ubicacion: CharField(30) - Ubicación física
- estado: Choice[Disponible|En préstamo|Mantenimiento|Inactivo]
- created_at: DateTime (auto)
- updated_at: DateTime (auto)
```

**Préstamos**
```python
- id: Integer (PK)
- numero: CharField(7) - Número de préstamo único
- herramienta_codigo: CharField(20) - Referencia (NO es FK)
- responsable: CharField(15) - Persona responsable
- fecha_salida: Date
- fecha_esperada: Date
- fecha_devolucion: Date (nullable)
- created_at: DateTime (auto)
- updated_at: DateTime (auto)
```

#### 2. **Respaldo Automático**

- **Ejecución:** Hilo independiente (daemon thread)
- **Intervalo:** 300 segundos (5 minutos) - configurable
- **Formato:** JSON
- **Ubicación:** `frontend/backups/backup_YYYYMMDD_HHMMSS.json`
- **Limpieza:** Mantiene los últimos 10 respaldos automáticamente
- **Configuración:** Variable de entorno `INTERVALO_BACKUP_SEG`

#### 3. **Interface Gráfica**

**Tabs principales:**

1. **Herramientas**
   - Formulario de alta/edición
   - Tabla con listado completo
   - Botones: Guardar, Limpiar, Editar, Eliminar

2. **Préstamos**
   - Formulario con validaciones
   - Tabla con estado de préstamos
   - Botones: Guardar, Editar, Eliminar, Registrar Devolución

3. **Búsqueda**
   - Búsqueda por código, nombre, responsable
   - Filtros dinámicos por tipo (Herramientas/Préstamos)
   - Resultados en tiempo real

---

## 🚀 Instalación y Ejecución

### Requisitos Previos

- **Python 3.10+** (probado en 3.14)
- **pip** (gestor de paquetes)
- **PowerShell 5.1+** (Windows)

### Paso 1: Clonar/Descargar el Proyecto

```bash
cd c:\Users\chatarra\Documents\Profe_Raul_-\trabajo_final
```

### Paso 2: Crear Entorno Virtual

```powershell
# Crear entorno virtual (si no existe)
python -m venv .venv

# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Si falla por política de ejecución:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Paso 3: Instalar Dependencias

```powershell
# Asegurarse que .venv está activado
pip install -r requirements.txt

# O instalar manualmente:
pip install Django==5.2.8
pip install djangorestframework==3.16.1
pip install django-cors-headers==4.9.0
pip install requests==2.32.5
```

### Paso 4: Aplicar Migraciones

```powershell
cd backend
python manage.py migrate
cd ..
```

### Paso 5: Iniciar Sistema

**Opción A: Script automático (Recomendado)**

```powershell
# Con todas las opciones:
.\iniciar_ihep.ps1

# El sistema iniciará:
# - Backend Django en http://127.0.0.1:8000
# - Frontend Tkinter automáticamente
# - Respaldos automáticos cada 5 minutos
```

**Opción B: Manual (Dos terminales)**

Terminal 1 - Backend:
```powershell
cd backend
python manage.py runserver 127.0.0.1:8000
# Output: Starting development server at http://127.0.0.1:8000/
```

Terminal 2 - Frontend:
```powershell
python main.py
# Se abre ventana Tkinter automáticamente
```

---

## 📖 Guía de Uso

### Gestión de Herramientas

1. **Agregar herramienta:**
   - Ir a tab "Herramientas"
   - Llenar formulario (código, nombre, categoría, ubicación)
   - Clic en "Guardar"

2. **Editar herramienta:**
   - Seleccionar herramienta en la tabla
   - Modificar campos
   - Clic en "Editar"

3. **Eliminar herramienta:**
   - Seleccionar herramienta
   - Clic en "Eliminar" (confirmación)

### Gestión de Préstamos

1. **Crear préstamo:**
   - Tab "Préstamos"
   - Llenar: Número, Código herramienta, Responsable, Fechas
   - La herramienta debe estar en estado "Disponible"
   - Clic en "Guardar"

2. **Registrar devolución:**
   - Seleccionar préstamo
   - Ingresar fecha de devolución
   - Clic en "Registrar Devolución"

3. **Validaciones automáticas:**
   - No permite préstamos de herramientas no disponibles
   - Valida formato de fechas (YYYY-MM-DD)
   - Verifica campos obligatorios

### Búsqueda Avanzada

1. **Buscar herramientas:**
   - Tab "Búsqueda"
   - Seleccionar "Herramientas" en "Buscar en"
   - Elegir campo (código, nombre, categoría, ubicación)
   - Ingresar término
   - Clic en "Buscar"

2. **Buscar préstamos:**
   - Seleccionar "Préstamos"
   - Elegir campo (número, responsable, código herramienta)
   - Ingresar término
   - Resultados aparecen automáticamente

---

## 🔌 API REST

### Endpoints Disponibles

#### Herramientas

```
GET    /api/herramientas/          - Listar todas las herramientas
POST   /api/herramientas/          - Crear nueva herramienta
GET    /api/herramientas/{id}/     - Obtener detalle
PUT    /api/herramientas/{id}/     - Actualizar herramienta
DELETE /api/herramientas/{id}/     - Eliminar herramienta
```

#### Préstamos

```
GET    /api/prestamos/             - Listar todos los préstamos
POST   /api/prestamos/             - Crear nuevo préstamo
GET    /api/prestamos/{id}/        - Obtener detalle
PUT    /api/prestamos/{id}/        - Actualizar préstamo
DELETE /api/prestamos/{id}/        - Eliminar préstamo
```

### Ejemplo de Uso de API

```bash
# Obtener todas las herramientas
curl -X GET http://127.0.0.1:8000/api/herramientas/

# Crear nuevo préstamo
curl -X POST http://127.0.0.1:8000/api/prestamos/ \
  -H "Content-Type: application/json" \
  -d '{
    "numero": "PR006",
    "herramienta_codigo": "001",
    "responsable": "Juan Pérez",
    "fecha_salida": "2025-11-30",
    "fecha_esperada": "2025-12-03",
    "fecha_devolucion": null
  }'
```

---

## 📁 Estructura de Directorios

```
trabajo_final/
├── backend/
│   ├── ch_sp/                  # Configuración Django
│   │   ├── settings.py         # Configuración principal
│   │   ├── urls.py             # URLs del proyecto
│   │   └── wsgi.py
│   ├── api/
│   │   ├── models/
│   │   │   ├── herramientas.py
│   │   │   └── prestamos.py
│   │   ├── serializers/
│   │   │   ├── herramientas_serializer.py
│   │   │   └── prestamos_serializer.py
│   │   ├── views/
│   │   │   ├── herramientas_views.py
│   │   │   └── prestamos_views.py
│   │   └── migrations/
│   ├── db.sqlite3              # Base de datos
│   └── manage.py
├── frontend/
│   ├── vista/
│   │   └── interfaz_grafica.py # UI Tkinter
│   ├── controladores/
│   │   ├── api_cliente.py      # Cliente HTTP
│   │   ├── backup_thread.py    # Respaldos automáticos
│   │   └── ...
│   ├── modelos/
│   │   ├── herramienta_model.py
│   │   └── prestamo_model.py
│   └── backups/                # Respaldos JSON
├── main.py                     # Punto de entrada
├── iniciar_ihep.ps1            # Script de inicio (PowerShell)
├── iniciar_ihep.bat            # Script de inicio (Batch)
├── iniciar_ihep.py             # Script de inicio (Python)
├── README.md                   # Este archivo
├── GUIA_POWERSHELL.md          # Guía de PowerShell
└── VERIFICACION_RFP.md         # Verificación de requisitos
```

---

## 🧪 Respaldos Automáticos

### Ejemplo de Respaldo JSON

```json
{
  "timestamp": "2025-11-30T14:30:45.123456",
  "herramientas": [
    {
      "id": 1,
      "codigo": "001",
      "nombre": "Martillo",
      "categoria": "Enviar",
      "ubicacion": "Almacén A - Estante 1",
      "estado": "Disponible",
      "created_at": "2025-11-29T16:00:50Z",
      "updated_at": "2025-11-29T16:00:50Z"
    }
  ],
  "prestamos": [
    {
      "id": 1,
      "numero": "PR001",
      "herramienta_codigo": "001",
      "responsable": "Juan Pérez",
      "fecha_salida": "2025-11-30",
      "fecha_esperada": "2025-12-03",
      "fecha_devolucion": null,
      "created_at": "2025-11-30T14:00:00Z",
      "updated_at": "2025-11-30T14:00:00Z"
    }
  ]
}
```

### Configurar Intervalo de Respaldo

```powershell
# Variable de entorno (300 segundos = 5 minutos por defecto)
$env:INTERVALO_BACKUP_SEG = "600"  # 10 minutos

# O en archivo .env en la raíz:
INTERVALO_BACKUP_SEG=600
```

---

## 🐛 Solución de Problemas

### Problema: "ModuleNotFoundError: No module named 'django'"

**Solución:**
```powershell
# Verificar que .venv está activado
.\.venv\Scripts\Activate.ps1

# Reinstalar dependencias
pip install -r requirements.txt
```

### Problema: "Port 8000 already in use"

**Solución:**
```powershell
# Usar otro puerto
cd backend
python manage.py runserver 127.0.0.1:8001

# O detener procesos Python
Get-Process python | Stop-Process -Force
```

### Problema: "Cannot connect to API"

**Verificar:**
1. Backend está corriendo: `python manage.py runserver`
2. URL correcta: `http://127.0.0.1:8000/api/`
3. No hay errores en terminal del backend

### Problema: Respaldos no se crean

**Solución:**
```powershell
# Crear carpeta manualmente si no existe
mkdir frontend/backups

# Verificar permisos de escritura
# Consultar logs en consola para errores específicos
```

---

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| Líneas de código (Backend) | ~500 |
| Líneas de código (Frontend) | ~550 |
| Modelos de datos | 2 |
| Endpoints REST | 10 |
| Tabs en interfaz | 3 |
| Scripts de utilidad | 4 |
| Campos validados | 12+ |
| Requisitos cumplidos (RFP) | 94% |

---

## ✅ Checklist de Cumplimiento RFP

- ✅ Desarrollo orientado a eventos (threading)
- ✅ Frontend en Tkinter (Python)
- ✅ Backend en Django REST Framework
- ✅ Gestión de herramientas y préstamos
- ✅ **SIN LLAVES FORÁNEAS** (herramienta_codigo es CharField)
- ✅ Borrado físico (eliminación permanente)
- ✅ Respaldo automático periódico
- ✅ Intervalo configurable
- ✅ Formato JSON
- ✅ Interface con pestañas
- ✅ Formularios con validación
- ✅ Listados con Treeview
- ✅ Búsqueda avanzada
- ✅ Textos en español
- ✅ CRUD completo
- ✅ Manejo de errores
- ✅ Código comentado y PEP8
- ✅ Ejecutable localmente

---

## 📝 Notas Importantes

1. **Seguridad en Desarrollo:** La aplicación está configurada con `DEBUG = True` y `ALLOWED_HOSTS = ['*']`. Para producción, cambiar a valores seguros.

2. **Autenticación:** No incluye sistema de autenticación por requisito del RFP. Para producción, se recomienda implementar.

3. **CORS:** Habilitado para desarrollo local. Restringir en producción.

4. **Base de datos:** SQLite es suficiente para desarrollo. Para producción, migrar a PostgreSQL o MySQL.

5. **Escalabilidad:** El sistema fue diseñado para ambiente local. Para escalar, considerar:
   - Microservicios
   - Caché distribuido (Redis)
   - Base de datos relacional robusta
   - Sistema de colas (Celery)

---

## 👥 Autor

**Desarrollado para:** TecnoGestión S.A.S.  
**Referencia:** RFP-IHEP-2025  
**Fecha:** Noviembre de 2025

---

## 📄 Licencia

Este proyecto fue desarrollado como parte de una solicitud de propuesta (RFP) para TecnoGestión S.A.S.

---

## 📞 Soporte

Para problemas o consultas:

1. Revisar `GUIA_POWERSHELL.md` para instrucciones paso a paso
2. Consultar `VERIFICACION_RFP.md` para verificación de requisitos
3. Revisar sección "Solución de Problemas" arriba
4. Examinar logs en terminal del backend

---

**Última actualización:** 30 de Noviembre de 2025  
**Versión:** 1.0  
**Estado:** ✅ Listo para presentación
