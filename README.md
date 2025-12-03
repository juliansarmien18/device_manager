# Devices Manager API

API desarrollada con Django y Django REST Framework (DRF) que implementa autenticación mediante JSON Web Tokens (JWT) y permite a los usuarios gestionar sus dispositivos en el contexto de múltiples plataformas.

## Características

- ✅ Autenticación JWT por plataforma
- ✅ Gestión de múltiples plataformas
- ✅ Usuarios pueden registrarse en múltiples plataformas con el mismo email
- ✅ Gestión de dispositivos por usuario y plataforma
- ✅ Modelos con auditoría (created_by, updated_by) usando django-currentuser
- ✅ Settings divididos en base, dev y prod
- ✅ Docker Compose para desarrollo
- ✅ Pre-commits configurados
- ✅ Tests unitarios y de integración
- ✅ Principios SOLID aplicados

## Requisitos

- Python 3.11+
- UV (gestor de paquetes)
- Docker y Docker Compose (opcional)

## Instalación

### Opción 1: Con Make (Más Rápido)

Si tienes `make` instalado:

```bash
make install    # Instalar dependencias
make migrate    # Ejecutar migraciones
make test-data  # Crear datos de prueba (opcional)
make run        # Ejecutar servidor
```

### Opción 2: Con UV (Recomendado)

1. **Instalar UV** (si no lo tienes):
   ```bash
   # Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Linux/Mac
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Instalar dependencias**:
   ```bash
   cd devices_manager
   uv pip install -e ".[dev]"
   ```

3. **Configurar variables de entorno** (opcional):
   ```bash
   # En Windows PowerShell
   $env:DJANGO_SETTINGS_MODULE="devices_manager.settings.dev"
   
   # En Linux/Mac
   export DJANGO_SETTINGS_MODULE=devices_manager.settings.dev
   ```

4. **Ejecutar migraciones**:
   ```bash
   cd devices_manager
   py manage.py migrate
   ```

5. **Crear superusuario** (opcional, para admin):
   ```bash
   py manage.py createsuperuser
   ```

6. **Ejecutar servidor de desarrollo**:
   ```bash
   py manage.py runserver
   ```

### Opción 3: Con Docker Compose

1. **Construir y ejecutar**:
   ```bash
   docker-compose up --build
   ```

2. **Ejecutar migraciones** (en otra terminal):
   ```bash
   docker-compose exec web py manage.py migrate
   ```

3. **Crear superusuario** (opcional):
   ```bash
   docker-compose exec web py manage.py createsuperuser
   ```

El servidor estará disponible en `http://localhost:8000`

## Configuración de Pre-commits

Para habilitar los pre-commits:

```bash
# Instalar pre-commit
uv pip install pre-commit

# Instalar hooks
pre-commit install
```

## Crear Datos de Prueba

### Crear Plataformas

Puedes crear plataformas de dos formas:

#### Opción 1: Desde el Admin de Django

1. Accede a `http://localhost:8000/admin/`
2. Inicia sesión con el superusuario
3. Ve a "Platforms" → "Add Platform"
4. Crea plataformas como "Plataforma A", "Plataforma B", etc.

#### Opción 2: Desde la Shell de Django

```bash
py manage.py shell
```

```python
from apps.platforms.models import Platform

# Crear plataformas
platform_a = Platform.objects.create(
    name="Plataforma A",
    description="Descripción de la Plataforma A",
    is_active=True
)

platform_b = Platform.objects.create(
    name="Plataforma B",
    description="Descripción de la Plataforma B",
    is_active=True
)

print(f"Plataforma A creada con ID: {platform_a.id}")
print(f"Plataforma B creada con ID: {platform_b.id}")
```

### Crear Usuarios de Prueba

#### Opción 1: Comando de Management (Recomendado)

```bash
cd devices_manager
py manage.py create_test_data
```

Este comando crea:
- 2 plataformas (Plataforma A y Plataforma B)
- 3 usuarios de prueba:
  - `usuario1@example.com` en Plataforma A y B (mismo email, diferentes plataformas)
  - `usuario2@example.com` en Plataforma A
- 3 dispositivos de ejemplo

**Credenciales de prueba**:
- Email: `usuario1@example.com`
- Password: `password123`
- Platform ID: `1` (Plataforma A) o `2` (Plataforma B)

#### Opción 2: Endpoint de Registro

Los usuarios también se pueden crear mediante el endpoint de registro (ver sección de Ejemplos de API).

## Endpoints de la API

### Base URL
```
http://localhost:8000/api
```

### Autenticación

#### 1. Registrar Usuario
```http
POST /api/auth/register/
Content-Type: application/json

{
    "email": "usuario@example.com",
    "password": "password123",
    "platform_id": 1
}
```

**Respuesta exitosa (201)**:
```json
{
    "message": "Usuario registrado exitosamente.",
    "user_id": 1,
    "email": "usuario@example.com",
    "platform": "Plataforma A"
}
```

#### 2. Iniciar Sesión (Obtener Token JWT)
```http
POST /api/auth/login/
Content-Type: application/json

{
    "email": "usuario@example.com",
    "password": "password123",
    "platform_id": 1
}
```

**Respuesta exitosa (200)**:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Plataformas

#### Listar Plataformas Activas
```http
GET /api/platforms/
```

