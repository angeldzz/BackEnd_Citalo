from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from API.models import CategoriaNegocio, Negocio, ServicioNegocio, HorarioNegocio
from decimal import Decimal
from datetime import time

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for testing the API'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categorias = [
            {'nombre': 'Peluquería', 'descripcion': 'Servicios de peluquería y estética', 'icono': 'fa-cut'},
            {'nombre': 'Barbería', 'descripcion': 'Servicios de barbería masculina', 'icono': 'fa-scissors'},
            {'nombre': 'Spa', 'descripcion': 'Servicios de relajación y belleza', 'icono': 'fa-spa'},
            {'nombre': 'Fisioterapia', 'descripcion': 'Servicios de fisioterapia y rehabilitación', 'icono': 'fa-heartbeat'},
            {'nombre': 'Medicina Estética', 'descripcion': 'Tratamientos de medicina estética', 'icono': 'fa-user-md'},
        ]
        
        for i, cat_data in enumerate(categorias, 1):
            categoria, created = CategoriaNegocio.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={
                    'descripcion': cat_data['descripcion'],
                    'icono': cat_data['icono'],
                    'activa': True,
                    'orden': i
                }
            )
            if created:
                self.stdout.write(f'✓ Created category: {categoria.nombre}')

        # Create sample business owner
        owner, created = User.objects.get_or_create(
            username='negocio_demo',
            defaults={
                'email': 'negocio@demo.com',
                'first_name': 'Demo',
                'last_name': 'Business',
                'tipo_usuario': 'negocio',
                'telefono': '600123456',
                'ciudad': 'Madrid',
                'provincia': 'Madrid'
            }
        )
        if created:
            owner.set_password('demo123')
            owner.save()
            self.stdout.write(f'✓ Created business owner: {owner.username}')

        # Create sample client
        client, created = User.objects.get_or_create(
            username='cliente_demo',
            defaults={
                'email': 'cliente@demo.com',
                'first_name': 'Demo',
                'last_name': 'Client',
                'tipo_usuario': 'cliente',
                'telefono': '600654321',
                'ciudad': 'Madrid',
                'provincia': 'Madrid'
            }
        )
        if created:
            client.set_password('demo123')
            client.save()
            self.stdout.write(f'✓ Created client: {client.username}')

        # Create sample business
        peluqueria_cat = CategoriaNegocio.objects.get(nombre='Peluquería')
        negocio, created = Negocio.objects.get_or_create(
            slug='peluqueria-demo',
            defaults={
                'propietario': owner,
                'categoria': peluqueria_cat,
                'nombre': 'Peluquería Demo',
                'descripcion': 'Una peluquería moderna con los mejores servicios',
                'telefono': '910123456',
                'email': 'info@peluqueriademo.com',
                'direccion': 'Calle Gran Vía 25',
                'ciudad': 'Madrid',
                'provincia': 'Madrid',
                'codigo_postal': '28013',
                'estado_suscripcion': 'activa',
                'activo': True,
                'verificado': True
            }
        )
        if created:
            self.stdout.write(f'✓ Created business: {negocio.nombre}')

        # Create services
        servicios = [
            {'nombre': 'Corte de Cabello', 'descripcion': 'Corte profesional', 'duracion': 30, 'precio': '15.00'},
            {'nombre': 'Lavado y Peinado', 'descripcion': 'Lavado y peinado completo', 'duracion': 45, 'precio': '20.00'},
            {'nombre': 'Tinte', 'descripcion': 'Tinte profesional con productos de calidad', 'duracion': 90, 'precio': '35.00'},
            {'nombre': 'Mechas', 'descripcion': 'Mechas con técnica profesional', 'duracion': 120, 'precio': '45.00'},
            {'nombre': 'Tratamiento Capilar', 'descripcion': 'Tratamiento regenerativo', 'duracion': 60, 'precio': '25.00'},
        ]
        
        for serv_data in servicios:
            servicio, created = ServicioNegocio.objects.get_or_create(
                negocio=negocio,
                nombre=serv_data['nombre'],
                defaults={
                    'descripcion': serv_data['descripcion'],
                    'duracion_minutos': serv_data['duracion'],
                    'precio': Decimal(serv_data['precio']),
                    'activo': True
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created service: {servicio.nombre}')

        # Create business hours (Monday to Saturday)
        horarios = [
            (0, time(9, 0), time(19, 0)),  # Monday
            (1, time(9, 0), time(19, 0)),  # Tuesday  
            (2, time(9, 0), time(19, 0)),  # Wednesday
            (3, time(9, 0), time(19, 0)),  # Thursday
            (4, time(9, 0), time(19, 0)),  # Friday
            (5, time(9, 0), time(15, 0)),  # Saturday
        ]
        
        for dia, inicio, fin in horarios:
            horario, created = HorarioNegocio.objects.get_or_create(
                negocio=negocio,
                dia_semana=dia,
                defaults={
                    'hora_inicio': inicio,
                    'hora_fin': fin,
                    'activo': True
                }
            )
            if created:
                dia_nombre = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'][dia]
                self.stdout.write(f'  ✓ Created schedule: {dia_nombre} {inicio}-{fin}')

        self.stdout.write(
            self.style.SUCCESS(
                '\n✨ Sample data created successfully!\n\n'
                'You can now test the API with:\n'
                '- Business owner: negocio_demo / demo123\n'
                '- Client: cliente_demo / demo123\n\n'
                'Visit http://localhost:8000/api/docs/ to explore the API documentation.'
            )
        )