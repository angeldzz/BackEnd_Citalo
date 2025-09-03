import django_filters
from django.db.models import Q
from .models import (
    Usuario, CategoriaNegocio, Negocio, EmpleadoNegocio, 
    ServicioNegocio, HorarioNegocio, BloqueoHorario, Cita,
    ReseñaNegocio, FacturacionSuscripcion
)


class UsuarioFilter(django_filters.FilterSet):
    """Filtros para Usuario"""
    nombre = django_filters.CharFilter(method='filter_by_name', label='Nombre completo')
    ciudad_provincia = django_filters.CharFilter(method='filter_by_location', label='Ciudad o Provincia')
    fecha_registro_desde = django_filters.DateFilter(field_name='fecha_creacion', lookup_expr='gte')
    fecha_registro_hasta = django_filters.DateFilter(field_name='fecha_creacion', lookup_expr='lte')

    class Meta:
        model = Usuario
        fields = {
            'tipo_usuario': ['exact'],
            'ciudad': ['exact', 'icontains'],
            'provincia': ['exact', 'icontains'],
            'is_active': ['exact'],
            'email_verificado': ['exact'],
            'telefono_verificado': ['exact'],
        }

    def filter_by_name(self, queryset, name, value):
        """Filtrar por nombre completo o partes del nombre"""
        return queryset.filter(
            Q(first_name__icontains=value) | 
            Q(last_name__icontains=value) |
            Q(username__icontains=value)
        )

    def filter_by_location(self, queryset, name, value):
        """Filtrar por ciudad o provincia"""
        return queryset.filter(
            Q(ciudad__icontains=value) | Q(provincia__icontains=value)
        )


class NegocioFilter(django_filters.FilterSet):
    """Filtros para Negocio"""
    nombre = django_filters.CharFilter(lookup_expr='icontains', label='Nombre del negocio')
    cerca_de = django_filters.CharFilter(method='filter_by_proximity', label='Cerca de (ciudad/provincia)')
    precio_desde = django_filters.NumberFilter(method='filter_by_min_price', label='Precio mínimo de servicios')
    precio_hasta = django_filters.NumberFilter(method='filter_by_max_price', label='Precio máximo de servicios')
    calificacion_minima = django_filters.NumberFilter(field_name='calificacion_promedio', lookup_expr='gte')
    con_disponibilidad = django_filters.BooleanFilter(method='filter_with_availability', label='Con disponibilidad hoy')

    class Meta:
        model = Negocio
        fields = {
            'categoria': ['exact'],
            'ciudad': ['exact', 'icontains'],
            'provincia': ['exact', 'icontains'],
            'estado_suscripcion': ['exact'],
            'verificado': ['exact'],
            'activo': ['exact'],
        }

    def filter_by_proximity(self, queryset, name, value):
        """Filtrar negocios cerca de una ubicación"""
        return queryset.filter(
            Q(ciudad__icontains=value) | 
            Q(provincia__icontains=value) |
            Q(direccion__icontains=value)
        )

    def filter_by_min_price(self, queryset, name, value):
        """Filtrar por precio mínimo de servicios"""
        return queryset.filter(servicios__precio__gte=value).distinct()

    def filter_by_max_price(self, queryset, name, value):
        """Filtrar por precio máximo de servicios"""
        return queryset.filter(servicios__precio__lte=value).distinct()

    def filter_with_availability(self, queryset, name, value):
        """Filtrar negocios con disponibilidad (simplificado)"""
        if value:
            from django.utils import timezone
            hoy = timezone.now().date()
            dia_semana = hoy.weekday()
            return queryset.filter(
                horarios__dia_semana=dia_semana,
                horarios__activo=True
            ).distinct()
        return queryset


class ServicioNegocioFilter(django_filters.FilterSet):
    """Filtros para ServicioNegocio"""
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    precio_desde = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_hasta = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    duracion_desde = django_filters.NumberFilter(field_name='duracion_minutos', lookup_expr='gte')
    duracion_hasta = django_filters.NumberFilter(field_name='duracion_minutos', lookup_expr='lte')

    class Meta:
        model = ServicioNegocio
        fields = {
            'negocio': ['exact'],
            'activo': ['exact'],
            'disponible_online': ['exact'],
            'requiere_confirmacion': ['exact'],
        }


class CitaFilter(django_filters.FilterSet):
    """Filtros para Cita"""
    fecha_desde = django_filters.DateFilter(field_name='fecha_hora_inicio', lookup_expr='date__gte')
    fecha_hasta = django_filters.DateFilter(field_name='fecha_hora_inicio', lookup_expr='date__lte')
    mes = django_filters.NumberFilter(field_name='fecha_hora_inicio', lookup_expr='month')
    año = django_filters.NumberFilter(field_name='fecha_hora_inicio', lookup_expr='year')
    cliente_nombre = django_filters.CharFilter(lookup_expr='icontains', field_name='nombre_cliente')
    precio_desde = django_filters.NumberFilter(field_name='precio_final', lookup_expr='gte')
    precio_hasta = django_filters.NumberFilter(field_name='precio_final', lookup_expr='lte')

    class Meta:
        model = Cita
        fields = {
            'estado': ['exact'],
            'negocio': ['exact'],
            'cliente': ['exact'],
            'empleado': ['exact'],
            'servicio': ['exact'],
        }


