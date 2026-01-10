from django.apps import AppConfig

class WalkthroughreportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'walkthroughreport'

    def ready(self):
        import walkthroughreport.signals