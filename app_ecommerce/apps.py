from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AppEcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_ecommerce'

    def ready(self):
        import app_ecommerce.signals
        post_migrate.connect(self.load_data)
    def load_data(self, sender, **kwargs):
        from django.core.management import call_command
        try:
            call_command('load_admin')
            call_command('load_products')
        except Exception as e:
            print(f'Algo salio mal : {e}')