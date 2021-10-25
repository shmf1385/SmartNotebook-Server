from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length=24)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField()

