# Generated by Django 5.0.7 on 2024-08-12 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_remove_ticket_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user_permissions',
        ),
    ]