**Respuesta (200)**:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Plataforma A",
            "description": "Descripción de la Plataforma A",
            "is_active": true,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### Dispositivos

**Nota**: Todos los endpoints de dispositivos requieren autenticación JWT.

#### Listar Dispositivos del Usuario Autenticado
```http
GET /api/devices/
Authorization: Bearer <access_token>
```

**Respuesta (200)**:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Dispositivo 1",
            "ip_address": "192.168.1.1",
            "is_active": true,
            "user_platform_email": "usuario@example.com",
            "platform_name": "Plataforma A",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

#### Crear Dispositivo
```http
POST /api/devices/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Nuevo Dispositivo",
    "ip_address": "192.168.1.100",
    "is_active": true
}
```

#### Obtener Detalle de Dispositivo
```http
GET /api/devices/{id}/
Authorization: Bearer <access_token>
```

#### Actualizar Dispositivo
```http
PATCH /api/devices/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Dispositivo Actualizado",
    "is_active": false
}
```

#### Eliminar Dispositivo
```http
DELETE /api/devices/{id}/
Authorization: Bearer <access_token>
```

#### Endpoint Personalizado: Mis Dispositivos
```http
GET /api/devices/my_devices/
Authorization: Bearer <access_token>
```

#### Toggle Estado Activo
```http
PATCH /api/devices/{id}/toggle_active/
Authorization: Bearer <access_token>
```

## Ejemplos de Uso con cURL

### 1. Registrar un Usuario

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "password123",
    "platform_id": 1
  }'
```

### 2. Obtener Token JWT

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "password": "password123",
    "platform_id": 1
  }'
```

Guarda el `access` token de la respuesta.

### 3. Listar Dispositivos

```bash
curl -X GET http://localhost:8000/api/devices/ \
  -H "Authorization: Bearer <TU_ACCESS_TOKEN>"
```

### 4. Crear un Dispositivo

```bash
curl -X POST http://localhost:8000/api/devices/ \
  -H "Authorization: Bearer <TU_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi Dispositivo",
    "ip_address": "192.168.1.50",
    "is_active": true
  }'
```

## Ejemplos de Uso con Postman

1. **Crear una colección** en Postman
2. **Configurar variables de entorno**:
   - `base_url`: `http://localhost:8000/api`
   - `access_token`: (se actualizará después del login)

3. **Flujo de trabajo**:
   - Primero, registra un usuario o inicia sesión
   - Copia el `access` token de la respuesta
   - Úsalo en el header `Authorization: Bearer <token>` para las peticiones protegidas

## Ejecutar Tests

```bash
# Con Make
make test

# O manualmente
cd devices_manager
py -m pytest

# Ejecutar tests con cobertura
py -m pytest --cov=devices_manager --cov-report=html

# Ejecutar tests de una app específica
py -m pytest apps/platforms/tests.py
```

## Estructura del Proyecto

```
devices_manager/
├── apps/
│   ├── authentication/    # Autenticación JWT personalizada
│   ├── core/              # Modelos base y utilidades
│   ├── devices/           # Gestión de dispositivos
│   └── platforms/         # Gestión de plataformas
├── devices_manager/
│   ├── settings/
│   │   ├── base.py        # Configuración base
│   │   ├── dev.py         # Configuración desarrollo
│   │   └── prod.py        # Configuración producción
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
├── .pre-commit-config.yaml
└── README.md
```

## Modelos de Datos

### Platform
- `name`: Nombre único de la plataforma
- `description`: Descripción opcional
- `is_active`: Estado activo/inactivo

### UserPlatform
- `email`: Email del usuario (único por plataforma)
- `platform`: Relación con Platform
- `password`: Contraseña hasheada
- `is_active`: Estado activo/inactivo
- `last_login`: Último acceso

**Nota**: El mismo email puede existir en múltiples plataformas.

### Device
- `name`: Nombre del dispositivo
- `ip_address`: Dirección IP (IPv4)
- `is_active`: Estado activo/inactivo
- `user_platform`: Relación con UserPlatform

Todos los modelos heredan de `BaseModel` que incluye:
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización
- `created_by`: Usuario que creó el registro
- `updated_by`: Usuario que actualizó el registro

## Seguridad

- Las contraseñas se almacenan usando el sistema de hashing de Django
- Los tokens JWT incluyen `platform_id` para validación
- Los endpoints protegidos requieren autenticación JWT
- Los dispositivos se filtran automáticamente por usuario y plataforma

## Características Adicionales

- **Paginación**: Los listados están paginados (20 items por página)
- **Búsqueda**: Los dispositivos se pueden buscar por nombre e IP
- **Ordenamiento**: Los dispositivos se pueden ordenar por varios campos
- **Filtros**: Filtrado automático por usuario y plataforma

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'apps'"
Asegúrate de estar en el directorio `devices_manager` al ejecutar los comandos.

### Error: "DJANGO_SETTINGS_MODULE not set"
Configura la variable de entorno:
```bash
# Windows PowerShell
$env:DJANGO_SETTINGS_MODULE="devices_manager.settings.dev"
```

### Error: "Token does not contain platform_id"
Asegúrate de usar el token obtenido del endpoint de login, no un token generado manualmente.

## Licencia

Este proyecto es una prueba técnica.

## Autor

Desarrollado siguiendo principios SOLID y mejores prácticas de Django/DRF.

