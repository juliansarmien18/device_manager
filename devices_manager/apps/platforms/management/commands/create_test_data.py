"""
Management command to create test data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from apps.platforms.models import Platform, UserPlatform
from apps.devices.models import Device


class Command(BaseCommand):
    """
    Command to create test platforms, users and devices.
    """

    help = 'Crea datos de prueba: plataformas, usuarios y dispositivos'

    def handle(self, *args, **options):
        """
        Execute the command.
        """
        self.stdout.write(self.style.SUCCESS('Creando datos de prueba...'))

        platform_a, created = Platform.objects.get_or_create(
            name='Plataforma A',
            defaults={
                'description': 'Plataforma de prueba A',
                'is_active': True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Plataforma A creada (ID: {platform_a.id})'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Plataforma A ya existe (ID: {platform_a.id})'))

        platform_b, created = Platform.objects.get_or_create(
            name='Plataforma B',
            defaults={
                'description': 'Plataforma de prueba B',
                'is_active': True,
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Plataforma B creada (ID: {platform_b.id})'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Plataforma B ya existe (ID: {platform_b.id})'))

        user1, created = UserPlatform.objects.get_or_create(
            email='usuario1@example.com',
            platform=platform_a,
            defaults={
                'password': make_password('password123'),
                'is_active': True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Usuario usuario1@example.com creado en Plataforma A (ID: {user1.id})'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠ Usuario usuario1@example.com ya existe en Plataforma A (ID: {user1.id})'
                )
            )

        user1_b, created = UserPlatform.objects.get_or_create(
            email='usuario1@example.com',
            platform=platform_b,
            defaults={
                'password': make_password('password123'),
                'is_active': True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Usuario usuario1@example.com creado en Plataforma B (ID: {user1_b.id})'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠ Usuario usuario1@example.com ya existe en Plataforma B (ID: {user1_b.id})'
                )
            )

        user2, created = UserPlatform.objects.get_or_create(
            email='usuario2@example.com',
            platform=platform_a,
            defaults={
                'password': make_password('password123'),
                'is_active': True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Usuario usuario2@example.com creado en Plataforma A (ID: {user2.id})'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠ Usuario usuario2@example.com ya existe en Plataforma A (ID: {user2.id})'
                )
            )

        device1, created = Device.objects.get_or_create(
            name='Dispositivo 1',
            user_platform=user1,
            defaults={
                'ip_address': '192.168.1.1',
                'is_active': True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Dispositivo "Dispositivo 1" creado para usuario1@example.com (ID: {device1.id})'
                )
            )

        device2, created = Device.objects.get_or_create(
            name='Dispositivo 2',
            user_platform=user1,
            defaults={
                'ip_address': '192.168.1.2',
                'is_active': True,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Dispositivo "Dispositivo 2" creado para usuario1@example.com (ID: {device2.id})'
                )
            )

        device3, created = Device.objects.get_or_create(
            name='Dispositivo 3',
            user_platform=user2,
            defaults={
                'ip_address': '192.168.1.3',
                'is_active': False,
            },
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Dispositivo "Dispositivo 3" creado para usuario2@example.com (ID: {device3.id})'
                )
            )

        self.stdout.write(self.style.SUCCESS('\n✓ Datos de prueba creados exitosamente!'))
        self.stdout.write(
            self.style.SUCCESS(
                '\nPuedes usar estas credenciales para probar la API:\n'
                '- Email: usuario1@example.com\n'
                '- Password: password123\n'
                '- Platform ID: 1 (Plataforma A) o 2 (Plataforma B)\n'
            )
        )

