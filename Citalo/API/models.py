from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
import uuid


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que extiende AbstractUser
    Maneja tanto clientes como propietarios de negocios
    
    CAMPOS HEREDADOS DE AbstractUser:
    - username: nombre de usuario único
    - email: correo electrónico 
    - first_name: nombre
    - last_name: apellidos
    - password: contraseña (hasheada)
    - is_active: activo (por defecto True)
    - is_staff: es staff
    - is_superuser: es superusuario
    - date_joined: fecha de registro
    - last_login: último login
    """
    TIPO_USUARIO_CHOICES = [
        ('cliente', 'Cliente'),
        ('negocio', 'Propietario de Negocio'),
        ('empleado', 'Empleado'),
        ('admin', 'Administrador'),
    ]
    
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('N', 'Prefiero no decirlo'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Override inherited fields to fix reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usuarios',
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuarios',
        related_query_name='usuario',
    )
    
    # Información personal adicional
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='cliente')
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    
    # Información de contacto
    telefono = models.CharField(max_length=20, blank=True, help_text="Teléfono principal")
    telefono_alternativo = models.CharField(max_length=20, blank=True)
    
    # Dirección personal
    direccion = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    provincia = models.CharField(max_length=100, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    pais = models.CharField(max_length=100, default='España')
    
    # Avatar y preferencias
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    biografia = models.TextField(blank=True, max_length=500, help_text="Descripción personal breve")
    
    # Configuración de notificaciones
    notificaciones_email = models.BooleanField(default=True)
    notificaciones_sms = models.BooleanField(default=False)
    notificaciones_push = models.BooleanField(default=True)
    
    # Preferencias de idioma y zona horaria
    idioma_preferido = models.CharField(max_length=10, default='es', help_text="Código de idioma (es, en, etc.)")
    zona_horaria = models.CharField(max_length=50, default='Europe/Madrid')
    
    # Control de estado y verificación
    email_verificado = models.BooleanField(default=False)
    telefono_verificado = models.BooleanField(default=False)
    
    # Timestamps personalizados
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    ultima_actividad = models.DateTimeField(blank=True, null=True)
    
    
    # Configuración adicional del modelo
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'usuarios'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['tipo_usuario']),
            models.Index(fields=['telefono']),
            models.Index(fields=['ciudad', 'provincia']),
        ]

    def __str__(self):
        nombre_completo = self.get_nombre_completo()
        return f"{nombre_completo or self.username} ({self.get_tipo_usuario_display()})"

    def get_nombre_completo(self):
        """
        Devuelve el nombre completo del usuario
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return ""

    def get_iniciales(self):
        """
        Devuelve las iniciales del usuario (útil para avatars)
        """
        nombre = self.first_name[:1].upper() if self.first_name else ''
        apellido = self.last_name[:1].upper() if self.last_name else ''
        return f"{nombre}{apellido}" or self.username[:2].upper()

    @property
    def nombre_completo(self):
        """Property para acceso rápido al nombre completo"""
        return self.get_nombre_completo()

    @property
    def es_propietario_negocio(self):
        """Verifica si el usuario es propietario de algún negocio"""
        return self.tipo_usuario == 'negocio' and self.negocios_propios.filter(activo=True).exists()

    @property
    def tiene_perfil_completo(self):
        """Verifica si el usuario tiene su perfil completo"""
        campos_requeridos = [
            self.first_name, self.last_name, self.email, 
            self.telefono, self.fecha_nacimiento
        ]
        return all(campo for campo in campos_requeridos)

    def save(self, *args, **kwargs):
        # Normalizar email a minúsculas
        if self.email:
            self.email = self.email.lower()
        
        # Actualizar última actividad si el usuario está haciendo login
        if self.pk and self.last_login != Usuario.objects.filter(pk=self.pk).values_list('last_login', flat=True).first():
            self.ultima_actividad = timezone.now()
            
        super().save(*args, **kwargs)


