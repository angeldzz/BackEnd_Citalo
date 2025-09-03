from django.shortcuts import render
from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db.models import Q, Count, Sum, Avg
from datetime import datetime, timedelta, time
from decimal import Decimal

from .models import (
    Usuario, CategoriaNegocio, Negocio, EmpleadoNegocio, 
    ServicioNegocio, HorarioNegocio, BloqueoHorario, Cita,
    ReseñaNegocio, FacturacionSuscripcion, ConfiguracionPlataforma
)
from .serializers import (
    UsuarioSerializer, UsuarioPublicSerializer, LoginSerializer,
    CategoriaNegocioSerializer, NegocioSerializer, EmpleadoNegocioSerializer,
    ServicioNegocioSerializer, HorarioNegocioSerializer, BloqueoHorarioSerializer,
    CitaSerializer, CitaCreateSerializer, ReseñaNegocioSerializer,
    FacturacionSuscripcionSerializer, ConfiguracionPlataformaSerializer,
    NegocioEstadisticasSerializer, DisponibilidadSerializer
)
from .filters import (
    UsuarioFilter, NegocioFilter, ServicioNegocioFilter, CitaFilter,
    ReseñaNegocioFilter, FacturacionSuscripcionFilter, HorarioNegocioFilter,
    BloqueoHorarioFilter, EmpleadoNegocioFilter
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado que solo permite a los propietarios editar sus objetos
    """
    def has_object_permission(self, request, view, obj):
        # Permisos de lectura para cualquier request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permisos de escritura solo para el propietario del objeto
        if hasattr(obj, 'propietario'):
            return obj.propietario == request.user
        elif hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        elif hasattr(obj, 'cliente'):
            return obj.cliente == request.user
        return obj == request.user


class IsBusinessOwnerOrEmployee(permissions.BasePermission):
    """
    Permiso que permite acceso a propietarios del negocio y empleados autorizados
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Verificar si es propietario del negocio
        if hasattr(obj, 'negocio'):
            if obj.negocio.propietario == request.user:
                return True
            # Verificar si es empleado del negocio
            return obj.negocio.empleados.filter(
                usuario=request.user, 
                activo=True
            ).exists()
        return False


class CustomAuthToken(ObtainAuthToken):
    """Vista personalizada para autenticación con token"""
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Actualizar última actividad
        user.ultima_actividad = timezone.now()
        user.save(update_fields=['ultima_actividad'])
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'tipo_usuario': user.tipo_usuario,
            'nombre_completo': user.get_nombre_completo()
        })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout_view(request):
    """Vista para logout que elimina el token"""
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Logout exitoso'}, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Error en logout'}, status=status.HTTP_400_BAD_REQUEST)


class UsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de usuarios"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = UsuarioFilter
    search_fields = ['username', 'email', 'first_name', 'last_name', 'telefono']
    ordering_fields = ['fecha_creacion', 'last_login', 'first_name']
    ordering = ['-fecha_creacion']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] and self.request.user != self.get_object():
            return UsuarioPublicSerializer
        return UsuarioSerializer

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """Endpoint para obtener/actualizar el perfil del usuario actual"""
        if request.method == 'GET':
            serializer = UsuarioSerializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = UsuarioSerializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """Cambiar contraseña del usuario"""
        user = self.get_object()
        if user != request.user:
            return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
            
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response({'error': 'Contraseña actual incorrecta'}, status=status.HTTP_400_BAD_REQUEST)
            
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Contraseña actualizada exitosamente'})


class CategoriaNegocioViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para categorías de negocio"""
    queryset = CategoriaNegocio.objects.filter(activa=True).order_by('orden', 'nombre')
    serializer_class = CategoriaNegocioSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['orden', 'nombre']


class NegocioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de negocios"""
    queryset = Negocio.objects.filter(activo=True)
    serializer_class = NegocioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NegocioFilter
    search_fields = ['nombre', 'descripcion', 'ciudad', 'direccion']
    ordering_fields = ['nombre', 'calificacion_promedio', 'fecha_creacion']
    ordering = ['-calificacion_promedio', 'nombre']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'disponibilidad']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(propietario=self.request.user)

    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Obtener estadísticas del negocio"""
        negocio = self.get_object()
        if negocio.propietario != request.user:
            return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)

        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        
        citas = negocio.citas.all()
        citas_mes = citas.filter(fecha_hora_inicio__date__gte=inicio_mes)
        
        estadisticas = {
            'total_citas': citas.count(),
            'citas_pendientes': citas.filter(estado='pendiente').count(),
            'citas_confirmadas': citas.filter(estado='confirmada').count(),
            'citas_completadas': citas.filter(estado='completada').count(),
            'citas_canceladas': citas.filter(estado__in=['cancelada_cliente', 'cancelada_negocio']).count(),
            'ingresos_mes_actual': citas_mes.filter(estado='completada').aggregate(
                total=Sum('precio_final'))['total'] or Decimal('0'),
            'calificacion_promedio': negocio.calificacion_promedio,
            'total_clientes': citas.values('cliente').distinct().count()
        }
        
        serializer = NegocioEstadisticasSerializer(estadisticas)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def disponibilidad(self, request, pk=None):
        """Consultar disponibilidad de horarios"""
        negocio = self.get_object()
        fecha_str = request.query_params.get('fecha')
        servicio_id = request.query_params.get('servicio')
        
        if not fecha_str:
            return Response({'error': 'Fecha requerida'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Formato de fecha inválido'}, status=status.HTTP_400_BAD_REQUEST)
            
        if fecha <= timezone.now().date():
            return Response({'error': 'La fecha debe ser futura'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener horarios del negocio para ese día
        dia_semana = fecha.weekday()
        horarios = negocio.horarios.filter(dia_semana=dia_semana, activo=True)
        
        if not horarios.exists():
            return Response({'fecha': fecha, 'horarios_disponibles': []})

        # Calcular horarios disponibles (simplificado)
        horarios_disponibles = []
        for horario in horarios:
            hora_actual = horario.hora_inicio
            while hora_actual < horario.hora_fin:
                # Verificar si hay citas en esa hora
                datetime_slot = timezone.make_aware(datetime.combine(fecha, hora_actual))
                citas_existentes = negocio.citas.filter(
                    fecha_hora_inicio=datetime_slot,
                    estado__in=['pendiente', 'confirmada']
                )
                
                if not citas_existentes.exists():
                    horarios_disponibles.append(hora_actual)
                    
                # Avanzar 30 minutos (puede ser configurable)
                hora_actual = (datetime.combine(fecha, hora_actual) + timedelta(minutes=30)).time()

        serializer = DisponibilidadSerializer({'fecha': fecha, 'horarios_disponibles': horarios_disponibles})
        return Response(serializer.data)


class EmpleadoNegocioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de empleados de negocio"""
    serializer_class = EmpleadoNegocioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EmpleadoNegocioFilter
    search_fields = ['usuario__first_name', 'usuario__last_name', 'especialidades']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return EmpleadoNegocio.objects.none()
        
        # Solo mostrar empleados de negocios del usuario actual
        return EmpleadoNegocio.objects.filter(
            negocio__propietario=self.request.user
        )

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated, IsBusinessOwnerOrEmployee]
        return [permission() for permission in permission_classes]


class ServicioNegocioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de servicios de negocio"""
    serializer_class = ServicioNegocioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ServicioNegocioFilter
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['orden', 'nombre', 'precio', 'duracion_minutos']
    ordering = ['orden', 'nombre']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ServicioNegocio.objects.none()
            
        # Filtrar por negocio si se proporciona
        negocio_id = self.request.query_params.get('negocio')
        queryset = ServicioNegocio.objects.filter(activo=True)
        
        if negocio_id:
            queryset = queryset.filter(negocio_id=negocio_id)
        elif self.request.user.is_authenticated:
            # Mostrar solo servicios de negocios del usuario
            queryset = queryset.filter(negocio__propietario=self.request.user)
            
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsBusinessOwnerOrEmployee]
        return [permission() for permission in permission_classes]


class HorarioNegocioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de horarios de negocio"""
    serializer_class = HorarioNegocioSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HorarioNegocioFilter

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return HorarioNegocio.objects.none()
            
        # Solo mostrar horarios de negocios del usuario actual
        return HorarioNegocio.objects.filter(
            negocio__propietario=self.request.user
        )

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated, IsBusinessOwnerOrEmployee]
        return [permission() for permission in permission_classes]


class BloqueoHorarioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de bloqueos de horario"""
    serializer_class = BloqueoHorarioSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BloqueoHorarioFilter
    ordering_fields = ['fecha_inicio', 'fecha_creacion']
    ordering = ['fecha_inicio']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return BloqueoHorario.objects.none()
            
        # Solo mostrar bloqueos de negocios del usuario actual
        return BloqueoHorario.objects.filter(
            negocio__propietario=self.request.user
        )

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated, IsBusinessOwnerOrEmployee]
        return [permission() for permission in permission_classes]


class CitaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de citas"""
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CitaFilter
    search_fields = ['nombre_cliente', 'telefono_cliente', 'email_cliente']
    ordering_fields = ['fecha_hora_inicio', 'fecha_creacion']
    ordering = ['fecha_hora_inicio']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cita.objects.none()
            
        user = self.request.user
        if user.tipo_usuario == 'cliente':
            return Cita.objects.filter(cliente=user)
        elif user.tipo_usuario in ['negocio', 'empleado']:
            return Cita.objects.filter(
                Q(negocio__propietario=user) | 
                Q(empleado__usuario=user)
            )
        return Cita.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return CitaCreateSerializer
        return CitaSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        """Cambiar estado de una cita"""
        cita = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if nuevo_estado not in [choice[0] for choice in Cita.ESTADO_CITA_CHOICES]:
            return Response({'error': 'Estado inválido'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar permisos según el estado
        if nuevo_estado in ['cancelada_cliente'] and cita.cliente != request.user:
            return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
        
        if nuevo_estado in ['confirmada', 'cancelada_negocio', 'completada', 'no_asistio']:
            if not (cita.negocio.propietario == request.user or 
                   cita.negocio.empleados.filter(usuario=request.user, activo=True).exists()):
                return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
        
        cita.estado = nuevo_estado
        if nuevo_estado in ['cancelada_cliente', 'cancelada_negocio']:
            cita.fecha_cancelacion = timezone.now()
        cita.save()
        
        serializer = CitaSerializer(cita)
        return Response(serializer.data)


class ReseñaNegocioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de reseñas de negocio"""
    serializer_class = ReseñaNegocioSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReseñaNegocioFilter
    ordering_fields = ['fecha_creacion', 'calificacion']
    ordering = ['-fecha_creacion']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ReseñaNegocio.objects.none()
            
        # Filtrar por negocio si se proporciona
        negocio_id = self.request.query_params.get('negocio')
        queryset = ReseñaNegocio.objects.filter(activa=True)
        
        if negocio_id:
            queryset = queryset.filter(negocio_id=negocio_id)
        elif self.request.user.is_authenticated:
            if self.request.user.tipo_usuario == 'cliente':
                queryset = queryset.filter(cliente=self.request.user)
            else:
                queryset = queryset.filter(negocio__propietario=self.request.user)
                
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)


class FacturacionSuscripcionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para facturación"""
    serializer_class = FacturacionSuscripcionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = FacturacionSuscripcionFilter
    ordering_fields = ['fecha_creacion', 'fecha_vencimiento']
    ordering = ['-fecha_creacion']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return FacturacionSuscripcion.objects.none()
            
        # Solo mostrar facturas de negocios del usuario actual
        return FacturacionSuscripcion.objects.filter(
            negocio__propietario=self.request.user
        )

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]


class ConfiguracionPlataformaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para configuración de plataforma"""
    queryset = ConfiguracionPlataforma.objects.filter(activa=True)
    serializer_class = ConfiguracionPlataformaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['clave', 'descripcion']