class ReseñaNegocioFilter(django_filters.FilterSet):
    """Filtros para ReseñaNegocio"""
    calificacion_minima = django_filters.NumberFilter(field_name='calificacion', lookup_expr='gte')
    calificacion_maxima = django_filters.NumberFilter(field_name='calificacion', lookup_expr='lte')
    fecha_desde = django_filters.DateFilter(field_name='fecha_creacion', lookup_expr='date__gte')
    fecha_hasta = django_filters.DateFilter(field_name='fecha_creacion', lookup_expr='date__lte')
    con_respuesta = django_filters.BooleanFilter(method='filter_with_response')

    class Meta:
        model = ReseñaNegocio
        fields = {
            'negocio': ['exact'],
            'cliente': ['exact'],
            'calificacion': ['exact'],
            'activa': ['exact'],
        }

    def filter_with_response(self, queryset, name, value):
        """Filtrar reseñas con o sin respuesta del negocio"""
        if value:
            return queryset.filter(respuesta_negocio__isnull=False)
        else:
            return queryset.filter(respuesta_negocio__isnull=True)


class FacturacionSuscripcionFilter(django_filters.FilterSet):
    """Filtros para FacturacionSuscripcion"""
    monto_desde = django_filters.NumberFilter(field_name='monto', lookup_expr='gte')
    monto_hasta = django_filters.NumberFilter(field_name='monto', lookup_expr='lte')
    periodo_desde = django_filters.DateFilter(field_name='periodo_inicio', lookup_expr='gte')
    periodo_hasta = django_filters.DateFilter(field_name='periodo_fin', lookup_expr='lte')
    vencimiento_proximo = django_filters.BooleanFilter(method='filter_upcoming_due')

    class Meta:
        model = FacturacionSuscripcion
        fields = {
            'negocio': ['exact'],
            'estado_pago': ['exact'],
            'moneda': ['exact'],
        }

    def filter_upcoming_due(self, queryset, name, value):
        """Filtrar facturas con vencimiento próximo (próximos 7 días)"""
        if value:
            from django.utils import timezone
            from datetime import timedelta
            fecha_limite = timezone.now() + timedelta(days=7)
            return queryset.filter(
                fecha_vencimiento__lte=fecha_limite,
                estado_pago='pendiente'
            )
        return queryset


class HorarioNegocioFilter(django_filters.FilterSet):
    """Filtros para HorarioNegocio"""
    class Meta:
        model = HorarioNegocio
        fields = {
            'negocio': ['exact'],
            'dia_semana': ['exact'],
            'activo': ['exact'],
        }


class BloqueoHorarioFilter(django_filters.FilterSet):
    """Filtros para BloqueoHorario"""
    fecha_desde = django_filters.DateFilter(field_name='fecha_inicio', lookup_expr='date__gte')
    fecha_hasta = django_filters.DateFilter(field_name='fecha_fin', lookup_expr='date__lte')
    activos_en_fecha = django_filters.DateFilter(method='filter_active_on_date')

    class Meta:
        model = BloqueoHorario
        fields = {
            'negocio': ['exact'],
            'empleado': ['exact'],
            'tipo_bloqueo': ['exact'],
            'activo': ['exact'],
        }

    def filter_active_on_date(self, queryset, name, value):
        """Filtrar bloqueos activos en una fecha específica"""
        from django.utils import timezone
        fecha = timezone.make_aware(timezone.datetime.combine(value, timezone.datetime.min.time()))
        fecha_fin = fecha.replace(hour=23, minute=59, second=59)
        
        return queryset.filter(
            fecha_inicio__lte=fecha_fin,
            fecha_fin__gte=fecha,
            activo=True
        )


class EmpleadoNegocioFilter(django_filters.FilterSet):
    """Filtros para EmpleadoNegocio"""
    nombre_empleado = django_filters.CharFilter(method='filter_by_employee_name')
    especialidad = django_filters.CharFilter(method='filter_by_specialty')

    class Meta:
        model = EmpleadoNegocio
        fields = {
            'negocio': ['exact'],
            'tipo_empleado': ['exact'],
            'activo': ['exact'],
        }

    def filter_by_employee_name(self, queryset, name, value):
        """Filtrar por nombre del empleado"""
        return queryset.filter(
            Q(usuario__first_name__icontains=value) |
            Q(usuario__last_name__icontains=value) |
            Q(usuario__username__icontains=value)
        )

    def filter_by_specialty(self, queryset, name, value):
        """Filtrar por especialidad"""
        return queryset.filter(especialidades__icontains=value)