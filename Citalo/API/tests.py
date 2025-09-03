from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta, time
from decimal import Decimal

from .models import (
    Usuario, CategoriaNegocio, Negocio, EmpleadoNegocio, 
    ServicioNegocio, HorarioNegocio, BloqueoHorario, Cita,
    ReseñaNegocio, FacturacionSuscripcion, ConfiguracionPlataforma
)

User = get_user_model()


class BaseAPITestCase(APITestCase):
    """Clase base para tests de API con configuración común"""
    
    def setUp(self):
        self.client = APIClient()
        
        # Crear usuarios de prueba
        self.cliente_user = User.objects.create_user(
            username='cliente_test',
            email='cliente@test.com',
            password='testpass123',
            first_name='Cliente',
            last_name='Test',
            tipo_usuario='cliente',
            telefono='123456789'
        )
        
        self.negocio_user = User.objects.create_user(
            username='negocio_test',
            email='negocio@test.com',
            password='testpass123',
            first_name='Negocio',
            last_name='Test',
            tipo_usuario='negocio',
            telefono='987654321'
        )
        
        # Crear categoría de negocio
        self.categoria = CategoriaNegocio.objects.create(
            nombre='Peluquería',
            descripcion='Servicios de peluquería y estética',
            icono='fa-cut',
            activa=True,
            orden=1
        )
        
        # Crear negocio
        self.negocio = Negocio.objects.create(
            propietario=self.negocio_user,
            categoria=self.categoria,
            nombre='Peluquería Test',
            descripcion='Una peluquería de prueba',
            slug='peluqueria-test',
            telefono='123456789',
            email='peluqueria@test.com',
            direccion='Calle Test 123',
            ciudad='Madrid',
            provincia='Madrid',
            codigo_postal='28001'
        )
        
        # Crear tokens de autenticación
        self.cliente_token = Token.objects.create(user=self.cliente_user)
        self.negocio_token = Token.objects.create(user=self.negocio_user)

    def authenticate_as_cliente(self):
        """Autenticar como cliente"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.cliente_token.key}')

    def authenticate_as_negocio(self):
        """Autenticar como negocio"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.negocio_token.key}')

    def unauthenticate(self):
        """Remover autenticación"""
        self.client.credentials()


