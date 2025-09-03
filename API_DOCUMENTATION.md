# API Documentation - Citalo Backend

## Introducción

La API de Citalo es una REST API completa para un sistema de gestión de citas y reservas para negocios. Permite a los usuarios registrarse como clientes o propietarios de negocios, gestionar servicios, horarios, citas y reseñas.

## Características Principales

- **Autenticación basada en tokens**
- **Gestión completa de usuarios** (clientes, negocios, empleados)
- **Sistema de categorías y negocios**
- **Gestión de servicios y horarios**
- **Sistema de reservas/citas**
- **Sistema de reseñas y calificaciones**
- **Facturación y suscripciones**
- **Filtrado avanzado y búsqueda**
- **Paginación automática**
- **Documentación OpenAPI/Swagger**

## URLs Base

- **API Base**: `/api/`
- **Documentación Swagger**: `/api/docs/`
- **Documentación ReDoc**: `/api/redoc/`
- **Schema OpenAPI**: `/api/schema/`

## Autenticación

### Endpoints de Autenticación

#### Login
```
POST /api/auth/login/
```

**Parámetros:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Respuesta exitosa:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": "uuid",
    "email": "user@example.com",
    "username": "usuario",
    "tipo_usuario": "cliente",
    "nombre_completo": "Nombre Apellido"
}
```

#### Logout
```
POST /api/auth/logout/
```

Requiere token de autenticación en headers:
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### Uso del Token

Para todas las peticiones autenticadas, incluir el header:
```
Authorization: Token YOUR_TOKEN_HERE
```

## Endpoints Principales

### 1. Usuarios (`/api/usuarios/`)

#### Registro de Usuario
```
POST /api/usuarios/
```

**Parámetros:**
```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "password_confirm": "string",
    "first_name": "string",
    "last_name": "string",
    "tipo_usuario": "cliente|negocio|empleado|admin",
    "telefono": "string",
    "ciudad": "string",
    "provincia": "string"
}
```

#### Obtener Perfil Propio
```
GET /api/usuarios/me/
```

#### Actualizar Perfil Propio
```
PATCH /api/usuarios/me/
```

#### Cambiar Contraseña
```
POST /api/usuarios/{id}/change_password/
```

**Parámetros:**
```json
{
    "old_password": "string",
    "new_password": "string"
}
```

#### Filtros Disponibles
- `tipo_usuario`: Filtrar por tipo de usuario
- `ciudad`: Filtrar por ciudad
- `nombre`: Buscar por nombre completo
- `fecha_registro_desde`: Usuarios registrados desde una fecha
- `fecha_registro_hasta`: Usuarios registrados hasta una fecha

### 2. Categorías de Negocio (`/api/categorias-negocio/`)

#### Listar Categorías
```
GET /api/categorias-negocio/
```

**Respuesta:**
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "nombre": "Peluquería",
            "descripcion": "Servicios de peluquería y estética",
            "icono": "fa-cut",
            "activa": true,
            "orden": 1,
            "duracion_cita_default": 30,
            "permite_citas_online": true,
            "requiere_confirmacion": false,
            "total_negocios": 5
        }
    ]
}
```

### 3. Negocios (`/api/negocios/`)

#### Crear Negocio
```
POST /api/negocios/
```

**Parámetros:**
```json
{
    "categoria": 1,
    "nombre": "Mi Peluquería",
    "descripcion": "La mejor peluquería de la ciudad",
    "telefono": "123456789",
    "email": "contacto@mipeluqueria.com",
    "direccion": "Calle Principal 123",
    "ciudad": "Madrid",
    "provincia": "Madrid",
    "codigo_postal": "28001"
}
```

#### Obtener Estadísticas del Negocio
```
GET /api/negocios/{id}/estadisticas/
```

**Respuesta:**
```json
{
    "total_citas": 150,
    "citas_pendientes": 5,
    "citas_confirmadas": 10,
    "citas_completadas": 120,
    "citas_canceladas": 15,
    "ingresos_mes_actual": "1250.00",
    "calificacion_promedio": "4.50",
    "total_clientes": 85
}
```

#### Consultar Disponibilidad
```
GET /api/negocios/{id}/disponibilidad/?fecha=2024-01-15&servicio=1
```

