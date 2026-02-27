from rest_framework import serializers
from .models import Tournament

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = [
            "id",
            "group_name",
            "home_team",
            "away_team",
            "home_score",
            "away_score",
            "match_date",
            "venue",
            "description",
            "created_at",
            "updated_at",
        ]      