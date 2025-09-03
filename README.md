# Citalo - Backend API

Sistema completo de gestión de citas para negocios desarrollado con Django REST Framework.

## Descripción

Citalo es una plataforma que permite a los negocios gestionar sus servicios, horarios, empleados y citas de manera eficiente. Los clientes pueden buscar negocios, ver servicios disponibles, consultar disponibilidad y reservar citas fácilmente.

## Características Principales

- 🔐 **Sistema de autenticación** con tokens JWT
- 👥 **Gestión de usuarios** (clientes, negocios, empleados, administradores)
- 🏢 **Gestión de negocios** con categorías y ubicaciones
- 💼 **Gestión de servicios** con precios y duraciones
- 📅 **Sistema de horarios** flexible por días de la semana
- 📝 **Sistema de citas** con diferentes estados
- ⭐ **Sistema de reseñas** y calificaciones
- 👨‍💼 **Gestión de empleados** con permisos específicos
- 🚫 **Bloqueos de horarios** para vacaciones, festivos, etc.
- 💰 **Sistema de facturación** y suscripciones
- 🔍 **Búsqueda y filtrado** avanzado
- 📊 **Estadísticas** para negocios
- 📖 **Documentación completa** con Swagger/OpenAPI

## Tecnologías Utilizadas

- **Python 3.12+**
- **Django 5.2+**
- **Django REST Framework 3.16+**
- **SQLite** (desarrollo) / **PostgreSQL** (producción)
- **drf-spectacular** (documentación OpenAPI)
- **django-cors-headers** (CORS)
- **django-filter** (filtrado)
- **Pillow** (manejo de imágenes)

## Instalación y Configuración

### Prerrequisitos

- Python 3.12 o superior
- pip (gestor de paquetes de Python)
- Git

### 1. Clonar el repositorio

```bash
git clone https://github.com/angeldzz/BackEnd_Citalo.git
cd BackEnd_Citalo
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Django Configuration
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True

# Database Configuration
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

### 5. Ejecutar migraciones

```bash
cd Citalo
python manage.py migrate
```

### 6. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 7. Cargar datos de prueba (opcional)

```bash
python manage.py loaddata fixtures/inicial.json
```

### 8. Ejecutar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## URLs Principales

- **API Base**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`
- **Documentación Swagger**: `http://localhost:8000/api/docs/`
- **Documentación ReDoc**: `http://localhost:8000/api/redoc/`
- **Schema OpenAPI**: `http://localhost:8000/api/schema/`

## Estructura del Proyecto

```
BackEnd_Citalo/
├── Citalo/                     # Proyecto Django principal
│   ├── Citalo/                 # Configuración del proyecto
│   │   ├── settings.py         # Configuración Django
│   │   ├── urls.py            # URLs principales
│   │   └── ...
│   ├── API/                    # Aplicación principal de la API
│   │   ├── models.py          # Modelos de datos
│   │   ├── serializers.py     # Serializers DRF
│   │   ├── views.py           # Vistas de la API
│   │   ├── urls.py            # URLs de la API
│   │   ├── filters.py         # Filtros personalizados
│   │   ├── tests.py           # Tests de la aplicación
│   │   └── ...
│   ├── static/                 # Archivos estáticos
│   ├── media/                  # Archivos de medios subidos
│   ├── manage.py               # Script de gestión Django
│   └── db.sqlite3              # Base de datos SQLite
├── requirements.txt            # Dependencias Python
├── .env                        # Variables de entorno
├── API_DOCUMENTATION.md        # Documentación completa de la API
└── README.md                   # Este archivo
```

## Modelos Principales

### Usuario
- Modelo personalizado basado en AbstractUser
- Tipos: cliente, negocio, empleado, admin
- Campos adicionales: teléfono, dirección, avatar, preferencias

### CategoriaNegocio
- Categorías para clasificar negocios
- Configuraciones específicas por categoría

### Negocio
- Información del negocio: nombre, dirección, contacto
- Estado de suscripción y verificación
- Métricas: calificación promedio, total de reseñas

### ServicioNegocio
- Servicios ofrecidos por cada negocio
- Precio, duración, descripción
- Empleados autorizados para cada servicio

### Cita
- Reservas de clientes en negocios
- Estados: pendiente, confirmada, completada, cancelada
- Información del cliente y notas

