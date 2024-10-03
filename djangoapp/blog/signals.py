# blog/signals.py

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Post

@receiver(post_save, sender=Post)
def create_post(sender, instance, created, **kwargs):
    """Sinal acionado após um Post ser salvo."""
    if created:
        # Ação a ser executada quando um novo Post é criado
        print(f'Novo Post criado: {instance.title}')

@receiver(post_save, sender=Post)
def save_post(sender, instance, **kwargs):
    """Sinal acionado sempre que um Post é salvo."""
    print(f'Post salvo: {instance.title}')

@receiver(pre_delete, sender=Post)
def post_deleted(sender, instance, **kwargs):
    """Sinal acionado antes de um Post ser excluído."""
    print(f'Post a ser excluído: {instance.title}')
