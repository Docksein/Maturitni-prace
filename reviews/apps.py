from django.apps import AppConfig
import schedule

class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'

    def ready(self):
        from jobs import updater
        updater.start()
