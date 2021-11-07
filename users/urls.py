from django.urls import path
from .views import signupView

urlpatterns = [
    path('signup/', signupView.as_view(), name="signup"),
]