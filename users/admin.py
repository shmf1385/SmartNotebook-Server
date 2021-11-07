from django.contrib import admin
from .models import Token, TempSignupCode

admin.site.register(Token)
admin.site.register(TempSignupCode)