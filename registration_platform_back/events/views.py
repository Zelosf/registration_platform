from rest_framework import viewsets
from .models import Event, Speaker, Program, Ticket
from .serializers import EventSerializer, SpeakerSerializer, ProgramSerializer, TicketSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


# class TicketViewSet(viewsets.ModelViewSet):
#     # queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         return Ticket.objects.filter(user=user)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer