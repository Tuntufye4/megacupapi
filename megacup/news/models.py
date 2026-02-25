from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title   