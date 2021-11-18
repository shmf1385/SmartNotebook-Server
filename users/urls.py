from django.urls import path
from .views import deleteUserView, signupView, loginView, checkTokenView

urlpatterns = [
    path('signup/', signupView.as_view(), name="signup"),
    path('login/', loginView.as_view(), name="loginView"),
    path('checkToken/', checkTokenView.as_view(), name="checkTokenView"),
    path('delete/', deleteUserView.as_view(), name="deleteUserView"),
]