### HorarioNegocio
- Horarios de funcionamiento por día de la semana
- Horarios especiales con fechas de vigencia

### ReseñaNegocio
- Reseñas y calificaciones de clientes
- Calificaciones específicas por aspecto
- Respuestas del negocio

## API Endpoints

### Autenticación
- `POST /api/auth/login/` - Iniciar sesión
- `POST /api/auth/logout/` - Cerrar sesión

### Gestión de Usuarios
- `GET /api/usuarios/` - Listar usuarios
- `POST /api/usuarios/` - Registrar usuario
- `GET /api/usuarios/me/` - Perfil propio
- `PATCH /api/usuarios/me/` - Actualizar perfil
- `POST /api/usuarios/{id}/change_password/` - Cambiar contraseña

### Negocios
- `GET /api/negocios/` - Listar negocios
- `POST /api/negocios/` - Crear negocio
- `GET /api/negocios/{id}/estadisticas/` - Estadísticas
- `GET /api/negocios/{id}/disponibilidad/` - Consultar disponibilidad

### Servicios
- `GET /api/servicios-negocio/` - Listar servicios
- `POST /api/servicios-negocio/` - Crear servicio

### Citas
- `GET /api/citas/` - Listar citas
- `POST /api/citas/` - Crear cita
- `PATCH /api/citas/{id}/cambiar_estado/` - Cambiar estado

### Reseñas
- `GET /api/reseñas/` - Listar reseñas
- `POST /api/reseñas/` - Crear reseña

Ver [API_DOCUMENTATION.md](API_DOCUMENTATION.md) para documentación completa.

## Testing

### Ejecutar todos los tests

```bash
python manage.py test
```

### Ejecutar tests específicos

```bash
python manage.py test API.tests.AuthenticationTestCase
python manage.py test API.tests.UsuarioAPITestCase
python manage.py test API.tests.CitaAPITestCase
```

### Ejecutar tests con cobertura

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Genera reporte HTML
```

### Tests Incluidos

- ✅ Tests de autenticación (login, logout, tokens)
- ✅ Tests de gestión de usuarios (registro, perfil, contraseñas)
- ✅ Tests de CRUD para todos los modelos
- ✅ Tests de permisos y autorización
- ✅ Tests de filtrado y búsqueda
- ✅ Tests de validaciones de negocio
- ✅ Tests de integración completos
- ✅ Tests de endpoints específicos (estadísticas, disponibilidad)

## Configuración para Producción

### Variables de Entorno para Producción

```env
SECRET_KEY=clave-super-secreta-para-produccion
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# Base de datos PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=citalo_prod
DB_USER=citalo_user
DB_PASSWORD=password_seguro
DB_HOST=localhost
DB_PORT=5432

# Configuración de archivos estáticos
STATIC_ROOT=/var/www/citalo/static/
MEDIA_ROOT=/var/www/citalo/media/
```

### Comandos para Producción

```bash
# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

## Funcionalidades Adicionales Implementadas

### 1. Sistema de Filtrado Avanzado
- Filtros personalizados para todos los modelos
- Búsqueda por texto en múltiples campos
- Filtros por rango de fechas, precios, calificaciones
- Filtros geográficos (ciudad, provincia)

### 2. Sistema de Permisos
- Permisos basados en roles de usuario
- Propietarios pueden gestionar sus negocios
- Empleados con permisos específicos
- Clientes solo pueden ver sus propias citas

### 3. Validaciones de Negocio
- Validación de horarios de citas
- Prevención de citas en el pasado
- Validación de empleados autorizados
- Verificación de disponibilidad

### 4. Estadísticas y Métricas
- Dashboard de estadísticas para negocios
- Cálculo automático de ingresos
- Conteo de citas por estado
- Métricas de clientes únicos

### 5. Sistema de Disponibilidad
- Consulta de horarios disponibles
- Consideración de horarios de negocio
- Detección de citas existentes
- Manejo de bloqueos de horarios

## Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para reportar bugs o solicitar nuevas funcionalidades, por favor crear un issue en GitHub.

## Autor

**Angel** - [angeldzz](https://github.com/angeldzz)

---

⭐ Si te gusta este proyecto, ¡no olvides darle una estrella en GitHub!