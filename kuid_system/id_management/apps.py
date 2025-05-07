# id_management/apps.py
from django.apps import AppConfig

class IdManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'id_management'

    def ready(self):
        import id_management.signals