**Respuesta:**
```json
{
    "fecha": "2024-01-15",
    "horarios_disponibles": [
        "09:00:00",
        "09:30:00",
        "10:00:00",
        "14:00:00"
    ]
}
```

#### Filtros Disponibles
- `categoria`: Filtrar por categoría
- `ciudad`: Filtrar por ciudad
- `cerca_de`: Buscar cerca de una ubicación
- `precio_desde`: Precio mínimo de servicios
- `precio_hasta`: Precio máximo de servicios
- `calificacion_minima`: Calificación mínima
- `con_disponibilidad`: Solo negocios con disponibilidad hoy

### 4. Servicios de Negocio (`/api/servicios-negocio/`)

#### Crear Servicio
```
POST /api/servicios-negocio/
```

**Parámetros:**
```json
{
    "negocio": 1,
    "nombre": "Corte de Cabello",
    "descripcion": "Corte profesional",
    "duracion_minutos": 30,
    "precio": "15.00",
    "requiere_confirmacion": false,
    "disponible_online": true
}
```

#### Filtros Disponibles
- `negocio`: Servicios de un negocio específico
- `precio_desde`: Precio mínimo
- `precio_hasta`: Precio máximo
- `duracion_desde`: Duración mínima en minutos
- `duracion_hasta`: Duración máxima en minutos

### 5. Citas (`/api/citas/`)

#### Crear Cita
```
POST /api/citas/
```

**Parámetros:**
```json
{
    "negocio": 1,
    "servicio": 1,
    "empleado": 1,
    "fecha_hora_inicio": "2024-01-15T10:00:00Z",
    "nombre_cliente": "Juan Pérez",
    "telefono_cliente": "123456789",
    "email_cliente": "juan@example.com",
    "notas_cliente": "Preferencia por corte corto"
}
```

#### Cambiar Estado de Cita
```
PATCH /api/citas/{id}/cambiar_estado/
```

**Parámetros:**
```json
{
    "estado": "confirmada|cancelada_cliente|cancelada_negocio|completada|no_asistio"
}
```

#### Estados de Cita
- `pendiente`: Pendiente de confirmación
- `confirmada`: Confirmada
- `en_curso`: En curso
- `completada`: Completada
- `cancelada_cliente`: Cancelada por el cliente
- `cancelada_negocio`: Cancelada por el negocio
- `no_asistio`: Cliente no asistió

#### Filtros Disponibles
- `estado`: Filtrar por estado
- `negocio`: Citas de un negocio específico
- `fecha_desde`: Citas desde una fecha
- `fecha_hasta`: Citas hasta una fecha
- `mes`: Citas de un mes específico
- `año`: Citas de un año específico

### 6. Reseñas (`/api/reseñas/`)

#### Crear Reseña
```
POST /api/reseñas/
```

**Parámetros:**
```json
{
    "negocio": 1,
    "cita": 1,
    "calificacion": 5,
    "comentario": "Excelente servicio",
    "calificacion_servicio": 5,
    "calificacion_atencion": 5,
    "calificacion_instalaciones": 4
}
```

#### Filtros Disponibles
- `negocio`: Reseñas de un negocio específico
- `calificacion_minima`: Calificación mínima
- `calificacion_maxima`: Calificación máxima
- `con_respuesta`: Reseñas con respuesta del negocio

### 7. Horarios de Negocio (`/api/horarios-negocio/`)

#### Crear Horario
```
POST /api/horarios-negocio/
```

**Parámetros:**
```json
{
    "negocio": 1,
    "dia_semana": 1,
    "hora_inicio": "09:00:00",
    "hora_fin": "18:00:00",
    "activo": true
}
```

**Días de la semana:**
- 0: Lunes
- 1: Martes
- 2: Miércoles
- 3: Jueves
- 4: Viernes
- 5: Sábado
- 6: Domingo

### 8. Empleados de Negocio (`/api/empleados-negocio/`)

#### Crear Empleado
```
POST /api/empleados-negocio/
```

