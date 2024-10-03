# blog/apps.py

from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        # Se não houver sinais, comente ou remova a linha abaixo
        # import blog.signals
        pass  # Remova essa linha se não for usar sinais
