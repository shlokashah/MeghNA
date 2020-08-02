from django.apps import AppConfig
class IsroConfig(AppConfig):
    name = 'IsroBackend'
    def ready(self):
        from BackgroundJobs import updater
        # updater.start()