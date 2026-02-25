from django.urls import path
from .views import HighlightListAPIView

urlpatterns = [
    path('highlights/', HighlightListAPIView.as_view(), name='highlights-list'),
]    