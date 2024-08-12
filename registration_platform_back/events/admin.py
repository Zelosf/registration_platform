from django.contrib import admin
from events.models import Event, Speaker, Program, Ticket



# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ('name')


admin.site.register(Event)
admin.site.register(Speaker)
admin.site.register(Program)
admin.site.register(Ticket)