from django.apps import AppConfig


class OrdersReporterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders_reporter'


    def ready(self):
        import orders_reporter.signals
