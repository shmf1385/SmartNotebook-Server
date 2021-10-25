from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length=24)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user}/{self.title}"