from django.apps import AppConfig

class PhoneCheckerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'phone_checker'

    def ready(self):
        #start_scheduler()
        pass

