from rest_framework import serializers
from .models import Highlight

class HighlightSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Highlight
        fields = ['id', 'title', 'video_url', 'description', 'date']

    def get_video_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.video.url)
        return obj.video.url        