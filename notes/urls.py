from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.newNote.as_view(), name="newNote")
]