class CategoriaNegocio(models.Model):
    """
    Categorías de negocios que pueden usar la plataforma
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=50, blank=True, help_text="Clase CSS o nombre del icono")
    activa = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0, help_text="Orden de visualización")
    
    # Configuraciones específicas por categoría
    duracion_cita_default = models.PositiveIntegerField(
        default=30, 
        help_text="Duración por defecto de las citas en minutos"
    )
    permite_citas_online = models.BooleanField(default=True)
    requiere_confirmacion = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Categoría de Negocio'
        verbose_name_plural = 'Categorías de Negocio'
        db_table = 'categorias_negocio'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class Negocio(models.Model):
    """
    Modelo principal para los negocios que se suscriben a la plataforma
    """
    ESTADO_SUSCRIPCION_CHOICES = [
        ('activa', 'Activa'),
        ('pendiente_pago', 'Pendiente de Pago'),
        ('suspendida', 'Suspendida'),
        ('cancelada', 'Cancelada'),
        ('prueba', 'Período de Prueba'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    propietario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='negocios_propios',
        limit_choices_to={'tipo_usuario': 'negocio'}
    )
    categoria = models.ForeignKey(CategoriaNegocio, on_delete=models.PROTECT, related_name='negocios')
    
    # Información básica
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, unique=True, help_text="URL amigable para el negocio")
    
    # Datos de contacto
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    sitio_web = models.URLField(blank=True)
    
    # Ubicación
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitud = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    
    # Imágenes y multimedia
    logo = models.ImageField(upload_to='negocios/logos/', blank=True, null=True)
    imagen_portada = models.ImageField(upload_to='negocios/portadas/', blank=True, null=True)
    
    # Configuración del negocio
    zona_horaria = models.CharField(max_length=50, default='Europe/Madrid')
    tiempo_anticipacion_minimo = models.PositiveIntegerField(
        default=60, 
        help_text="Tiempo mínimo de anticipación para reservar cita (minutos)"
    )
    tiempo_cancelacion_limite = models.PositiveIntegerField(
        default=120,
        help_text="Tiempo límite para cancelar una cita sin penalización (minutos)"
    )
    permite_reservas_multiples = models.BooleanField(default=False)
    
    # Estado y suscripción
    estado_suscripcion = models.CharField(
        max_length=20, 
        choices=ESTADO_SUSCRIPCION_CHOICES, 
        default='pendiente_pago'
    )
    fecha_inicio_suscripcion = models.DateTimeField(blank=True, null=True)
    fecha_fin_suscripcion = models.DateTimeField(blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Métricas y configuración
    calificacion_promedio = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reseñas = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    verificado = models.BooleanField(default=False)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Negocio'
        verbose_name_plural = 'Negocios'
        db_table = 'negocios'
        indexes = [
            models.Index(fields=['ciudad', 'categoria']),
            models.Index(fields=['estado_suscripcion']),
            models.Index(fields=['activo', 'verificado']),
        ]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            base_slug = slugify(self.nombre)
            unique_slug = base_slug
            counter = 1
            while Negocio.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    @property
    def suscripcion_activa(self):
        return (
            self.estado_suscripcion == 'activa' and 
            self.fecha_fin_suscripcion and 
            timezone.now() <= self.fecha_fin_suscripcion
        )


class EmpleadoNegocio(models.Model):
    """
    Empleados que pueden gestionar citas en nombre del negocio
    """
    TIPO_EMPLEADO_CHOICES = [
        ('administrador', 'Administrador'),
        ('empleado', 'Empleado Regular'),
        ('consultor', 'Consultor/Freelancer'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='empleos')
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, related_name='empleados')
    tipo_empleado = models.CharField(max_length=20, choices=TIPO_EMPLEADO_CHOICES, default='empleado')
    
    # Especialidades y servicios que puede ofrecer
    especialidades = models.TextField(blank=True, help_text="Especialidades del empleado separadas por comas")
    
    # Configuración de disponibilidad
    activo = models.BooleanField(default=True)
    fecha_incorporacion = models.DateField(auto_now_add=True)
    fecha_baja = models.DateField(blank=True, null=True)
    
    # Permisos
    puede_crear_citas = models.BooleanField(default=True)
    puede_modificar_citas = models.BooleanField(default=True)
    puede_cancelar_citas = models.BooleanField(default=True)
    puede_gestionar_horarios = models.BooleanField(default=False)
    puede_ver_estadisticas = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Empleado de Negocio'
        verbose_name_plural = 'Empleados de Negocio'
        db_table = 'empleados_negocio'
        unique_together = ['usuario', 'negocio']

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.negocio.nombre}"


class ServicioNegocio(models.Model):
    """
    Servicios que ofrece cada negocio
    """
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, related_name='servicios')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    
    # Duración y precio
    duracion_minutos = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Configuración del servicio
    requiere_confirmacion = models.BooleanField(default=False)
    disponible_online = models.BooleanField(default=True)
    maximo_por_dia = models.PositiveIntegerField(blank=True, null=True, help_text="Límite máximo de este servicio por día")
    
    # Empleados que pueden realizar este servicio
    empleados_autorizados = models.ManyToManyField(
        EmpleadoNegocio, 
        blank=True, 
        related_name='servicios_autorizados',
        help_text="Si está vacío, todos los empleados pueden realizar este servicio"
    )
    
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Servicio de Negocio'
        verbose_name_plural = 'Servicios de Negocio'
        db_table = 'servicios_negocio'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return f"{self.negocio.nombre} - {self.nombre}"


class HorarioNegocio(models.Model):
    """
    Horarios de funcionamiento del negocio por día de la semana
    """
    DIAS_SEMANA = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activo = models.BooleanField(default=True)
    
    # Para horarios especiales (ej: horarios de verano)
    fecha_inicio_vigencia = models.DateField(blank=True, null=True)
    fecha_fin_vigencia = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Horario de Negocio'
        verbose_name_plural = 'Horarios de Negocio'
        db_table = 'horarios_negocio'
        unique_together = ['negocio', 'dia_semana', 'fecha_inicio_vigencia']

    def __str__(self):
        return f"{self.negocio.nombre} - {self.get_dia_semana_display()}: {self.hora_inicio}-{self.hora_fin}"


class BloqueoHorario(models.Model):
    """
    Bloqueos específicos de horarios (vacaciones, días festivos, etc.)
    """
    TIPO_BLOQUEO_CHOICES = [
        ('vacaciones', 'Vacaciones'),
        ('festivo', 'Día Festivo'),
        ('mantenimiento', 'Mantenimiento'),
        ('personal', 'Motivos Personales'),
        ('otro', 'Otro'),
    ]
    
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, related_name='bloqueos')
    empleado = models.ForeignKey(
        EmpleadoNegocio, 
        on_delete=models.CASCADE, 
        related_name='bloqueos',
        blank=True, null=True,
        help_text="Si se especifica, el bloqueo aplica solo a este empleado"
    )
    
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    tipo_bloqueo = models.CharField(max_length=20, choices=TIPO_BLOQUEO_CHOICES, default='otro')
    motivo = models.TextField(blank=True)
    
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Bloqueo de Horario'
        verbose_name_plural = 'Bloqueos de Horario'
        db_table = 'bloqueos_horario'

    def __str__(self):
        empleado_info = f" - {self.empleado}" if self.empleado else ""
        return f"{self.negocio.nombre}{empleado_info}: {self.get_tipo_bloqueo_display()}"


class Cita(models.Model):
    """
    Modelo principal para las citas
    """
    ESTADO_CITA_CHOICES = [
        ('pendiente', 'Pendiente de Confirmación'),
        ('confirmada', 'Confirmada'),
        ('en_curso', 'En Curso'),
        ('completada', 'Completada'),
        ('cancelada_cliente', 'Cancelada por Cliente'),
        ('cancelada_negocio', 'Cancelada por Negocio'),
        ('no_asistio', 'No Asistió'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, related_name='citas')
    cliente = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='citas_cliente',
        limit_choices_to={'tipo_usuario': 'cliente'}
    )
    empleado = models.ForeignKey(
        EmpleadoNegocio, 
        on_delete=models.SET_NULL, 
        related_name='citas_asignadas',
        blank=True, null=True
    )
    servicio = models.ForeignKey(ServicioNegocio, on_delete=models.PROTECT, related_name='citas')
    
    # Información de la cita
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADO_CITA_CHOICES, default='pendiente')
    
    # Información del cliente para la cita
    nombre_cliente = models.CharField(max_length=200, help_text="Nombre completo del cliente para la cita")
    telefono_cliente = models.CharField(max_length=20)
    email_cliente = models.EmailField()
    
    # Notas y observaciones
    notas_cliente = models.TextField(blank=True, help_text="Notas adicionales del cliente")
    notas_internas = models.TextField(blank=True, help_text="Notas internas del negocio")
    
    # Precio final (puede diferir del precio base del servicio)
    precio_final = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    # Control de cambios y comunicaciones
    recordatorio_enviado = models.BooleanField(default=False)
    confirmacion_enviada = models.BooleanField(default=False)
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_cancelacion = models.DateTimeField(blank=True, null=True)
    
    # Para reprogramaciones
    cita_original = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        blank=True, null=True,
        related_name='reprogramaciones'
    )
    
    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        db_table = 'citas'
        indexes = [
            models.Index(fields=['fecha_hora_inicio', 'estado']),
            models.Index(fields=['negocio', 'fecha_hora_inicio']),
            models.Index(fields=['cliente', 'estado']),
        ]

    def __str__(self):
        return f"Cita {self.id} - {self.cliente.get_full_name()} - {self.servicio.nombre}"

    def save(self, *args, **kwargs):
        # Calcular fecha_hora_fin automáticamente
        if not self.fecha_hora_fin and self.servicio:
            from datetime import timedelta
            self.fecha_hora_fin = self.fecha_hora_inicio + timedelta(minutes=self.servicio.duracion_minutos)
        
        # Establecer precio final si no está definido
        if not self.precio_final and self.servicio:
            self.precio_final = self.servicio.precio
            
        super().save(*args, **kwargs)


class ReseñaNegocio(models.Model):
    """
    Reseñas y calificaciones de los negocios
    """
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, related_name='reseñas')
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reseñas_escritas')
    cita = models.OneToOneField(
        Cita, 
        on_delete=models.CASCADE, 
        related_name='reseña',
        blank=True, null=True
    )
    
    calificacion = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True)
    
    # Aspectos específicos (opcional)
    calificacion_servicio = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        blank=True, null=True
    )
    calificacion_atencion = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        blank=True, null=True
    )
    calificacion_instalaciones = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        blank=True, null=True
    )
    
    # Respuesta del negocio
    respuesta_negocio = models.TextField(blank=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Reseña de Negocio'
        verbose_name_plural = 'Reseñas de Negocio'
        db_table = 'reseñas_negocio'
        unique_together = ['negocio', 'cliente', 'cita']

    def __str__(self):
        return f"Reseña de {self.cliente.get_full_name()} para {self.negocio.nombre} - {self.calificacion}⭐"


class FacturacionSuscripcion(models.Model):
    """
    Registro de facturación y pagos de suscripciones
    """
    ESTADO_PAGO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('fallido', 'Fallido'),
        ('reembolsado', 'Reembolsado'),
        ('cancelado', 'Cancelado'),
    ]
    
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, related_name='facturas')
    
    # Información de Stripe
    stripe_invoice_id = models.CharField(max_length=100, unique=True)
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True)
    stripe_subscription_id = models.CharField(max_length=100)
    
    # Detalles de la factura
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3, default='EUR')
    periodo_inicio = models.DateField()
    periodo_fin = models.DateField()
    
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES, default='pendiente')
    fecha_vencimiento = models.DateTimeField()
    fecha_pago = models.DateTimeField(blank=True, null=True)
    
    # Información fiscal
    numero_factura = models.CharField(max_length=100, unique=True, blank=True)
    datos_fiscales = models.JSONField(default=dict, blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Facturación de Suscripción'
        verbose_name_plural = 'Facturaciones de Suscripción'
        db_table = 'facturacion_suscripcion'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Factura {self.numero_factura or self.id} - {self.negocio.nombre}"


class ConfiguracionPlataforma(models.Model):
    """
    Configuraciones globales de la plataforma
    """
    clave = models.CharField(max_length=100, unique=True)
    valor = models.TextField()
    descripcion = models.TextField(blank=True)
    tipo_dato = models.CharField(
        max_length=20, 
        choices=[
            ('string', 'Texto'),
            ('integer', 'Entero'),
            ('float', 'Decimal'),
            ('boolean', 'Booleano'),
            ('json', 'JSON'),
        ],
        default='string'
    )
    
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuración de Plataforma'
        verbose_name_plural = 'Configuraciones de Plataforma'
        db_table = 'configuracion_plataforma'

    def __str__(self):
        return f"{self.clave}: {self.valor[:50]}..."

    def get_valor(self):
        """Convierte el valor según su tipo de dato"""
        if self.tipo_dato == 'integer':
            return int(self.valor)
        elif self.tipo_dato == 'float':
            return float(self.valor)
        elif self.tipo_dato == 'boolean':
            return self.valor.lower() in ['true', '1', 'yes', 'on']
        elif self.tipo_dato == 'json':
            import json
            return json.loads(self.valor)
        return self.valor