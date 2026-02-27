from django.db import models
       
class Highlights(models.Model):
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='highlights/')  # Video file
    content = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title        