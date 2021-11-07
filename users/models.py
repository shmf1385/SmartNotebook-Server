from django.db import models
from django.contrib.auth.models import User

class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=48)

    def __str__(self):
        return f"{self.user}'s Token"

class TempSignupCode(models.Model):
    code = models.CharField(max_length=48)
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)