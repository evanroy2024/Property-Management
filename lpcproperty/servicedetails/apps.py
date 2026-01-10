from django.apps import AppConfig

class ServicedetailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'servicedetails'

    def ready(self):
        import servicedetails.signals
