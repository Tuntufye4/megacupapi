from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from collections import defaultdict
from .models import Tournament
from .serializers import TournamentSerializer

class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all().order_by("-match_date")
    serializer_class = TournamentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["group_name", "home_team", "away_team"]

    # ---------------- Upcoming Matches ----------------
    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        now = timezone.now()
        upcoming_matches = Tournament.objects.filter(match_date__gt=now).order_by("match_date")
        serializer = self.get_serializer(upcoming_matches, many=True)
        return Response(serializer.data)
                 
    # GET /tournament/previous/
    @action(detail=False, methods=["get"])
    def previous_match(self, request):
        now = timezone.now()
        previous_matches = Tournament.objects.filter(match_date__lt=now).order_by("-match_date")
        serializer = self.get_serializer(previous_matches, many=True)
        return Response(serializer.data)

    # ---------------- Group Matches ----------------
    @action(detail=False, methods=["get"])
    def group(self, request):
        group_name = request.query_params.get("name")
        if not group_name:
            return Response({"detail": "Group name required"}, status=400)
        matches = Tournament.objects.filter(group_name__iexact=group_name).order_by("match_date")
        serializer = self.get_serializer(matches, many=True)
        return Response(serializer.data)

    # ---------------- Next Match ----------------
    @action(detail=False, methods=["get"])
    def next_match(self, request):
        now = timezone.now()
        next_match = Tournament.objects.filter(match_date__gt=now).order_by("match_date").first()
        if not next_match:
            return Response(None)
        serializer = self.get_serializer(next_match)
        return Response(serializer.data)

    # ---------------- Results / Standings ----------------
    @action(detail=False, methods=["get"])
    def results(self, request):
        group_name = request.query_params.get("group")
        matches = self.queryset
        if group_name:
            matches = matches.filter(group_name__iexact=group_name)

        # Only consider matches with valid scores
        matches = matches.exclude(home_score__isnull=True).exclude(away_score__isnull=True)

        table = defaultdict(lambda: {
            "club": "",
            "mp": 0,
            "w": 0,
            "d": 0,
            "l": 0,
            "gf": 0,
            "ga": 0,
            "gd": 0,
            "pts": 0,
        })

        for match in matches:
            home = table[match.home_team]
            away = table[match.away_team]
            home["club"] = match.home_team
            away["club"] = match.away_team

            home["mp"] += 1
            away["mp"] += 1

            home["gf"] += match.home_score
            home["ga"] += match.away_score
            away["gf"] += match.away_score
            away["ga"] += match.home_score

            home["gd"] = home["gf"] - home["ga"]
            away["gd"] = away["gf"] - away["ga"]

            if match.home_score > match.away_score:
                home["w"] += 1
                home["pts"] += 3
                away["l"] += 1
            elif match.home_score < match.away_score:
                away["w"] += 1
                away["pts"] += 3
                home["l"] += 1
            else:
                home["d"] += 1
                home["pts"] += 1
                away["d"] += 1
                away["pts"] += 1
   
        # Convert to list and sort by points, gd, gf
        results = sorted(table.values(), key=lambda x: (-x["pts"], -x["gd"], -x["gf"]))

        # Assign rank
        for idx, r in enumerate(results, start=1):
            r["rank"] = idx

        return Response(results)     