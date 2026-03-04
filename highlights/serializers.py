from rest_framework import serializers
from .models import Highlights

class HighlightsSerializer(serializers.ModelSerializer):
    class Meta:   
        model = Highlights       
        fields = "__all__"                

          