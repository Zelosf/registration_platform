from django.db import models
from django.core.exceptions import ValidationError
import uuid
from user.models import CustomUser


class Event(models.Model):
    EVENT_TYPES = (
        ('conference', 'Конференція'),
        ('seminar', 'Семінар'),
        ('workshop', 'Воркшоп'),
    )

    name = models.CharField(max_length=255)
    event_type = models.CharField(choices=EVENT_TYPES, max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.name


class Speaker(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField()
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - cont. info: {self.contact_info}"


class Program(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()
    total_tickets = models.IntegerField(default=0)
    available_tickets = models.IntegerField(default=0)

    class Meta:
        permissions = [
            ("can_create_program", "Can Create Program"),
            ("can_edit_program", "Can Edit Program")
        ]

    def __str__(self):
        return f"{self.event.name} - {self.speaker.name} at {self.event.date}: {self.start_time}"

    def clean(self):
        super().clean()
        if self.end_time <= self.start_time:
            raise ValidationError('Час початку повинен бути менше часу закінчення')
        if self.total_tickets < 0:
            raise ValidationError('Загальна кількість білетів не повина бути відьемною')
        if self.available_tickets < 0 or self.available_tickets > self.total_tickets:
            raise ValidationError('Кількість доступних квитків має бути в межах загальної кількості квитків')

    def can_create_ticket(self):
        return self.available_tickets > 0

    def reduce_available_tickets(self):
        if self.can_create_ticket():
            self.available_tickets -= 1
            self.save()
        else:
            raise ValidationError('Квитки Закінчились!')

    def save(self, *args, **kwargs):
        if self.pk:
            old_program = Program.objects.get(pk=self.pk)
            if old_program.total_tickets != self.total_tickets:
                tickets_sold = Ticket.objects.filter(program=self).count()
                self.available_tickets = self.total_tickets - tickets_sold
        else:
            self.available_tickets = self.total_tickets

        super().save(*args, **kwargs)


class Ticket(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    electronic_ticket = models.CharField(max_length=255, blank=True, editable=False)

    def __str__(self):
        return f"{self.user.username} - {self.electronic_ticket}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.program.reduce_available_tickets()
            self.electronic_ticket = str(uuid.uuid4())  # Генерируем электронный билет
        super().save(*args, **kwargs)


