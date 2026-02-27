from rest_framework.viewsets import ModelViewSet
from .models import Highlights
from .serializers import HighlightsSerializer   

class HighlightsViewSet(ModelViewSet):   
    queryset = Highlights.objects.all().order_by("-date")
    serializer_class = HighlightsSerializer                                               