**Parámetros:**
```json
{
    "usuario": "user-uuid",
    "negocio": 1,
    "tipo_empleado": "administrador|empleado|consultor",
    "especialidades": "Corte, Tinte, Peinado",
    "puede_crear_citas": true,
    "puede_modificar_citas": true
}
```

### 9. Bloqueos de Horario (`/api/bloqueos-horario/`)

#### Crear Bloqueo
```
POST /api/bloqueos-horario/
```

**Parámetros:**
```json
{
    "negocio": 1,
    "empleado": 1,
    "fecha_inicio": "2024-01-15T09:00:00Z",
    "fecha_fin": "2024-01-15T18:00:00Z",
    "tipo_bloqueo": "vacaciones|festivo|mantenimiento|personal|otro",
    "motivo": "Vacaciones de verano"
}
```

### 10. Facturación (`/api/facturacion/`)

Endpoint de solo lectura para consultar facturas y pagos.

## Paginación

Todos los endpoints de listado soportan paginación automática:

```json
{
    "count": 100,
    "next": "http://api.example.com/api/usuarios/?page=3",
    "previous": "http://api.example.com/api/usuarios/?page=1",
    "results": [...]
}
```

**Parámetros de paginación:**
- `page`: Número de página (por defecto: 1)
- `page_size`: Elementos por página (máximo: 20)

## Filtrado y Búsqueda

### Búsqueda de Texto
Usar el parámetro `search`:
```
GET /api/negocios/?search=peluquería
```

### Ordenamiento
Usar el parámetro `ordering`:
```
GET /api/negocios/?ordering=-calificacion_promedio,nombre
```

Prefijo `-` para orden descendente.

### Filtros Múltiples
Los filtros se pueden combinar:
```
GET /api/citas/?estado=confirmada&fecha_desde=2024-01-01&negocio=1
```

## Códigos de Estado HTTP

- `200 OK`: Operación exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Error en los datos enviados
- `401 Unauthorized`: No autenticado
- `403 Forbidden`: Sin permisos
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Estructura de Errores

```json
{
    "detail": "Mensaje de error específico"
}
```

O para errores de validación:

```json
{
    "field_name": [
        "Este campo es requerido."
    ],
    "non_field_errors": [
        "Error general de validación."
    ]
}
```

## Ejemplos de Uso

### Flujo Completo de Reserva

1. **Cliente se registra:**
```bash
curl -X POST http://localhost:8000/api/usuarios/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "cliente1",
    "email": "cliente@example.com",
    "password": "pass123",
    "password_confirm": "pass123",
    "first_name": "Juan",
    "last_name": "Pérez",
    "tipo_usuario": "cliente"
  }'
```

2. **Cliente hace login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "cliente1",
    "password": "pass123"
  }'
```

3. **Cliente busca negocios:**
```bash
curl -X GET "http://localhost:8000/api/negocios/?ciudad=Madrid&categoria=1" \
  -H "Authorization: Token YOUR_TOKEN"
```

4. **Cliente ve servicios:**
```bash
curl -X GET "http://localhost:8000/api/servicios-negocio/?negocio=1" \
  -H "Authorization: Token YOUR_TOKEN"
```

5. **Cliente consulta disponibilidad:**
```bash
curl -X GET "http://localhost:8000/api/negocios/1/disponibilidad/?fecha=2024-01-15" \
  -H "Authorization: Token YOUR_TOKEN"
```

6. **Cliente reserva cita:**
```bash
curl -X POST http://localhost:8000/api/citas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "negocio": 1,
    "servicio": 1,
    "fecha_hora_inicio": "2024-01-15T10:00:00Z",
    "nombre_cliente": "Juan Pérez",
    "telefono_cliente": "123456789",
    "email_cliente": "cliente@example.com"
  }'
```

## Seguridad

- **Autenticación requerida** para la mayoría de endpoints
- **Permisos basados en roles** (cliente, negocio, empleado)
- **Validación de propietario** para operaciones sensibles
- **Tokens seguros** para autenticación
- **Validación de entrada** en todos los endpoints

## Limitaciones

- Máximo 20 elementos por página
- Tokens no expiran automáticamente
- Límites de rate limiting pueden aplicar en producción

## Soporte

Para soporte técnico o preguntas sobre la API, contactar al equipo de desarrollo.