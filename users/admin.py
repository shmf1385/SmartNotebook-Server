from django.contrib import admin
from .models import Token, TempSignupCode, UserDevice

admin.site.register(Token)
admin.site.register(TempSignupCode)
admin.site.register(UserDevice)