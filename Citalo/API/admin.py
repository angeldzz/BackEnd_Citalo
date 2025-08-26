from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, CategoriaNegocio, Negocio, EmpleadoNegocio, 
    ServicioNegocio, HorarioNegocio, BloqueoHorario, 
    Cita, ReseñaNegocio, FacturacionSuscripcion, 
    ConfiguracionPlataforma
)

# Admin para Usuario
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = (
        'username', 'email', 'get_nombre_completo', 'tipo_usuario',
        'email_verificado', 'telefono_verificado', 'fecha_creacion', 'ultima_actividad'
    )
    list_filter = ('tipo_usuario', 'email_verificado', 'telefono_verificado', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'telefono')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'ultima_actividad', 'id')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'id')}),
        ('Información Personal', {
            'fields': (
                'first_name', 'last_name',
                'email', 'genero', 'fecha_nacimiento'
            )
        }),
        ('Información de Contacto', {
            'fields': ('telefono', 'telefono_alternativo', 'direccion', 'ciudad', 'provincia', 'codigo_postal', 'pais')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Preferencias', {
            'fields': (
                'tipo_usuario', 'avatar', 'biografia', 'notificaciones_email',
                'notificaciones_sms', 'notificaciones_push', 'idioma_preferido', 'zona_horaria'
            )
        }),
        ('Estado', {
            'fields': ('email_verificado', 'telefono_verificado', 'fecha_creacion', 'fecha_actualizacion', 'ultima_actividad')
        }),
    )

# Admin para CategoriaNegocio
@admin.register(CategoriaNegocio)
class CategoriaNegocioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa', 'orden', 'duracion_cita_default', 'permite_citas_online')
    list_filter = ('activa', 'permite_citas_online', 'requiere_confirmacion')
    search_fields = ('nombre', 'descripcion')
    ordering = ('orden', 'nombre')

# Admin para Negocio
@admin.register(Negocio)
class NegocioAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'propietario', 'categoria', 'estado_suscripcion', 
        'calificacion_promedio', 'activo', 'verificado', 'fecha_creacion'
    )
    list_filter = ('estado_suscripcion', 'activo', 'verificado', 'categoria')
    search_fields = ('nombre', 'propietario__username', 'propietario__email', 'email', 'telefono')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'id')
    fieldsets = (
        (None, {'fields': ('id', 'propietario', 'categoria', 'nombre', 'slug')}),
        ('Información de Contacto', {
            'fields': ('telefono', 'email', 'sitio_web', 'direccion', 'ciudad', 'provincia', 'codigo_postal')
        }),
        ('Ubicación', {'fields': ('latitud', 'longitud')}),
        ('Multimedia', {'fields': ('logo', 'imagen_portada')}),
        ('Configuración', {
            'fields': (
                'zona_horaria', 'tiempo_anticipacion_minimo', 'tiempo_cancelacion_limite',
                'permite_reservas_multiples', 'estado_suscripcion', 'fecha_inicio_suscripcion',
                'fecha_fin_suscripcion', 'stripe_customer_id', 'stripe_subscription_id'
            )
        }),
        ('Métricas', {'fields': ('calificacion_promedio', 'total_reseñas', 'activo', 'verificado')}),
        ('Timestamps', {'fields': ('fecha_creacion', 'fecha_actualizacion')}),
    )

# Admin para EmpleadoNegocio
@admin.register(EmpleadoNegocio)
class EmpleadoNegocioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'negocio', 'tipo_empleado', 'activo', 'fecha_incorporacion')
    list_filter = ('tipo_empleado', 'activo', 'negocio')
    search_fields = ('usuario__username', 'usuario__email', 'negocio__nombre')
    readonly_fields = ('fecha_incorporacion',)
    fieldsets = (
        (None, {'fields': ('usuario', 'negocio', 'tipo_empleado')}),
        ('Configuración', {
            'fields': (
                'especialidades', 'activo', 'fecha_incorporacion', 'fecha_baja',
                'puede_crear_citas', 'puede_modificar_citas', 'puede_cancelar_citas',
                'puede_gestionar_horarios', 'puede_ver_estadisticas'
            )
        }),
    )

# Admin para ServicioNegocio
@admin.register(ServicioNegocio)
class ServicioNegocioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'negocio', 'duracion_minutos', 'precio', 'activo')
    list_filter = ('negocio', 'activo', 'disponible_online', 'requiere_confirmacion')
    search_fields = ('nombre', 'negocio__nombre', 'descripcion')
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        (None, {'fields': ('negocio', 'nombre', 'descripcion')}),
        ('Configuración', {
            'fields': (
                'duracion_minutos', 'precio', 'requiere_confirmacion',
                'disponible_online', 'maximo_por_dia', 'empleados_autorizados',
                'orden', 'activo'
            )
        }),
        ('Timestamps', {'fields': ('fecha_creacion',)}),
    )

