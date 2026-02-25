from rest_framework import generics
from .models import Highlight
from .serializers import HighlightSerializer

class HighlightListAPIView(generics.ListAPIView):
    queryset = Highlight.objects.all().order_by('-date')  # latest first
    serializer_class = HighlightSerializer       