from django.db import models
from django.core.exceptions import ValidationError
import uuid
from user.models import CustomUser
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


# For creating an event
class Event(models.Model):
    EVENT_TYPES = (
        ('conference', 'Конференція'),
        ('seminar', 'Семінар'),
        ('workshop', 'Воркшоп'),
    )

    name = models.CharField(max_length=255)
    event_type = models.CharField(choices=EVENT_TYPES, max_length=50)


    def __str__(self):
        return self.name


# For creating a speaker with the ability to provide a biography and contact information
class Speaker(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField()
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - cont. info: {self.contact_info}"


# For creating a program with the option to select one of the existing speakers and events
# With ticket quantity setup
class Program(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    date = models.DateField()
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
        return f"{self.event.name} - {self.speaker.name} at {self.date}: {self.start_time}"

    # Validation for time and ticket quantity
    def clean(self):
        super().clean()
        if self.end_time <= self.start_time:
            raise ValidationError('Час початку повинен бути менше часу закінчення')
        if self.total_tickets < 0:
            raise ValidationError('Загальна кількість білетів не повина бути відьемною')
        if self.available_tickets < 0 or self.available_tickets > self.total_tickets:
            raise ValidationError('Кількість доступних квитків має бути в межах загальної кількості квитків')

    # Checking the possibility of creating a user
    def can_create_ticket(self):
        return self.available_tickets > 0

    # Decreasing the number of available tickets when creating a ticket (user registration for a program)
    def reduce_available_tickets(self):
        if self.can_create_ticket():
            self.available_tickets -= 1
            self.save()
        else:
            raise ValidationError('Квитки Закінчились!')

    def save(self, *args, **kwargs):
        # Adjusting the number of available tickets when saving changes
        if self.pk:
            old_program = Program.objects.get(pk=self.pk)
            if old_program.total_tickets != self.total_tickets:
                tickets_sold = Ticket.objects.filter(program=self).count()
                self.available_tickets = self.total_tickets - tickets_sold
        else:
            self.available_tickets = self.total_tickets

        super().save(*args, **kwargs)


# Creating a ticket and generating the ticket ID and QR code
class Ticket(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    electronic_ticket = models.CharField(max_length=255, blank=True, editable=False)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, editable=False)  # Field for storing the QR code

    def __str__(self):
        return f"{self.user.username} - {self.electronic_ticket}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.program.reduce_available_tickets()
            # Generating an electronic ticket
            self.electronic_ticket = str(uuid.uuid4())
            # Generating a QR code
            qr_data = f"Ticket ID: {self.electronic_ticket}, Program ID: {self.program.id}"  # Data for the QR code
            qr_img = self.generate_qr_code(qr_data)
            self.qr_code.save(f'{self.electronic_ticket}.png', qr_img, save=False)  # Saving the QR code
        super().save(*args, **kwargs)

    # QR code settings
    def generate_qr_code(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return ContentFile(img_bytes.read(), 'qr_code.png')