class AuthenticationTestCase(BaseAPITestCase):
    """Tests para autenticación"""
    
    def test_login_exitoso(self):
        """Test login exitoso"""
        url = reverse('api:login')
        data = {
            'username': 'cliente_test',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(response.data['username'], 'cliente_test')

    def test_login_credenciales_invalidas(self):
        """Test login con credenciales inválidas"""
        url = reverse('api:login')
        data = {
            'username': 'cliente_test',
            'password': 'password_incorrecto'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_exitoso(self):
        """Test logout exitoso"""
        self.authenticate_as_cliente()
        url = reverse('api:logout')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el token fue eliminado
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(user=self.cliente_user)


class UsuarioAPITestCase(BaseAPITestCase):
    """Tests para la API de usuarios"""
    
    def test_registro_usuario(self):
        """Test registro de nuevo usuario"""
        url = reverse('api:usuario-list')
        data = {
            'username': 'nuevo_usuario',
            'email': 'nuevo@test.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'tipo_usuario': 'cliente',
            'telefono': '555123456'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='nuevo_usuario').exists())

    def test_registro_contraseñas_no_coinciden(self):
        """Test registro con contraseñas que no coinciden"""
        url = reverse('api:usuario-list')
        data = {
            'username': 'nuevo_usuario',
            'email': 'nuevo@test.com',
            'password': 'testpass123',
            'password_confirm': 'testpass456',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'tipo_usuario': 'cliente'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtener_perfil_propio(self):
        """Test obtener perfil del usuario actual"""
        self.authenticate_as_cliente()
        url = reverse('api:usuario-me')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'cliente_test')

    def test_actualizar_perfil_propio(self):
        """Test actualizar perfil del usuario actual"""
        self.authenticate_as_cliente()
        url = reverse('api:usuario-me')
        data = {
            'first_name': 'Cliente Actualizado',
            'biografia': 'Nueva biografía'
        }
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Cliente Actualizado')

    def test_cambiar_contraseña(self):
        """Test cambiar contraseña"""
        self.authenticate_as_cliente()
        url = reverse('api:usuario-change-password', kwargs={'pk': self.cliente_user.pk})
        data = {
            'old_password': 'testpass123',
            'new_password': 'nuevapass123'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que la contraseña cambió
        self.cliente_user.refresh_from_db()
        self.assertTrue(self.cliente_user.check_password('nuevapass123'))


class CategoriaNegocioAPITestCase(BaseAPITestCase):
    """Tests para la API de categorías de negocio"""
    
    def test_listar_categorias(self):
        """Test listar categorías (sin autenticación)"""
        url = reverse('api:categoria-negocio-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nombre'], 'Peluquería')

    def test_obtener_categoria_detalle(self):
        """Test obtener detalle de categoría"""
        url = reverse('api:categoria-negocio-detail', kwargs={'pk': self.categoria.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Peluquería')


class NegocioAPITestCase(BaseAPITestCase):
    """Tests para la API de negocios"""
    
    def test_listar_negocios(self):
        """Test listar negocios (sin autenticación)"""
        url = reverse('api:negocio-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_crear_negocio(self):
        """Test crear negocio"""
        self.authenticate_as_negocio()
        url = reverse('api:negocio-list')
        data = {
            'categoria': self.categoria.pk,
            'nombre': 'Nuevo Negocio',
            'descripcion': 'Descripción del nuevo negocio',
            'telefono': '987654321',
            'email': 'nuevo@negocio.com',
            'direccion': 'Nueva dirección',
            'ciudad': 'Barcelona',
            'provincia': 'Barcelona'
        }
        response = self.client.post(url, data)
        
        # Debug: print response if error
        if response.status_code != status.HTTP_201_CREATED:
            print("Response status:", response.status_code)
            print("Response data:", response.data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['propietario'], self.negocio_user.pk)

    def test_obtener_estadisticas_negocio(self):
        """Test obtener estadísticas del negocio"""
        self.authenticate_as_negocio()
        url = reverse('api:negocio-estadisticas', kwargs={'pk': self.negocio.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_citas', response.data)
        self.assertIn('ingresos_mes_actual', response.data)

    def test_consultar_disponibilidad(self):
        """Test consultar disponibilidad de horarios"""
        # Crear horario para el negocio
        HorarioNegocio.objects.create(
            negocio=self.negocio,
            dia_semana=1,  # Martes
            hora_inicio=time(9, 0),
            hora_fin=time(18, 0),
            activo=True
        )
        
        # Obtener un martes futuro
        hoy = timezone.now().date()
        dias_hasta_martes = (1 - hoy.weekday()) % 7
        if dias_hasta_martes == 0:
            dias_hasta_martes = 7
        martes_futuro = hoy + timedelta(days=dias_hasta_martes)
        
        url = reverse('api:negocio-disponibilidad', kwargs={'pk': self.negocio.pk})
        response = self.client.get(url, {'fecha': martes_futuro.strftime('%Y-%m-%d')})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('horarios_disponibles', response.data)


class ServicioNegocioAPITestCase(BaseAPITestCase):
    """Tests para la API de servicios de negocio"""
    
    def setUp(self):
        super().setUp()
        self.servicio = ServicioNegocio.objects.create(
            negocio=self.negocio,
            nombre='Corte de Cabello',
            descripcion='Corte de cabello profesional',
            duracion_minutos=30,
            precio=Decimal('15.00'),
            activo=True
        )

    def test_listar_servicios_por_negocio(self):
        """Test listar servicios de un negocio específico"""
        url = reverse('api:servicio-negocio-list')
        response = self.client.get(url, {'negocio': self.negocio.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_crear_servicio(self):
        """Test crear servicio"""
        self.authenticate_as_negocio()
        url = reverse('api:servicio-negocio-list')
        data = {
            'negocio': self.negocio.pk,
            'nombre': 'Tinte',
            'descripcion': 'Tinte profesional',
            'duracion_minutos': 60,
            'precio': '25.00',
            'activo': True
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], 'Tinte')


class CitaAPITestCase(BaseAPITestCase):
    """Tests para la API de citas"""
    
    def setUp(self):
        super().setUp()
        self.servicio = ServicioNegocio.objects.create(
            negocio=self.negocio,
            nombre='Corte de Cabello',
            descripcion='Corte de cabello profesional',
            duracion_minutos=30,
            precio=Decimal('15.00'),
            activo=True
        )
        
        self.empleado = EmpleadoNegocio.objects.create(
            usuario=self.negocio_user,
            negocio=self.negocio,
            tipo_empleado='administrador',
            activo=True
        )

    def test_crear_cita(self):
        """Test crear cita"""
        self.authenticate_as_cliente()
        url = reverse('api:cita-list')
        fecha_futura = timezone.now() + timedelta(days=1)
        
        data = {
            'negocio': self.negocio.pk,
            'empleado': self.empleado.pk,
            'servicio': self.servicio.pk,
            'fecha_hora_inicio': fecha_futura.isoformat(),
            'nombre_cliente': 'Cliente Test',
            'telefono_cliente': '123456789',
            'email_cliente': 'cliente@test.com'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_crear_cita_fecha_pasada(self):
        """Test crear cita con fecha en el pasado (debe fallar)"""
        self.authenticate_as_cliente()
        url = reverse('api:cita-list')
        fecha_pasada = timezone.now() - timedelta(days=1)
        
        data = {
            'negocio': self.negocio.pk,
            'servicio': self.servicio.pk,
            'fecha_hora_inicio': fecha_pasada.isoformat(),
            'nombre_cliente': 'Cliente Test',
            'telefono_cliente': '123456789',
            'email_cliente': 'cliente@test.com'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listar_citas_cliente(self):
        """Test listar citas de un cliente"""
        # Crear cita
        cita = Cita.objects.create(
            negocio=self.negocio,
            cliente=self.cliente_user,
            servicio=self.servicio,
            fecha_hora_inicio=timezone.now() + timedelta(days=1),
            nombre_cliente='Cliente Test',
            telefono_cliente='123456789',
            email_cliente='cliente@test.com'
        )
        
        self.authenticate_as_cliente()
        url = reverse('api:cita-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_cambiar_estado_cita(self):
        """Test cambiar estado de cita"""
        # Crear cita
        cita = Cita.objects.create(
            negocio=self.negocio,
            cliente=self.cliente_user,
            servicio=self.servicio,
            fecha_hora_inicio=timezone.now() + timedelta(days=1),
            nombre_cliente='Cliente Test',
            telefono_cliente='123456789',
            email_cliente='cliente@test.com'
        )
        
        self.authenticate_as_negocio()
        url = reverse('api:cita-cambiar-estado', kwargs={'pk': cita.pk})
        data = {'estado': 'confirmada'}
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cita.refresh_from_db()
        self.assertEqual(cita.estado, 'confirmada')


class ReseñaAPITestCase(BaseAPITestCase):
    """Tests para la API de reseñas"""
    
    def setUp(self):
        super().setUp()
        self.servicio = ServicioNegocio.objects.create(
            negocio=self.negocio,
            nombre='Corte de Cabello',
            duracion_minutos=30,
            precio=Decimal('15.00'),
            activo=True
        )
        
        self.cita = Cita.objects.create(
            negocio=self.negocio,
            cliente=self.cliente_user,
            servicio=self.servicio,
            fecha_hora_inicio=timezone.now() - timedelta(days=1),
            nombre_cliente='Cliente Test',
            telefono_cliente='123456789',
            email_cliente='cliente@test.com',
            estado='completada'
        )

    def test_crear_reseña(self):
        """Test crear reseña"""
        self.authenticate_as_cliente()
        url = reverse('api:reseña-list')
        data = {
            'negocio': self.negocio.pk,
            'cita': self.cita.pk,
            'calificacion': 5,
            'comentario': 'Excelente servicio',
            'calificacion_servicio': 5,
            'calificacion_atencion': 5
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['calificacion'], 5)

    def test_listar_reseñas_negocio(self):
        """Test listar reseñas de un negocio"""
        # Crear reseña
        ReseñaNegocio.objects.create(
            negocio=self.negocio,
            cliente=self.cliente_user,
            cita=self.cita,
            calificacion=4,
            comentario='Buen servicio'
        )
        
        url = reverse('api:reseña-list')
        response = self.client.get(url, {'negocio': self.negocio.pk})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class ModelTestCase(TestCase):
    """Tests para los modelos"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.categoria = CategoriaNegocio.objects.create(
            nombre='Test Category',
            activa=True
        )
        
        self.negocio = Negocio.objects.create(
            propietario=self.user,
            categoria=self.categoria,
            nombre='Test Business',
            telefono='123456789',
            email='business@test.com',
            direccion='Test Address',
            ciudad='Test City'
        )

    def test_usuario_str(self):
        """Test string representation de Usuario"""
        expected = f"Test User (Cliente)"
        self.assertEqual(str(self.user), expected)

    def test_usuario_nombre_completo(self):
        """Test método get_nombre_completo"""
        self.assertEqual(self.user.get_nombre_completo(), "Test User")

    def test_usuario_iniciales(self):
        """Test método get_iniciales"""
        self.assertEqual(self.user.get_iniciales(), "TU")

    def test_negocio_str(self):
        """Test string representation de Negocio"""
        self.assertEqual(str(self.negocio), "Test Business")

    def test_categoria_negocio_str(self):
        """Test string representation de CategoriaNegocio"""
        self.assertEqual(str(self.categoria), "Test Category")

    def test_cita_save_method(self):
        """Test método save de Cita que calcula fecha_hora_fin automáticamente"""
        servicio = ServicioNegocio.objects.create(
            negocio=self.negocio,
            nombre='Test Service',
            duracion_minutos=30,
            precio=Decimal('20.00')
        )
        
        fecha_inicio = timezone.now() + timedelta(days=1)
        cita = Cita.objects.create(
            negocio=self.negocio,
            cliente=self.user,
            servicio=servicio,
            fecha_hora_inicio=fecha_inicio,
            nombre_cliente='Test Client',
            telefono_cliente='123456789',
            email_cliente='client@test.com'
        )
        
        expected_fin = fecha_inicio + timedelta(minutes=30)
        self.assertEqual(cita.fecha_hora_fin, expected_fin)
        self.assertEqual(cita.precio_final, servicio.precio)


class IntegrationTestCase(BaseAPITestCase):
    """Tests de integración para flujos completos"""
    
    def test_flujo_completo_reserva_cita(self):
        """Test del flujo completo de reserva de cita"""
        
        # 1. Registro de cliente
        url = reverse('api:usuario-list')
        data = {
            'username': 'cliente_nuevo',
            'email': 'cliente_nuevo@test.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Cliente',
            'last_name': 'Nuevo',
            'tipo_usuario': 'cliente',
            'telefono': '555123456'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 2. Login del cliente
        login_url = reverse('api:login')
        login_data = {
            'username': 'cliente_nuevo',
            'password': 'testpass123'
        }
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['token']
        
        # 3. Autenticar cliente
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        
        # 4. Listar negocios disponibles
        negocios_url = reverse('api:negocio-list')
        response = self.client.get(negocios_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)
        
        # 5. Ver servicios del negocio
        servicios_url = reverse('api:servicio-negocio-list')
        servicio = ServicioNegocio.objects.create(
            negocio=self.negocio,
            nombre='Corte Premium',
            duracion_minutos=45,
            precio=Decimal('25.00'),
            activo=True
        )
        response = self.client.get(servicios_url, {'negocio': self.negocio.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 6. Consultar disponibilidad
        # Crear horario
        HorarioNegocio.objects.create(
            negocio=self.negocio,
            dia_semana=1,  # Martes
            hora_inicio=time(9, 0),
            hora_fin=time(18, 0),
            activo=True
        )
        
        hoy = timezone.now().date()
        dias_hasta_martes = (1 - hoy.weekday()) % 7
        if dias_hasta_martes == 0:
            dias_hasta_martes = 7
        martes_futuro = hoy + timedelta(days=dias_hasta_martes)
        
        disponibilidad_url = reverse('api:negocio-disponibilidad', kwargs={'pk': self.negocio.pk})
        response = self.client.get(disponibilidad_url, {'fecha': martes_futuro.strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 7. Crear cita
        citas_url = reverse('api:cita-list')
        fecha_cita = timezone.make_aware(datetime.combine(martes_futuro, time(10, 0)))
        cita_data = {
            'negocio': self.negocio.pk,
            'servicio': servicio.pk,
            'fecha_hora_inicio': fecha_cita.isoformat(),
            'nombre_cliente': 'Cliente Nuevo',
            'telefono_cliente': '555123456',
            'email_cliente': 'cliente_nuevo@test.com'
        }
        response = self.client.post(citas_url, cita_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cita_id = response.data['id']
        
        # 8. Ver citas del cliente
        response = self.client.get(citas_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # 9. El negocio confirma la cita
        self.authenticate_as_negocio()
        cambiar_estado_url = reverse('api:cita-cambiar-estado', kwargs={'pk': cita_id})
        response = self.client.patch(cambiar_estado_url, {'estado': 'confirmada'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 10. Después del servicio, el cliente deja una reseña
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        # Primero marcar la cita como completada
        self.authenticate_as_negocio()
        response = self.client.patch(cambiar_estado_url, {'estado': 'completada'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ahora el cliente puede dejar reseña
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        reseñas_url = reverse('api:reseña-list')
        reseña_data = {
            'negocio': self.negocio.pk,
            'calificacion': 5,
            'comentario': 'Excelente servicio, muy profesional'
        }
        response = self.client.post(reseñas_url, reseña_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
