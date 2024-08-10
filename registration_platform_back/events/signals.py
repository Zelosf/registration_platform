from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Ticket, Program


@receiver(post_save, sender=Ticket)
def update_available_tickets(sender, instance, **kwargs):
    if kwargs.get('created', False):
        program = instance.program
        if not program.can_create_ticket():
            instance.delete()
            raise ValidationError("No available tickets for the program with ID {program.id}")
