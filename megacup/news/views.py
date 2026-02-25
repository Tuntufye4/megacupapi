from rest_framework import generics
from .models import News
from .serializers import NewsSerializer

class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all().order_by('-date')  # latest first
    serializer_class = NewsSerializer     