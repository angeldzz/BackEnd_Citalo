from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import (
    Usuario, CategoriaNegocio, Negocio, EmpleadoNegocio, 
    ServicioNegocio, HorarioNegocio, BloqueoHorario, Cita,
    ReseñaNegocio, FacturacionSuscripcion, ConfiguracionPlataforma
)


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Usuario"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    nombre_completo = serializers.CharField(read_only=True)
    iniciales = serializers.CharField(read_only=True, source='get_iniciales')
    es_propietario_negocio = serializers.BooleanField(read_only=True)
    tiene_perfil_completo = serializers.BooleanField(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'tipo_usuario', 'genero', 'fecha_nacimiento', 'telefono', 
            'telefono_alternativo', 'direccion', 'ciudad', 'provincia',
            'codigo_postal', 'pais', 'avatar', 'biografia',
            'notificaciones_email', 'notificaciones_sms', 'notificaciones_push',
            'idioma_preferido', 'zona_horaria', 'email_verificado', 
            'telefono_verificado', 'is_active', 'fecha_creacion',
            'fecha_actualizacion', 'ultima_actividad', 'password',
            'password_confirm', 'nombre_completo', 'iniciales',
            'es_propietario_negocio', 'tiene_perfil_completo'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'fecha_creacion': {'read_only': True},
            'fecha_actualizacion': {'read_only': True},
            'ultima_actividad': {'read_only': True},
        }

    def validate(self, attrs):
        if 'password' in attrs and 'password_confirm' in attrs:
            if attrs['password'] != attrs['password_confirm']:
                raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        user = Usuario.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance


class UsuarioPublicSerializer(serializers.ModelSerializer):
    """Serializer público para mostrar información básica del usuario"""
    nombre_completo = serializers.CharField(read_only=True)
    iniciales = serializers.CharField(read_only=True, source='get_iniciales')

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name', 'avatar',
            'biografia', 'nombre_completo', 'iniciales'
        ]


