from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, SpeakerViewSet, ProgramViewSet, TicketViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'speakers', SpeakerViewSet)
router.register(r'programs', ProgramViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls))
]