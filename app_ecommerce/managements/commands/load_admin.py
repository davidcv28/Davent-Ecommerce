from django.contrib.auth.models import User
from django.core.management import BaseCommand


"""

En este modulo, vamos a crear el usuario administrador por defecto del sistema.

"""

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.WARNING('CARGANDO CUENTA ADMINISTRADORA'))
            User.objects.create_superuser(
                first_name = 'Admin',
                last_name = 'Davent',
                email = 'admin_daven@hotmail.com',
                username = 'admin',
                password = 'admin1234',
            )
            self.stdout.write(self.style.SUCCESS('CUENTA DE ADMINISTRADOR CARGADA'))
        except:
            return
        
            
