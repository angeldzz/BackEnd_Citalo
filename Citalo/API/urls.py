from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    UsuarioViewSet, CategoriaNegocioViewSet, NegocioViewSet, 
    EmpleadoNegocioViewSet, ServicioNegocioViewSet, HorarioNegocioViewSet,
    BloqueoHorarioViewSet, CitaViewSet, ReseñaNegocioViewSet,
    FacturacionSuscripcionViewSet, ConfiguracionPlataformaViewSet,
    CustomAuthToken, logout_view
)

app_name = 'api'

# Configurar el router para las APIs
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'categorias-negocio', CategoriaNegocioViewSet, basename='categoria-negocio')
router.register(r'negocios', NegocioViewSet, basename='negocio')
router.register(r'empleados-negocio', EmpleadoNegocioViewSet, basename='empleado-negocio')
router.register(r'servicios-negocio', ServicioNegocioViewSet, basename='servicio-negocio')
router.register(r'horarios-negocio', HorarioNegocioViewSet, basename='horario-negocio')
router.register(r'bloqueos-horario', BloqueoHorarioViewSet, basename='bloqueo-horario')
router.register(r'citas', CitaViewSet, basename='cita')
router.register(r'reseñas', ReseñaNegocioViewSet, basename='reseña')
router.register(r'facturacion', FacturacionSuscripcionViewSet, basename='facturacion')
router.register(r'configuracion', ConfiguracionPlataformaViewSet, basename='configuracion')

urlpatterns = [
    # Autenticación
    path('auth/login/', CustomAuthToken.as_view(), name='login'),
    path('auth/logout/', logout_view, name='logout'),
    
    # API endpoints
    path('', include(router.urls)),
]
