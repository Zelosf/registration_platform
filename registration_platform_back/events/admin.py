from django.contrib import admin
from .models import Event, Speaker, Program, Ticket
from .models import CustomUser


# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ('name')

admin.site.register(CustomUser)
admin.site.register(Event)
admin.site.register(Speaker)
admin.site.register(Program)
admin.site.register(Ticket)