# Admin para HorarioNegocio
@admin.register(HorarioNegocio)
class HorarioNegocioAdmin(admin.ModelAdmin):
    list_display = ('negocio', 'get_dia_semana_display', 'hora_inicio', 'hora_fin', 'activo')
    list_filter = ('negocio', 'dia_semana', 'activo')
    search_fields = ('negocio__nombre',)
    fieldsets = (
        (None, {'fields': ('negocio', 'dia_semana', 'hora_inicio', 'hora_fin')}),
        ('Vigencia', {'fields': ('activo', 'fecha_inicio_vigencia', 'fecha_fin_vigencia')}),
    )

# Admin para BloqueoHorario
@admin.register(BloqueoHorario)
class BloqueoHorarioAdmin(admin.ModelAdmin):
    list_display = ('negocio', 'empleado', 'tipo_bloqueo', 'fecha_inicio', 'fecha_fin', 'activo')
    list_filter = ('negocio', 'tipo_bloqueo', 'activo')
    search_fields = ('negocio__nombre', 'motivo')
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        (None, {'fields': ('negocio', 'empleado', 'tipo_bloqueo', 'motivo')}),
        ('Período', {'fields': ('fecha_inicio', 'fecha_fin', 'activo')}),
        ('Timestamps', {'fields': ('fecha_creacion',)}),
    )

# Admin para Cita
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'negocio', 'cliente', 'servicio', 'fecha_hora_inicio', 
        'estado', 'precio_final', 'fecha_creacion'
    )
    list_filter = ('estado', 'negocio', 'servicio')
    search_fields = (
        'cliente__username', 'cliente__email', 'negocio__nombre', 
        'servicio__nombre', 'nombre_cliente'
    )
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'id')
    fieldsets = (
        (None, {'fields': ('id', 'negocio', 'cliente', 'empleado', 'servicio')}),
        ('Detalles de la Cita', {
            'fields': (
                'fecha_hora_inicio', 'fecha_hora_fin', 'estado',
                'nombre_cliente', 'telefono_cliente', 'email_cliente',
                'notas_cliente', 'notas_internas', 'precio_final'
            )
        }),
        ('Notificaciones', {'fields': ('recordatorio_enviado', 'confirmacion_enviada')}),
        ('Reprogramación', {'fields': ('cita_original',)}),
        ('Timestamps', {'fields': ('fecha_creacion', 'fecha_actualizacion', 'fecha_cancelacion')}),
    )

# Admin para ReseñaNegocio
@admin.register(ReseñaNegocio)
class ReseñaNegocioAdmin(admin.ModelAdmin):
    list_display = ('negocio', 'cliente', 'calificacion', 'activa', 'fecha_creacion')
    list_filter = ('calificacion', 'activa', 'negocio')
    search_fields = ('negocio__nombre', 'cliente__username', 'comentario')
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        (None, {'fields': ('negocio', 'cliente', 'cita')}),
        ('Calificaciones', {
            'fields': (
                'calificacion', 'calificacion_servicio', 
                'calificacion_atencion', 'calificacion_instalaciones'
            )
        }),
        ('Comentarios', {'fields': ('comentario', 'respuesta_negocio', 'fecha_respuesta')}),
        ('Estado', {'fields': ('activa', 'fecha_creacion')}),
    )

# Admin para FacturacionSuscripcion
@admin.register(FacturacionSuscripcion)
class FacturacionSuscripcionAdmin(admin.ModelAdmin):
    list_display = (
        'numero_factura', 'negocio', 'monto', 'estado_pago', 
        'periodo_inicio', 'periodo_fin', 'fecha_creacion'
    )
    list_filter = ('estado_pago', 'negocio')
    search_fields = ('numero_factura', 'negocio__nombre', 'stripe_invoice_id')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        (None, {'fields': ('negocio', 'numero_factura', 'stripe_invoice_id', 'stripe_payment_intent_id', 'stripe_subscription_id')}),
        ('Detalles', {'fields': ('monto', 'moneda', 'periodo_inicio', 'periodo_fin', 'estado_pago', 'fecha_vencimiento', 'fecha_pago')}),
        ('Información Fiscal', {'fields': ('datos_fiscales',)}),
        ('Timestamps', {'fields': ('fecha_creacion', 'fecha_actualizacion')}),
    )

# Admin para ConfiguracionPlataforma
@admin.register(ConfiguracionPlataforma)
class ConfiguracionPlataformaAdmin(admin.ModelAdmin):
    list_display = ('clave', 'tipo_dato', 'activa', 'fecha_creacion')
    list_filter = ('tipo_dato', 'activa')
    search_fields = ('clave', 'valor', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        (None, {'fields': ('clave', 'valor', 'tipo_dato')}),
        ('Detalles', {'fields': ('descripcion', 'activa')}),
        ('Timestamps', {'fields': ('fecha_creacion', 'fecha_actualizacion')}),
    )

# Registrar el modelo Usuario con su admin personalizado
admin.site.register(Usuario, UsuarioAdmin)