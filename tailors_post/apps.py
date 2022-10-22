from django.apps import AppConfig


class TailorsPostConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tailors_post'
    def ready(self):
        import tailors_post.signals