class LoginSerializer(serializers.Serializer):
    """Serializer para login de usuarios"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Credenciales inválidas')
            if not user.is_active:
                raise serializers.ValidationError('Usuario inactivo')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Debe proporcionar username y password')

        return attrs


class CategoriaNegocioSerializer(serializers.ModelSerializer):
    """Serializer para CategoriaNegocio"""
    total_negocios = serializers.SerializerMethodField()

    class Meta:
        model = CategoriaNegocio
        fields = [
            'id', 'nombre', 'descripcion', 'icono', 'activa', 'orden',
            'duracion_cita_default', 'permite_citas_online', 'requiere_confirmacion',
            'total_negocios'
        ]

    def get_total_negocios(self, obj):
        return obj.negocios.filter(activo=True).count()


class NegocioSerializer(serializers.ModelSerializer):
    """Serializer para Negocio"""
    propietario_info = UsuarioPublicSerializer(source='propietario', read_only=True)
    categoria_info = CategoriaNegocioSerializer(source='categoria', read_only=True)
    suscripcion_activa = serializers.BooleanField(read_only=True)
    total_empleados = serializers.SerializerMethodField()
    total_servicios = serializers.SerializerMethodField()

    class Meta:
        model = Negocio
        fields = [
            'id', 'propietario', 'categoria', 'nombre', 'descripcion', 'slug',
            'telefono', 'email', 'sitio_web', 'direccion', 'ciudad', 'provincia',
            'codigo_postal', 'latitud', 'longitud', 'logo', 'imagen_portada',
            'zona_horaria', 'tiempo_anticipacion_minimo', 'tiempo_cancelacion_limite',
            'permite_reservas_multiples', 'estado_suscripcion', 'fecha_inicio_suscripcion',
            'fecha_fin_suscripcion', 'calificacion_promedio', 'total_reseñas',
            'activo', 'verificado', 'fecha_creacion', 'fecha_actualizacion',
            'propietario_info', 'categoria_info', 'suscripcion_activa',
            'total_empleados', 'total_servicios'
        ]
        read_only_fields = [
            'propietario', 'slug', 'calificacion_promedio', 'total_reseñas', 'verificado',
            'fecha_creacion', 'fecha_actualizacion'
        ]

    def get_total_empleados(self, obj):
        return obj.empleados.filter(activo=True).count()

    def get_total_servicios(self, obj):
        return obj.servicios.filter(activo=True).count()


class EmpleadoNegocioSerializer(serializers.ModelSerializer):
    """Serializer para EmpleadoNegocio"""
    usuario_info = UsuarioPublicSerializer(source='usuario', read_only=True)
    negocio_info = serializers.StringRelatedField(source='negocio', read_only=True)
    especialidades_list = serializers.SerializerMethodField()

    class Meta:
        model = EmpleadoNegocio
        fields = [
            'id', 'usuario', 'negocio', 'tipo_empleado', 'especialidades',
            'activo', 'fecha_incorporacion', 'fecha_baja', 'puede_crear_citas',
            'puede_modificar_citas', 'puede_cancelar_citas', 'puede_gestionar_horarios',
            'puede_ver_estadisticas', 'usuario_info', 'negocio_info', 'especialidades_list'
        ]

    def get_especialidades_list(self, obj):
        if obj.especialidades:
            return [esp.strip() for esp in obj.especialidades.split(',')]
        return []


class ServicioNegocioSerializer(serializers.ModelSerializer):
    """Serializer para ServicioNegocio"""
    negocio_info = serializers.StringRelatedField(source='negocio', read_only=True)
    empleados_autorizados_info = UsuarioPublicSerializer(
        many=True, source='empleados_autorizados.usuario', read_only=True
    )
    precio_formateado = serializers.SerializerMethodField()

    class Meta:
        model = ServicioNegocio
        fields = [
            'id', 'negocio', 'nombre', 'descripcion', 'duracion_minutos', 'precio',
            'requiere_confirmacion', 'disponible_online', 'maximo_por_dia',
            'empleados_autorizados', 'orden', 'activo', 'fecha_creacion',
            'negocio_info', 'empleados_autorizados_info', 'precio_formateado'
        ]

    def get_precio_formateado(self, obj):
        return f"€{obj.precio}"


class HorarioNegocioSerializer(serializers.ModelSerializer):
    """Serializer para HorarioNegocio"""
    dia_semana_display = serializers.CharField(source='get_dia_semana_display', read_only=True)
    negocio_info = serializers.StringRelatedField(source='negocio', read_only=True)

    class Meta:
        model = HorarioNegocio
        fields = [
            'id', 'negocio', 'dia_semana', 'hora_inicio', 'hora_fin', 'activo',
            'fecha_inicio_vigencia', 'fecha_fin_vigencia', 'dia_semana_display',
            'negocio_info'
        ]


class BloqueoHorarioSerializer(serializers.ModelSerializer):
    """Serializer para BloqueoHorario"""
    negocio_info = serializers.StringRelatedField(source='negocio', read_only=True)
    empleado_info = UsuarioPublicSerializer(source='empleado.usuario', read_only=True)
    tipo_bloqueo_display = serializers.CharField(source='get_tipo_bloqueo_display', read_only=True)

    class Meta:
        model = BloqueoHorario
        fields = [
            'id', 'negocio', 'empleado', 'fecha_inicio', 'fecha_fin', 'tipo_bloqueo',
            'motivo', 'activo', 'fecha_creacion', 'negocio_info', 'empleado_info',
            'tipo_bloqueo_display'
        ]


class CitaSerializer(serializers.ModelSerializer):
    """Serializer para Cita"""
    negocio_info = NegocioSerializer(source='negocio', read_only=True)
    cliente_info = UsuarioPublicSerializer(source='cliente', read_only=True)
    empleado_info = UsuarioPublicSerializer(source='empleado.usuario', read_only=True)
    servicio_info = ServicioNegocioSerializer(source='servicio', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    precio_final_formateado = serializers.SerializerMethodField()
    duracion_minutos = serializers.SerializerMethodField()

    class Meta:
        model = Cita
        fields = [
            'id', 'negocio', 'cliente', 'empleado', 'servicio', 'fecha_hora_inicio',
            'fecha_hora_fin', 'estado', 'nombre_cliente', 'telefono_cliente',
            'email_cliente', 'notas_cliente', 'notas_internas', 'precio_final',
            'recordatorio_enviado', 'confirmacion_enviada', 'fecha_creacion',
            'fecha_actualizacion', 'fecha_cancelacion', 'cita_original',
            'negocio_info', 'cliente_info', 'empleado_info', 'servicio_info',
            'estado_display', 'precio_final_formateado', 'duracion_minutos'
        ]
        read_only_fields = [
            'fecha_hora_fin', 'precio_final', 'fecha_creacion', 'fecha_actualizacion'
        ]

    def get_precio_final_formateado(self, obj):
        if obj.precio_final:
            return f"€{obj.precio_final}"
        return None

    def get_duracion_minutos(self, obj):
        return obj.servicio.duracion_minutos if obj.servicio else None


class ReseñaNegocioSerializer(serializers.ModelSerializer):
    """Serializer para ReseñaNegocio"""
    negocio_info = serializers.StringRelatedField(source='negocio', read_only=True)
    cliente_info = UsuarioPublicSerializer(source='cliente', read_only=True)
    cita_info = serializers.StringRelatedField(source='cita', read_only=True)

    class Meta:
        model = ReseñaNegocio
        fields = [
            'id', 'negocio', 'cliente', 'cita', 'calificacion', 'comentario',
            'calificacion_servicio', 'calificacion_atencion', 'calificacion_instalaciones',
            'respuesta_negocio', 'fecha_respuesta', 'activa', 'fecha_creacion',
            'negocio_info', 'cliente_info', 'cita_info'
        ]
        read_only_fields = ['cliente', 'fecha_creacion']


class FacturacionSuscripcionSerializer(serializers.ModelSerializer):
    """Serializer para FacturacionSuscripcion"""
    negocio_info = serializers.StringRelatedField(source='negocio', read_only=True)
    estado_pago_display = serializers.CharField(source='get_estado_pago_display', read_only=True)
    monto_formateado = serializers.SerializerMethodField()

    class Meta:
        model = FacturacionSuscripcion
        fields = [
            'id', 'negocio', 'stripe_invoice_id', 'stripe_payment_intent_id',
            'stripe_subscription_id', 'monto', 'moneda', 'periodo_inicio',
            'periodo_fin', 'estado_pago', 'fecha_vencimiento', 'fecha_pago',
            'numero_factura', 'datos_fiscales', 'fecha_creacion', 'fecha_actualizacion',
            'negocio_info', 'estado_pago_display', 'monto_formateado'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

    def get_monto_formateado(self, obj):
        return f"{obj.monto} {obj.moneda}"


class ConfiguracionPlataformaSerializer(serializers.ModelSerializer):
    """Serializer para ConfiguracionPlataforma"""
    valor_procesado = serializers.SerializerMethodField()

    class Meta:
        model = ConfiguracionPlataforma
        fields = [
            'id', 'clave', 'valor', 'descripcion', 'tipo_dato', 'activa',
            'fecha_creacion', 'fecha_actualizacion', 'valor_procesado'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']

    def get_valor_procesado(self, obj):
        return obj.get_valor()


# Serializers específicos para operaciones especiales

class CitaCreateSerializer(serializers.ModelSerializer):
    """Serializer específico para crear citas"""
    class Meta:
        model = Cita
        fields = [
            'negocio', 'empleado', 'servicio', 'fecha_hora_inicio',
            'nombre_cliente', 'telefono_cliente', 'email_cliente', 'notas_cliente'
        ]

    def validate(self, attrs):
        # Validar que la fecha de la cita no esté en el pasado
        from django.utils import timezone
        if attrs['fecha_hora_inicio'] <= timezone.now():
            raise serializers.ValidationError("La fecha de la cita debe ser futura")
        
        # Validar que el empleado pertenezca al negocio
        if attrs.get('empleado') and attrs['empleado'].negocio != attrs['negocio']:
            raise serializers.ValidationError("El empleado no pertenece a este negocio")
            
        return attrs

    def create(self, validated_data):
        # Asignar el cliente desde el contexto (usuario autenticado)
        validated_data['cliente'] = self.context['request'].user
        return super().create(validated_data)


class NegocioEstadisticasSerializer(serializers.Serializer):
    """Serializer para estadísticas del negocio"""
    total_citas = serializers.IntegerField()
    citas_pendientes = serializers.IntegerField()
    citas_confirmadas = serializers.IntegerField()
    citas_completadas = serializers.IntegerField()
    citas_canceladas = serializers.IntegerField()
    ingresos_mes_actual = serializers.DecimalField(max_digits=10, decimal_places=2)
    calificacion_promedio = serializers.DecimalField(max_digits=3, decimal_places=2)
    total_clientes = serializers.IntegerField()


class DisponibilidadSerializer(serializers.Serializer):
    """Serializer para consultar disponibilidad de horarios"""
    fecha = serializers.DateField()
    horarios_disponibles = serializers.ListField(
        child=serializers.TimeField(),
        read_only=True
    )