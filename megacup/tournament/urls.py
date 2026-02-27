from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TournamentViewSet

router = DefaultRouter()
router.register(r"tournament", TournamentViewSet, basename="tournament")

urlpatterns = [
    path("", include(router.urls)),
]    