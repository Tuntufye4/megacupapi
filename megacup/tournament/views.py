from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Tournament
from .serializers import TournamentSerializer

class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all().order_by("-match_date")
    serializer_class = TournamentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["group_name", "home_team", "away_team"]

    # GET /tournament/upcoming/
    @action(detail=False, methods=["get"])  
    def upcoming(self, request):
        now = timezone.now()
        upcoming_matches = Tournament.objects.filter(match_date__gt=now).order_by("match_date")
        serializer = self.get_serializer(upcoming_matches, many=True)
        return Response(serializer.data)

    # GET /tournament/group/?name=GROUPNAME
    @action(detail=False, methods=["get"])
    def group(self, request):
        group_name = request.query_params.get("name")
        if not group_name:
            return Response({"detail": "Group name required"}, status=400)
        matches = Tournament.objects.filter(group_name__iexact=group_name).order_by("match_date")
        serializer = self.get_serializer(matches, many=True)
        return Response(serializer.data)       