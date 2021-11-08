from django.urls import path
from .views import newNote, editNote

urlpatterns = [
    path('new/', newNote.as_view(), name="newNote"),
    path('edit/', editNote.as_view(), name="editView")
]