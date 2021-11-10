from django.urls import path
from .views import signupView, loginView, checkToken

urlpatterns = [
    path('signup/', signupView.as_view(), name="signup"),
    path('login/', loginView.as_view(), name="loginView"),
    path('checkToken/', checkToken.as_view(), name="checkTokenView")
]