from django.urls import path
from .views import signupView, loginView

urlpatterns = [
    path('signup/', signupView.as_view(), name="signup"),
    path('login/', loginView.as_view(), name="loginView")
]