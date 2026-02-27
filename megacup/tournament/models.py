from django.db import models

class Tournament(models.Model):
    # Group info
    group_name = models.CharField(max_length=10)

    # Teams
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)

    # Scores (optional)
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
   
    # Match details   
    match_date = models.DateTimeField()
    venue = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)   

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return f"{self.home_team} vs {self.away_team} (Group {self.group_name})"  