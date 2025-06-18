from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Manufacturer
from chatbot.vector_store_utils import add_to_vector_store


@receiver(post_save, sender=Manufacturer)
def update_vector_store(sender, instance, **kwargs):
    add_to_vector_store(instance)